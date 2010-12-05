from math import log10
import index

LAMBDA = .1
DOC_COUNT = 2500

def calcQLScores(termCount, myindex, query):
    """Query Likelihood Retrieval Model"""
    notTerms = query.get('NOT', [])
    andTerms = query.get('AND', [])
    orTerms = query.get('OR', [])

    termIndex = {}
    docids = []
    # Select all docs from OR and AND terms
    terms = orTerms[:]
    terms.extend(andTerms)
    for term in terms:
        tc = index.getTermContent(myindex, term)
        termIndex[term] = tc
        docids.extend(tc.get('docs', []).keys())
    
    # Remove docs from NOT    
    exdocids = []
    for term in notTerms:
        tc = index.getTermContent(myindex, term)
        exdocids.extend(tc.get('docs', []).keys())
    
    scores = []
    for docID in docids:
        if docID in exdocids:
            continue

        docScore = 0.0
        for term in terms:
            tf = termIndex[term]['docs'].get(docID, 0.0)
            docScore = docScore + log10((1 - LAMBDA) * (tf * 1.0 / termCount[docID]) + 
                                        LAMBDA * (termIndex[term]['count'] * 1.0 / termCount['total']))        
        scores.append([docID, docScore])	
    return scores

