"""Distributor"""
import os
import user
import Pyro.core
from multiprocessing import Pool
import json
import operator
import time

__version__ = "1.0"
__authors__ = "Bhadresh Patel <bhadresh@wsu.edu>"
__date__ = "Nov 26, 2010"

def dqp(q, p=1, m='QL'):
    """
    Distributed Query Processing
    
    Run the given query on multiple nodes and return the combined result
    """
    st = time.time()
    nodesfile = os.path.realpath(os.path.join(os.path.dirname(__file__), getattr(user, "dqp_nodes_file", "local.nodes")))
    nodes = open(nodesfile).read().strip().splitlines()
    args = []
    for node in nodes:
        args.append(('PYROLOC://' + node + '/dqp', q, (p * 10), m))

    pool = Pool(processes=len(nodes))
    result = pool.map(do_search, args)
    
    # Merge results
    rdict = {}
    total = 0
    for (rcount, r) in result:
        total = total + rcount
        for rec in r:
            if rec['docid'] in rdict:
                rdict[rec['docid']]['score'] = rdict[rec['docid']]['score'] + rec['score']
            else:
                rdict[rec['docid']] = rec

    results = rdict.values()
    combined_result = sorted(results, key=operator.itemgetter('score'), reverse=True)    
    return {'count': total, 'time': (time.time() - st), 'records': combined_result[(p - 1) * 10:(p * 10)]}

def do_search(arg):
    """Call Remote Node and execute Search"""
    result = []
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
    parser.add_option('-p', '--page', help="Page Number [default: %default]", action="store", type='int', default=1)
    parser.add_option('-m', '--model', help="Retrieval Model [default: %default]", action="store", choices=['QL', 'BM25'], default='QL')

    (options, args) = parser.parse_args()
    if not args:
        print "Please provide query"
        parser.print_help()
        raise SystemExit
    
    _verbose = options.verbose
    
    try:
        query = json.load(args[0])
    except:
        query = {'AND': args[0].split()}
    
    result = dqp(query, options.page, options.model)
    if _verbose:        
        for r, d in enumerate(result['records']):
            print "%d. %s" % (r + 1, d)
    else:
        print result
