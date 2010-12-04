from math import log10

LAMBDA = .1
DOC_COUNT = 2500


def checkExclusions(docID, notTerms, index):
    for term in notTerms:
        #{"term": {"count": 18, "docs": {0:5, 23:6}}, ...}
        for doc in index[term]['docs']:
            if doc == docID:
                return True
    return False

def checkInclusions(docID, andTerms, index):
    for term in andTerms:
        #{"term": {"count": 18, "docs": {0:5, 23:6}}, ...}
        for doc in index[term]['docs']:
            if doc == docID:
                return True
    return False


def calcQLScores(termCount, index, query):
    
    # format terms
    termMap = parseQuery(query)
    
    notTerms = termMap['NOT']
    andTerms = termMap['AND']
    orTerms = termMap['OR']
    
    scores = []
    for docID in range(1, DOC_COUNT+1):
        exFound = checkExclusions(docID, notTerms, index)
        
        if exFound:
            continue

        inFound = checkInclusions(docID, andTerms, index)
        
        if not inFound:
            continue
        
        docScore = 0.0
        for term in andTerms:
            
            if docID in index[term]['docs']:
                tf = index[term]['docs'][docID]
            else:
                tf = 0.0
            
            docScore = docScore + log10((1 - LAMBDA) * (tf/termCount[docID]) + 
                                        LAMBDA * (index[term]['count']/termCount['total']))
        
        scores.append([docID, docScore])
	
    return scores

        
'''
def parseQuery(query):
    termMap = {}
    termMap['include'] = set([])
    termMap['exclude'] = set([])
    terms = query.split(' ')
    
    for term in terms:
        if term[0] == '-':
            termMap['exclude'].add(term[1:])
        else:
            termMap['include'].add(term)
    
    return termMap
'''