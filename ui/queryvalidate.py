#!/Python27 python
import sys, fileinput, queryparser


def validate():
    notFlag = 0
    andFlag = 0
    orFlag = 0
    input = sys.argv[1]
    for letter in input:
        if notFlag or orFlag or andFlag:
            notFlag = 0
            orFlag = 0
            andFlag = 0
            if not letter.isalpha():
                return 0
        if letter == "+":
            andFlag = 1
        if letter == " ":
            orFlag = 1
        if letter == "-":
            notFlag = 1
    if notFlag or orFlag or andFlag:
        return 0
    return 1
####Start####
valid = validate()
if valid:
    queryparser.main(sys.argv[1].lower())
else:
    print "ERROR"