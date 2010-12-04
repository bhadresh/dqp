"""Node Server"""
import os
import sys
import user
import Pyro.core
import ip
import time
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'rm')))
from retrieval import RetrievalModel

__version__ = "1.0"
__authors__ = "Bhadresh Patel <bhadresh@wsu.edu>"
__date__ = "Nov 26, 2010"
_datadir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def log(msg):
    if _verbose:
        print "[%s] %s" % (time.strftime('%m/%d/%Y %H:%M:%S'), msg)

if __name__=="__main__":
    import optparse
    parser = optparse.OptionParser(description="Node Server",
                                   usage="usage: %prog [options]",
                                   version=__version__)
    parser.add_option('-v', '--verbose', help="Verbose Output [default: %default]", action="count", default=False)
    parser.add_option('-d', '--data', help="Data Storage location [default: %default]", action="store", default=_datadir)
    parser.add_option('-c', '--compressed_index', help="Use Compressed Index [default: %default]", action="store_true", default=False)

    (options, args) = parser.parse_args()
    _index = None
    _verbose = options.verbose
    _datadir = options.data
    if not os.path.isdir(_datadir):
        print "Data dir: %s NOT found" % (_datadir)
        raise SystemExit        
    
    nodeip = None
    nodeport = None
    myip = ip.get_ip()
    nodesfile = os.path.realpath(os.path.join(os.path.dirname(__file__), getattr(user, "dqp_nodes_file", "local.nodes")))
    nodes = open(nodesfile).read().strip().splitlines()
    for i, node in enumerate(nodes):
        ip, port = node.split(':')
        if ip == myip:
            _index = i
            nodeip = ip
            nodeport = int(port)
            break

    if nodeip is None or nodeport is None:
        print "Detected Lan IP (%s) for this system is NOT in %s" % (myip, nodesfile)
        raise SystemExit
        
    if options.compressed_index:
        indexfile = os.path.join(_datadir, 'compressed_index', 'index-%d' % (_index))
    else:
        indexfile = os.path.join(_datadir, 'index', 'index-%d' % (_index))
        
    if os.path.exists(indexfile):
        Pyro.core.initServer()
        daemon = Pyro.core.Daemon(host=nodeip, port=nodeport)
        uri = daemon.connect(RetrievalModel(datadir=_datadir, indexfile=indexfile, verbose=_verbose), "dqp")

        log("Server started")
        log("Location: %s" % uri)
        log("Indexfile: %s" % indexfile)
        try:
            daemon.requestLoop()
        finally:
            daemon.shutdown(True)
    else:
        print "Index file: %s NOT found" % (indexfile)
