from sys import stdin,stdout

lines=stdin.readlines()
for line in lines:
    (term,sep,data)=line.partition(':')
    stdout.write(data)
