The programs in this folder create huffman codes and use those codes
to encode or decode given files.

huffman.py:
	This file is a library used by the createCode.py script.

createCode.py:
	This script creates a huffman code for use by the encoder and
	decoder. It takes as arguments a file to be used to create
	the code. It creates a file called 'huffmanCode' that is
	a pickled huffmanCoder object to be used by the encode
	and decode script.

encode.py:
	This script encodes a given text file. It takes as arguments
	an input file to be encoded, a file containing a pickled
	huffmanCoder object, and the name of the file the output
	should be written to.

decode.py:
	This script decodes a given text file. It takes as arguments
	an input file to be decoded, a file containing a pickled 
	huffmanCoder object, and the name of the file the output
	should be written to.
