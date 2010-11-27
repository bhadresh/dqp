"""Node Server"""
import os
import Pyro.core
import Pyro.naming
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
                                   usage="usage: %prog [options] index",
                                   version=__version__)
    parser.add_option('-v', '--verbose', help="Verbose Output [default: %default]", action="count", default=False)

    (options, args) = parser.parse_args()
    if not args:
        print "Please select index number"
        parser.print_help()
        raise SystemExit
    
    _index = int(args[0])
    _verbose = options.verbose
        
    Pyro.core.initServer()
    daemon = Pyro.core.Daemon()
    ns = Pyro.naming.NameServerLocator().getNS()
    try:
        ns.createGroup('dqp')
    except:
        pass
    daemon.useNameServer(ns)
    uri = daemon.connect(Search(), "dqp." + str(_index))

    log("Server started: %s" % uri)
    try:
        daemon.requestLoop()
    finally:
        daemon.shutdown(True)

