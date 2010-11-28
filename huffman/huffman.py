import heapq

def getCharCounts(text):
    countMap={}
    for ch in text:
        if(ch in countMap):
            countMap[ch]=countMap[ch]+1
        else:
            countMap[ch]=1
    return countMap

def createCountPQueue(countMap):
    pQueue=[]
    for key in countMap:
        heapq.heappush(pQueue,(countMap[key],key,None,None))
    return pQueue

def getHuffmanTree(countPQueue):
    if(len(countPQueue)==1):
        return heapq.heappop(countPQueue)
    else:
        node1=heapq.heappop(countPQueue)
        node2=heapq.heappop(countPQueue)
        newNode=(node1[0]+node2[0],node1[1]+node2[1],node1,node2)
        heapq.heappush(countPQueue,newNode)
        return getHuffmanTree(countPQueue)


def getCharCodeFromHuffmanTree(char,huffmanTree):
    if(huffmanTree[1]==char):
        return ''
    elif(huffmanTree[2]!=None and char in huffmanTree[2][1]):
        return '0'+getCharCodeFromHuffmanTree(char,huffmanTree[2])
    else: 
        return '1'+getCharCodeFromHuffmanTree(char,huffmanTree[3])

def getCodeMapFromHuffmanTree(huffmanTree):
    codeMap={}
    charSet=set([x for x in huffmanTree[1]])
    for char in charSet:
        codeMap[char]=getCharCodeFromHuffmanTree(char,huffmanTree)
    return codeMap

def getCodeFromText(text):
    charCounts=getCharCounts(text)
    countPQueue=createCountPQueue(charCounts)
    huffmanTree=getHuffmanTree(countPQueue)
    return getCodeMapFromHuffmanTree(huffmanTree),huffmanTree

class HuffmanCoder:
    codeMap=None
    huffTree=None
    
    def __init__(self,codeMap,huffTree):
        self.codeMap=codeMap
        self.huffTree=huffTree

    def bitStringToChar(self,bitString):
        charNum=0
        for char in reversed(bitString):
            charNum=charNum*2+int(char)
        return chr(charNum)

    def charToBitString(self,char):
        bitString=''
        charNum=ord(char)
        for i in range(0,8):
            bitString=bitString+str(charNum%2)
            charNum=charNum/2
        return bitString
    
    def encodeText(self,inputText):
        extraBits=8-len(inputText)%8
    
        encodedText=''
        currentBitString=''
        for ch in inputText:
            currentBitString=currentBitString+self.codeMap[ch]
            if(len(currentBitString)>8):
                tempString=currentBitString[:8]
                currentBitString=currentBitString[8:]
                encodedText=encodedText+self.bitStringToChar(tempString)

        extraBits=len(currentBitString)
        return chr(extraBits)+encodedText+self.bitStringToChar(currentBitString)

    def decodeBinary(self,encodedString):
        decodedString=''
        extraBits=ord(encodedString[0])
        currentBitString=''
        currentHuffmanNode=self.huffTree
        for i,char in enumerate(encodedString[1:]):
            currentBitString=self.charToBitString(char)
            if(i==len(encodedString)-2):
                currentBitString=currentBitString[:extraBits]
            for bit in currentBitString:
                if(bit=='0'):
                    currentHuffmanNode=currentHuffmanNode[2]
                else:
                    currentHuffmanNode=currentHuffmanNode[3]
                if(len(currentHuffmanNode[1])==1):
                    decodedString=decodedString+currentHuffmanNode[1]
                    currentHuffmanNode=self.huffTree
        return decodedString
