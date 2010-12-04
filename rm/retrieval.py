from sys import argv
from qlikelihood import calcQLScores
import os, glob

pageRankFile = 'out.txt'
termCountsFile = 'termcounts.txt'
indexFile = 'index.txt'
pidMapFile = 'pidmap.txt'
modelType = 'QL'

# PROBLEMS:
#    don't know about index file
#    Is every non-NOT considered AND? Needs double space?


def getRanks(index, query, termCount):
    if modelType == 'QL':
        scores = calcQLScores(termCount, index, query)
    elif modelType == 'BM25':
        print 'BM25' #not implemented yet
    return scores

        
def getPidMap():
    f = open(pidMapFile, 'r')
    doc = f.readlines()
    f.close()

    pidMap = {}
    for line in doc:
        line = line.split(' ')
        pidMap[int(line[0])] = line[1]
    return pidMap


def getIndex():
    f = open(indexFile, 'r')
    doc = f.readlines()
    f.close()

    index = {}
    for line in doc:
        # assumes terms do not have spaces (such as noun phrases)
        line = line.replace(' ', '').split(':')
        #{"term": {"count": 18, "docs": {0:5, 23:6}}, ...}
        index[line[0]] = {'count':int(line[1]), 'docs':{}}
        
        counts = line[2].replace('(', '')[0: -1].split(')')
        for count in counts:            
            count = count.split(',')
            index[term]['docs'][int(count[0])] = int(count[1])
        
            
def getPageRanks():
    f = open(pageRanksFile, 'r')
    doc = f.readlines()
    f.close()

    pageRanks = {}
    for line in doc:
        line = line.split(':')
        pageRanks[int(line[0])] = float(line[1])
        
    return pageRanks


def getTermCounts():
    f = open(termCountsFile, 'r')
    doc = f.readlines()
    f.close()
    
    termCounts = {}
    for line in doc[0: -1]:
        line = line.split(' ')
        termCounts[int(line[0])] = int(line[1])

    termCounts['total'] = int(doc[-1])
    
    return termCounts


def search(query):
    
    #test
    pidMap = getPidMap()
    pageRanks = getPageRanks()
    termCount = getTermCount()
    index = getIndex()
    #test
    
    scores = getRanks(index, query, termCount)
    results = []
    for entry in scores:
        result = {}
        result['docid'] = entry[0]
        result['score'] = entry[1]
        result['url'] = pidMap[entry[0]]
        result['pagerank'] = pageRanks[entry[0]]
        results.append(result)
    return results

