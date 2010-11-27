"""Distributor"""
import os
import Pyro.core
import Pyro.naming
from multiprocessing import Pool

__version__ = "1.0"
__authors__ = "Bhadresh Patel <bhadresh@wsu.edu>"
__date__ = "Nov 26, 2010"

def dqp(q):
    """
    Distributed Query Processing
    
    Run the given query on multiple nodes and return the combined result
    """
    g = 'dqp' # Group
    try:
        ns = Pyro.naming.NameServerLocator().getNS(host='localhost', port=9090)
        servers = ns.list(g)
    except:
        print "Unable to connect to Pyro NameServer. Start the NameServer at localhost:9090 using pyro-ns command"
        raise SystemExit
    
    if len(servers) == 0:
        print "No server available to process queries."
        raise SystemExit

    pool = Pool(processes=len(servers))
    args = [(g + '.' + servers[i][0], q) for i in range(len(servers))]
    result = pool.map(do_search, args)
    return result
    
def do_search(arg):
    """Call Remote Node and execute Search"""
    u, q = arg
    dqp = Pyro.core.getProxyForURI("PYRONAME://" + u)
    return dqp.search(q)

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
        print "%d. %s" % (r, d)

