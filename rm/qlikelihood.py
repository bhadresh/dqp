from math import log10
import index

LAMBDA = .1


def calcQLScores(termCount, myindex, query, coder):
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
        tc = index.getTermContent(myindex, term, coder)
        termIndex[term] = tc
        docids.extend(tc.get('docs', []).keys())
    
    # Remove docs from NOT    
    exdocids = []
    for term in notTerms:
        tc = index.getTermContent(myindex, term, coder)
        exdocids.extend(tc.get('docs', []).keys())

    # Get docs in AND    
    indocids = []
    for term in andTerms:
        indocids.append(termIndex[term].get('docs', []).keys())
        
    scores = []
    for docID in docids:
        if docID in exdocids:
            continue
        
        skip = False
        if len(indocids) > 0:            
            for entry in indocids:
                if docID not in entry:
                    skip = True
                    break

        if skip:
            continue
                    
        docScore = 0.0
        for term in terms:
            if termIndex[term]['count'] != 0:
                tf = termIndex[term]['docs'].get(docID, 0.0)
                docScore = docScore + log10((1 - LAMBDA) * (tf * 1.0 / termCount[docID]) + 
                                            LAMBDA * (termIndex[term]['count'] * 1.0 / termCount['total']))        
        scores.append([docID, docScore])	
    return scores

