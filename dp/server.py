"""Node Server"""
import os
import user
import Pyro.core
import ip
import time

__version__ = "1.0"
__authors__ = "Bhadresh Patel <bhadresh@wsu.edu>"
__date__ = "Nov 26, 2010"

class Search(Pyro.core.ObjBase):
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

    def search(self, q):
        """Search documents for the given query q"""
        log(q)
        return []

def log(msg):
    if _verbose:
        print "[%s] %s" % (time.strftime('%m/%d/%Y %H:%M:%S'), msg)

if __name__=="__main__":
    import optparse
    parser = optparse.OptionParser(description="Node Server",
                                   usage="usage: %prog [options]",
                                   version=__version__)
    parser.add_option('-v', '--verbose', help="Verbose Output [default: %default]", action="count", default=False)

    (options, args) = parser.parse_args()
    _index = None
    _verbose = options.verbose
    
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
        
    Pyro.core.initServer()
    daemon = Pyro.core.Daemon(host=nodeip, port=nodeport)
    uri = daemon.connect(Search(), "dqp")

    log("Server started: %s" % uri)
    try:
        daemon.requestLoop()
    finally:
        daemon.shutdown(True)

