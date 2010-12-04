"""Distributor"""
import os
import user
import Pyro.core
from multiprocessing import Pool
import json

__version__ = "1.0"
__authors__ = "Bhadresh Patel <bhadresh@wsu.edu>"
__date__ = "Nov 26, 2010"

def dqp(q, p=1, m='QL'):
    """
    Distributed Query Processing
    
    Run the given query on multiple nodes and return the combined result
    """
    nodesfile = os.path.realpath(os.path.join(os.path.dirname(__file__), getattr(user, "dqp_nodes_file", "local.nodes")))
    nodes = open(nodesfile).read().strip().splitlines()
    args = []
    for node in nodes:
        args.append(('PYROLOC://' + node + '/dqp', q, (p * 10), m))

    pool = Pool(processes=len(nodes))
    result = pool.map(do_search, args)
    combined_result = []
    for r in result:
        combined_result.extend(r)
    return combined_result

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
        for r, d in enumerate(result):
            print "%d. %s" % (r + 1, d)
    else:
        print result
