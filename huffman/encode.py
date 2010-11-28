from sys import argv
import pickle

if(len(argv)!=4):
    print 'expecting input file and code file and output file'
    exit()

inputFile=open(argv[1],'r')
inputText=inputFile.read()
inputFile.close()

codeFile=open(argv[2],'r')
huffmanCoder=pickle.load(codeFile)
codeFile.close()

outputFile=open(argv[3],'w')
outputFile.write(huffmanCoder.encodeText(inputText))
outputFile.close()

