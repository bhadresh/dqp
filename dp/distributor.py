"""Distributor"""
import os
import user
import Pyro.core
from multiprocessing import Pool

__version__ = "1.0"
__authors__ = "Bhadresh Patel <bhadresh@wsu.edu>"
__date__ = "Nov 26, 2010"

def dqp(q):
    """
    Distributed Query Processing
    
    Run the given query on multiple nodes and return the combined result
    """
    nodesfile = os.path.realpath(os.path.join(os.path.dirname(__file__), getattr(user, "dqp_nodes_file", "local.nodes")))
    nodes = open(nodesfile).read().strip().splitlines()
    args = []
    for node in nodes:
        args.append(('PYROLOC://' + node + '/dqp', q))

    pool = Pool(processes=len(nodes))
    result = pool.map(do_search, args)
    return result

def do_search(arg):
    """Call Remote Node and execute Search"""
    result = []
    try:
        uri, q = arg
        dqp = Pyro.core.getProxyForURI(uri)
        result = dqp.search(q)
    except:
        pass
    return result

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser(description="Distributor - perform search on multiple nodes",
                                   usage="usage: %prog [options] query",
                                   version=__version__)
    parser.add_option('-v', '--verbose', help="Verbose Output [default: %default]", action="count", default=False)

    (options, args) = parser.parse_args()
    if not args:
        print "Please provide query"
        parser.print_help()
        raise SystemExit
    
    _verbose = options.verbose
    result = dqp(args[0])
    for r, d in enumerate(result):
        print "%d. %s" % (r + 1, d)

