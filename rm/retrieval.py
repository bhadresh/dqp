"""Retrieval Model"""
from qlikelihood import calcQLScores
from bm25 import calcBM25Scores
import Pyro.core
import index
import os
import time

def getPidMap(pidMapFile):
    f = open(pidMapFile, 'r')
    doc = f.readlines()
    f.close()

    pidMap = {}
    for line in doc:
        line = line.strip().split(' ', 1)
        pidMap[int(line[0])] = line[1]
    return pidMap

def getPageRanks(pageRanksFile):
    """Load Page Ranks"""
    f = open(pageRanksFile, 'r')
    doc = f.readlines()
    f.close()

    pageRanks = {}
    for line in doc:
        line = line.strip().split(':')
        pageRanks[int(line[0])] = float(line[1])        
    return pageRanks

def getTermCounts(termCountsFile):
    """Load Term Counts"""
    f = open(termCountsFile, 'r')
    doc = f.readlines()
    f.close()
    
    totalNumDocs = 0
    termCounts = {}
    for line in doc[0: -1]:
        line = line.strip().split(' ')
        termCounts[int(line[0])] = int(line[1])
        totalNumDocs = totalNumDocs + 1
    
    termCounts['average'] = int(doc[-1]) / totalNumDocs
    termCounts['total'] = int(doc[-1])
    termCounts['totalDocs'] = totalNumDocs
    return termCounts
        
class RetrievalModel(Pyro.core.ObjBase):
    """Retrieval Model"""
    def __init__(self, datadir, indexfile, verbose=False):
        """Initialize"""
        Pyro.core.ObjBase.__init__(self)
        self.datadir = datadir
        self.verbose = verbose
        
        # Load Data into memory
        self.index = index.getIndex(indexfile)
        self.pidMap = getPidMap(os.path.join(datadir, "pid_map.dat"))
        self.pageRanks = getPageRanks(os.path.join(datadir, "pagerank.dat"))
        self.termCount = getTermCounts(os.path.join(datadir, "term_counts.dat"))
        self.coder = index.getCoder(os.path.join(datadir,'huffmanCode'))

    def getRanks(self, query, model):
        """Calculate Score"""
        if model == 'QL':
            scores = calcQLScores(self.termCount, self.index, query,self.coder)
        elif model == 'BM25':
            scores = calcBM25Scores(self.termCount, self.index, query,self.coder)
        return scores

    def search(self, query, K=10, model='BM25'):
        """Perform Search"""
        self.log(query)
        scores = self.getRanks(query, model)
        results = []
        for entry in scores[:K]: # Returning TOP K results
            results.append({
                'docid': entry[0],
                'score': entry[1],
                'url': self.pidMap[entry[0]],
                'pagerank': self.pageRanks[entry[0]]            
            })
        return (len(scores), results)
    
    def log(self, msg):
        if self.verbose:
            print "[%s] %s" % (time.strftime('%m/%d/%Y %H:%M:%S'), msg)
    
