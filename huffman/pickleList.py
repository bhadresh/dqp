from sys import argv
import pickle

if(len(argv)!=3):
    print 'expecting input file and output file'
    exit()

inputFile=open(argv[1],'r')
lines=inputFile.readlines()
inputFile.close()

invertedList={}
outputFile=open(argv[2],'w')
for line in lines:
    (term,sep,data)=line.partition(':')
    invertedList[term]=data
pickle.dump({'type':'uncompressed','data':invertedList},outputFile)
outputFile.close()
