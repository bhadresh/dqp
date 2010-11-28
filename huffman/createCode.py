from sys import argv
import heapq
from pprint import PrettyPrinter
import huffman
import pickle

def printCode(codeMap):
    for key in sorted(codeMap):
        print (key,codeMap[key])

def getCompressionInfo(inputText,codeMap):
    ''' Return a Tuple containing the original number of bits, the final number of bits, and the compression ratio.'''
    codedSum=0
    for char in inputText:
        codedSum=codedSum+len(codeMap[char])
    startSize=len(inputText)*8
    endSize=codedSum
    ratio=float(startSize)/endSize
    return (startSize,endSize,ratio)

def printCodeInfo(inputText,codeMap):
    print 'Code Map:'
    printCode(codeMap)
    rawSize,compressedSize,ratio=getCompressionInfo(inputText,codeMap)
    print 'Original Size(bits):',rawSize,', Compressed Size(bits):',compressedSize,', Compression Ratio:',ratio

if(len(argv)>2):
    print 'expecting one argument'
    exit()
elif(len(argv)==1):
    argv.append('InputOutput.txt')

inputFile=open(argv[1],'r')
inputText=inputFile.read()

codeMap,codeTree=huffman.getCodeFromText(inputText)
huffmanCoder=huffman.HuffmanCoder(codeMap,codeTree)
pickleFile=open('huffmanCode','w')
pickle.dump(huffmanCoder,pickleFile)
pickleFile.close()
