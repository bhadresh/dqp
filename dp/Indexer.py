"""Generate Indexes"""
import os

__version__ = "1.0"
__authors__ = "Bhadresh Patel <bhadresh@wsu.edu>"
__date__ = "Dec 04, 2010"

if __name__ == "__main__":
    _storage = os.path.realpath(os.path.join(os.path.dirname(__file__), '../data'))
    import optparse
    parser = optparse.OptionParser(description="Indexer", usage="usage: %prog [options]")
    parser.add_option('-v', '--verbose', help="Verbose Output [default: %default]", action="count", default=False)
    parser.add_option('-i', '--input', help="Input stored files [default: %default]", default=os.path.join(_storage, 'stemmed', ''))
    parser.add_option('-o', '--output', help="Output location to stored files [default: %default]", default=os.path.join(_storage, 'index', ''))

    (options, args) = parser.parse_args()
    indir = options.input
    outdir = options.output
    verbose = options.verbose

    terms = {}        
    for f in os.listdir(indir):
        print "Processing: %s" % (f)
        fp = open(os.path.join(indir, f), "r")
        content = fp.read()
        fp.close()

        lines = content.splitlines()
        if len(lines) > 1:
            for term in lines[1].split():
                if terms.has_key(term):
                    if terms[term].has_key(f):
                        terms[term][f] = terms[term][f] + 1
                    else:
                        terms[term][f] = 1
                else:
                    terms[term] = {f: 1}
    
    totalterms = len(terms)    
    _index = -1
    fp = None
    sterms = sorted(terms.keys())
    for n, term in enumerate(sterms):
        if fp == None or n % (totalterms / 5) == 0:
            if fp:
                fp.close()
            _index = _index + 1
            fp = open(os.path.join(outdir, 'index-%d' % _index), 'w')
        
        content = "%s:%d:" % (term, len(terms[term]))
        for docid, count in terms[term].iteritems():
            content = content + "(%s, %d)" % (docid, count)
        fp.write(content + "\n")
