from sys import argv
import pickle

if(len(argv)!=4):
    print 'expecting input file and code file and output file'
    exit()

inputFile=open(argv[1],'r')
lines=inputFile.readlines()
inputFile.close()

codeFile=open(argv[2],'r')
huffmanCoder=pickle.load(codeFile)
codeFile.close()

compressedInvertedList={}
outputFile=open(argv[3],'w')
for line in lines:
    (term,sep,data)=line.partition(':')
    compressedInvertedList[term]=huffmanCoder.encodeText(data)
pickle.dump({'type':'compressed','data':compressedInvertedList},outputFile)
outputFile.close()
