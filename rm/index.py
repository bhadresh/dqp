"""Index Processing"""

def getIndex(indexFile):
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

def getTermContent(indx, term):
    """Get Documents for given term"""
    return indx.get(term, {'count':0, 'docs':{}})

