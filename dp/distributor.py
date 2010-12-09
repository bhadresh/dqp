"""Distributor"""
import os
import user
import Pyro.core
from multiprocessing import Pool
import json
import operator
import time
import sys
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ui')))
import queryparser

__version__ = "1.0"
__authors__ = "Bhadresh Patel <bhadresh@wsu.edu>"
__date__ = "Nov 26, 2010"

def findIndex(vec, term):
    for i, line in enumerate(vec):
        word = line.strip().split(': ')[1]
        if term <= word:
            return i
    return -1

def dqp(q, p=1, m='QL'):
    """
    Distributed Query Processing
    
    Run the given query on multiple nodes and return the combined result
    """
    st = time.time()
    nodesfile = os.path.realpath(os.path.join(os.path.dirname(__file__), getattr(user, "dqp_nodes_file", "local.nodes")))
    nodes = open(nodesfile).read().strip().splitlines()

    indexwords = open(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'algorithmForGettingIndex'))).read().strip().splitlines()    
    indexnodes = []
    for ttype,terms in q.iteritems():
        for term in terms:
            ind = findIndex(indexwords, term)
            if ind != -1 and ind not in indexnodes:
                indexnodes.append(ind)
                        
    args = []
    for ind in indexnodes:
        args.append(('PYROLOC://' + nodes[ind] + '/dqp', q, (p * 10), m))
    
    total = 0
    combined_result = []
    if len(args) > 0:
        pool = Pool(processes=len(args))
        result = pool.map(do_search, args)
        
        # Merge results
        rdict = {}
        for (rcount, r) in result:
            total = total + rcount
            for rec in r:
                if rec['docid'] in rdict:
                    rdict[rec['docid']]['score'] = rdict[rec['docid']]['score'] + rec['score']
                else:
                    rdict[rec['docid']] = rec

        results = rdict.values()
        combined_result = sorted(results, key=operator.itemgetter('score'), reverse=True)
        combined_result = combined_result[(p - 1) * 10:(p * 10)]
        
    return {'count': total, 'time': (time.time() - st), 'records': combined_result}

def do_search(arg):
    """Call Remote Node and execute Search"""
    result = {'count': 0, 'time': 0, 'records': []}
    try:
        uri, q, k, m = arg
        dqp = Pyro.core.getProxyForURI(uri)
        result = dqp.search(q, k, m)
    except Exception as e:
        print "Exception:", e
    return result

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser(description="Distributor - perform search on multiple nodes",
                                   usage="usage: %prog [options] query",
                                   version=__version__)
    parser.add_option('-v', '--verbose', help="Verbose Output [default: %default]", action="count", default=False)
    parser.add_option('-q', '--query', help="Query", action="store")
    parser.add_option('-p', '--page', help="Page Number [default: %default]", action="store", type='int', default=1)
    parser.add_option('-m', '--model', help="Retrieval Model [default: %default]", action="store", choices=['QL', 'BM25'], default='QL')

    (options, args) = parser.parse_args()
    if not args and not options.query:
        print "Please provide query"
        parser.print_help()
        raise SystemExit
    
    _verbose = options.verbose
    
    query = options.query if options.query else args[0]
    valid = queryparser.validate(query)
    if valid:
        query = queryparser.main(query.lower())
    else:
        print {'count':0, 'records':[], 'error': 'Invalid Query'}
        raise SystemExit
    
    result = dqp(query, options.page, options.model)
    if _verbose:        
        for r, d in enumerate(result['records']):
            print "%d. %s" % (r + 1, d)
    else:
        print result
