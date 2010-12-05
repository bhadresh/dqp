"""Index Processing"""
import pickle

def parseCountString(countString):
    countString = countString.strip().replace(' ','').split(':')
    countMap = {'count':int(countString[0]), 'docs':{}}
    counts = countString[1].replace('(','')[:-1].split(')')
    for count in counts:
        count = count.split(',')
        countMap['docs'][int(count[0])] = int(count[1])
    return countMap
'''
def getIndex(indexFile,isCompressed):
    """Load Index"""
    f = open(indexFile, 'r')
    doc = f.readlines()
    f.close()

    index = {}
    for line in doc:
        # assumes terms do not have spaces (such as noun phrases)
        line = line.strip().replace(' ', '').split(':')
        #{"term": {"count": 18, "docs": {0:5, 23:6}}, ...}
        term = line[0]
        index[term] = {'count':int(line[1]), 'docs':{}}        
        counts = line[2].replace('(', '')[0: -1].split(')')
        for count in counts:            
            count = count.split(',')
            index[term]['docs'][int(count[0])] = int(count[1])
    return index
'''

def getIndex(indexFile):
    """Load Index"""
    f = open(indexFile, 'r')
    index=pickle.load(f)
    f.close()

    
    #if it isn't compressed parse the index into a map
    if(index['type']=='uncompressed'):
        for term in index['data'].keys():
            # assumes terms do not have spaces (such as noun phrases)
            #{"term": {"count": 18, "docs": {0:5, 23:6}}, ...}
            countString=index['data'][term]
            index['data'][term]=parseCountString(countString)
    return index

def getTermContent(index, term, coder):
    """Get Documents for given term"""
    default={'count':0,'docs':{}}
    if(index['type']=='uncompressed'):
        return index['data'].get(term,default)
    else:
        compressedCounts=index['data'].get(term,'')
        if(compressedCounts==''):
            return default
        else:
            return parseCountString(coder.decodeBinary(compressedCounts))

def getCoder(codeFilename):
    """Load huffman code"""
    codeFile=open(codeFilename,'r')
    coder=pickle.load(codeFile)
    codeFile.close()
    return coder
