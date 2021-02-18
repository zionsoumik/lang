from __future__ import division
import csv

from numpy import random
f=open("COLAG_2011_flat_formatted.txt")
reader=csv.reader(f, delimiter='\t')
LD={}
LD1={}

### choosegrammar gets the probabities for all the parameters and returns the current grammar
def choosegrammar(grammar):
    ret=""
    for g in grammar:
        #gl=random.choice([0,1],p=[1-g,g])
        gl=random.random()
        if gl<g:
            ret=ret+str(1)
        else:
            ret = ret + str(0)
        #ret=ret+str(gl)
    return ret

for row in reader:
    LD[row[0]]=set()
    LD1[row[0]] = set()
    #print(row[0])

f.close()
f1=open("COLAG_2011_flat_formatted.txt")
reader1=csv.reader(f1, delimiter='\t')
#LD1={}

# LD is for the regular language domain
# LD1 is for the ns items

for row1 in reader1:
    #LD1[row[0]] = []
    if row1[1]=='IMP' and 'S' not in row[1]:
        LD1[row1[0]].add('DEC' + row1[2])
    else:
        LD1[row1[0]].add(row1[1] + row1[2])
    #print(row1[1])
    LD[row1[0]].add(row1[1]+row1[2])
#print(LD)
#print(LD1)
#f2=open("english.txt")
#reader2=csv.reader(f2,delimiter='\t')
r=0.001
faculty=0
max_sentences=500000
Gtarg = [0,0,0,1,0,0,1,1,0,0,0,1,1]
initial_grammar=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
f3=open("output.csv","wb")
write = csv.writer(f3)
for i in range(0,500000):
    faculty = (i - 220000) / 200000
    if faculty < 0:
        faculty = 0
    if faculty > 1:
        faculty = 1
    ch = random.choice([1, 2], p=[1 - faculty, faculty])
    #ch=2 uncomment this to get the pure var learner
    l=""
    '''
        l is the current grammar initial grammar is the weights. we choose l untill the l in in colag 
        domain and choosegrammar() has the probabilities right.
    '''
    while l not in LD.keys():
        l = choosegrammar(initial_grammar)
    write.writerow(initial_grammar)
    #print("l",l)
    if ch==1:
        #print(g)
        sentence = random.choice(list(LD1["0001001100011"]))
        #l=random.choice(LD1.keys())
        if sentence in LD[l]:
            for j in range(0,len(l)):
                #print(l[j])
                if l[j]=='0':
                    initial_grammar[j]=initial_grammar[j]-r*initial_grammar[j]
                else:
                    initial_grammar[j]=initial_grammar[j]+r*(1-initial_grammar[j])
    else:
        sentence = random.choice(list(LD["0001001100011"]))
        #write.writerow(list(l))

        #write.writerow(sentence)
        if sentence in LD[l]:
            for j in range(0,len(l)):
                #print(j,initial_grammar[j])
                if initial_grammar[j]>0.02 and initial_grammar[j]<0.98:
                    if l[j]=='0':
                        initial_grammar[j]=initial_grammar[j]-r*initial_grammar[j]
                    else:
                        initial_grammar[j]=initial_grammar[j]+r*(1-initial_grammar[j])
print(initial_grammar)





