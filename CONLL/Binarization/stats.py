import re,os
from CONLL import ElementConll
import codecs
from itertools import groupby
import graphviz
import asciitree
from collections import defaultdict
# Class for construct the nodes of the tree. (Subtrees)
import sys,os
from CONLL.FormatError import FormatError
from six import string_types
import codecs
import re
from CONLL.FormatError import FormatError


def readFile(path):
    with open(path,"r") as file:
        document=[]
        sentence =[]# form \t ccgTag
        i=0
        for line in file:
            contentLine = line.split("\t")
            if len(contentLine)>1:
                i=0
                sentence.append([contentLine[0].replace("\n",""),contentLine[1].replace("\n","")])
            else:
                i+=1
                if i==2:
                    document.append(sentence)
                    sentence=[]

        document.append(sentence)
        return document


fileText = "/home/lengocluyen/PyWorkspace/FrenchCCGBank/ccgresult.txt"
def statsCCG():
    document = readFile(fileText)
    i=0
    #for sentence in document:
    #    for word in sentence:
    #        print (str(i) + "-" + word[0] + " - " + word[1])
    #        i+=1
    #    print("------------------------")
    ccgCollection = []
    for sentence in document:
        for word in sentence:
            ccg = word[1]
            if findInWordCollection(ccg,ccgCollection)==None:
                print ("working ...")
                ccgCollection.append([ccg,1])
            else:
                for ccgitem in ccgCollection:
                    if ccg==ccgitem[0]:
                        ccgitem[1]+=1

    with open("/home/lengocluyen/Dropbox/Inwork/results/statsCCG.txt","w") as file:
        for item in ccgCollection:
            print("printing...")
            file.write(str(item[0]) + "\t" + str(item[1])+ "\n")
        print("Complete")

def statsWords():
    document = readFile(fileText)
    wordCollection = []
    for sentence in document:
        for word in sentence:
            cand = word[0].lower()
            if findInWordCollection(cand,wordCollection)==None:
                print("working ...")
                wordCollection.append([cand, 1, [word[1]]])
            else:
                for worditem in wordCollection:
                    if worditem[0] == cand:
                        worditem[1] += 1
                        worditem[2].append(word[1])
    '''with open("ccgResultWithLemma.txt","w") as file:
        for sentence in document:
            for word in sentence:
                print ("printing")
                file.write(word[0] + "\t" + word[2]+ "\t" + word[1]+"\n")
            file.write("\n")
        print("Complete")'''
    with open("/home/lengocluyen/Dropbox/Inwork/results/statsCCG2.txt", "w") as file:
        for item in wordCollection:
            print("printing...")
            file.write(str(item[0]) + "\t" + str(item[1]) + "\t" + ' '.join(str(e) for e in item[2]) + "\n")
        print("Complete")

    return ""
def findInWordCollection(cand, wordCollection):
    for ca in wordCollection:
        if ca[0] == cand:
            return ca[0]
    return None
def statsLog():
    document = readFile(fileText)
    loglog=[]
    ccgCollection=[]
    i=1
    with open("/home/lengocluyen/Dropbox/Inwork/results/statsCCG3.txt", "w") as file:
        for sentence in document:
            for word in sentence:
                ccg = word[1]
                if ccg not in ccgCollection:
                    print("working ...")
                    ccgCollection.append(ccg)
            temp=ccgCollection
            print("printing...")
            file.write(str(i) + "\t" + str(len(temp))+ "\t" + ' '.join(str(e) for e in temp)+ "\n")
            loglog.append([i,len(temp),temp])
            temp=[]
            i+=1


        print("Complete")

    return ""

def findInCollection(cand, wordCollection):
    for ca in wordCollection:
        if ca[1] == cand:
            return ca
    return None

def readFile2(file,fileout):
    str =  "\\documentclass{article}" + "\n"
    str += "\\usepackage{graphics}"+ "\n"
    str += "\\usepackage{tikz}"+ "\n"
    str += "\\usepackage{pgfplots}"+ "\n"
    str+="\\usepgfplotslibrary{external}" + "\n"
    str+="\\tikzexternalize" + "\n"
    str += "\\begin{document}"+ "\n"
    str += "\\begin{tikzpicture}"+ "\n"
    str += "\\begin{semilogyaxis}["+ "\n"
    str += "xlabel=Index,ylabel=Value]"+ "\n"
    str += "\\addplot[color=blue,mark=*] coordinates {"+ "\n"
    with open(file,"r") as w:
        listresult = []
        for line in w:
            strs = line.split("\t")
            if findInCollection(strs[1],listresult) is None:
                listresult.append([strs[0], strs[1]])
                str+= "("+strs[0] + "," + strs[1]+") " + "\n"
            else:
                listresult.append([strs[0],strs[1]])
    str +="}; \n"
    str +="\\end{semilogyaxis}" + "\n"
    str += "\\end{tikzpicture}" + "\n"
    str +="\\end{document}" + "\n"

    with open(fileout, "w") as w2:
        w2.write(str)
fileText = "/home/lengocluyen/PyWorkspace/FrenchCCGBank/ccgresult.txt"
def statsWords2():
    document = readFile(fileText)
    wordCollection = []
    for sentence in document:
        for word in sentence:
            cand = word[0].lower()
            if findInWordCollection(cand,wordCollection)==None:
                print("working ...")
                wordCollection.append([cand, 1, [word[1]]])
            else:
                for worditem in wordCollection:
                    if worditem[0] == cand:
                        worditem[1] += 1
                        worditem[2].append(word[1])
    '''with open("ccgResultWithLemma.txt","w") as file:
        for sentence in document:
            for word in sentence:
                print ("printing")
                file.write(word[0] + "\t" + word[2]+ "\t" + word[1]+"\n")
            file.write("\n")
        print("Complete")'''
    for it in wordCollection:
        ccgCollection = []
        for ccg in it[2]:
            if ccg not in ccgCollection:
                ccgCollection.append(ccg)
        it.append(len(ccgCollection))
    with open("/home/lengocluyen/Dropbox/Inwork/results/statsCCG22.txt", "w") as file:
        for item in wordCollection:
            print("printing...")
            file.write(str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[3]) + "\n")
            #" + ' '.join(str(e) for e in item[2]) + "\n")
        print("Complete")

    return ""
#ccgresult
#statsCCG()
#statsWords()
#statsLog()

#readFile2("/home/lengocluyen/Dropbox/Inwork/results/statsCCG3.txt","/home/lengocluyen/Dropbox/Inwork/results/statsCCG3latex.tex")
#statsWords2()




import re,os
from CONLL import ElementConll
import codecs
from itertools import groupby
import graphviz
import asciitree
from collections import defaultdict
# Class for construct the nodes of the tree. (Subtrees)
import sys,os
from CONLL.CoNLLXHandle import CoNLLXHandle
from CONLL.FormatError import FormatError
from CONLL.Binarization.NodeInfo import NodeInfo
from CONLL.Binarization.TreeNode import TreeNode
from CONLL.Binarization.BTree import BTree
from CONLL.Binarization.DTree import DTree
from CONLL.Binarization.MappingTree import MappingTree
from CONLL.Binarization.CCGMask import CCGMask

import collections

#the relation in dependency tree
#suj


def readConllFile(path):
    conllx = CoNLLXHandle()
    #listing all file in directory
    dtreeList = []
    for name in os.listdir(path):
        dtreeFileList = []
        #readfile
        f = os.path.join(path, name)
        try:
            #reading conll file content
            for sentence in conllx.read_conllx(f):
                #print(sentence.to_normal_sentence())
                dtree = DTree(sentence)
                dtreeList.append(dtree)
                dtreeFileList.append(dtree)
                #dtree.drawTreeInText()
        except FormatError as e:
            print (sys.stderr, 'Error processing %s: %s' % (f, str(e)))
        #generation ccg for tree

        #save conll file content
    return dtreeList

def testBtree():
    nodeInfo1 = NodeInfo("Sentence", "S")
    nodeInfo2 = NodeInfo("Henri", "NP")
    nodeInfo3 = NodeInfo("mange", "(S\\NP)/NP")
    nodeInfo4 = NodeInfo("des", "NP\\NP")
    nodeInfo5 = NodeInfo("pommes", "NP")
    nodeInfo6 = NodeInfo("que", "Empty")
    nodeInfo7 = NodeInfo("je", "NP")
    nodeInfo8 = NodeInfo("lui", "NP")
    nodeInfo9 = NodeInfo("donne", "(S\\NP)/NP")

    mytree = BTree()
    mytree.put(nodeInfo1, 0)
    mytree.put(nodeInfo2, 0)
    mytree.put(nodeInfo3, 0)
    mytree.put(nodeInfo4, 1)
    mytree.put(nodeInfo5, 0)
    mytree.put(nodeInfo6, 0)
    mytree.put(nodeInfo7, 1)
    mytree.put(nodeInfo8, 0)
    mytree.put(nodeInfo9, 1)

    mytree.drawTree()

    print(mytree)

def listingElement(chunk):
    if hasattr(chunk[0], "form"):
        for element in chunk:
            print (element.form + " ["+ str(element.id) +"] ")
    else:
        for itemList in chunk:
            print ("Chunk in Chunk:")
            listingElement(itemList)
            print ("\n")
def readConllFile2(path):
    conllx = CoNLLXHandle()
    #listing all file in directory
    dtreeList = []
    for name in os.listdir(path):
        dtreeFileList = []
        #readfile
        f = os.path.join(path, name)
        try:
            #reading conll file content
            for sentence in conllx.read_conllx(f):
                #print(sentence.to_normal_sentence())
                dtree = DTree(sentence)
                dtreeList.append(dtree)
                dtreeFileList.append(dtree)
                #dtree.drawTreeInText()
        except FormatError as e:
            print (sys.stderr, 'Error processing %s: %s' % (f, str(e)))
        #generation ccg for tree

        #save conll file content
    return dtreeList
#Execution

path_conll = "CONLL/test/"

path_conll = "CONLL/question/"

path_conll = "CONLL/test/"

path_conll = "CONLL/data/"
dtreeList = readConllFile2(path_conll)

#for dtree in dtreeList:
#    print(dtree.sentence.to_normal_sentence())
#    id = 1
#    for chunk in dtree.chunkingDtree():
#        print("chunk id:" + str(id))
#        for element in chunk:
#            print(element.form + " [" + str(element.id) + "] ")
#        id = id + 1
#        print("\n")


'''
print (dtree.chunkingDtreeRercusion())
id=0

for chunk in dtree.chunkingDtreeRercusion():
    print ("chunk id:"+ str(id))
    listingElement(chunk)
    #    for element in chunk:
    #        print (element.form + " ["+ str(element.id) +"] ")
    id = id + 1
    print ("\n")

'''

#id=0
#for chunk in dtree.chunkingDtree():
#    print ("chunk id:"+ str(id))
#    for element in chunk:
#        print (element.form + " ["+ str(element.id) +"] ")
#    id = id + 1
#    print ("\n")
#mappingTree = MappingTree()
#testList = sorted(dtree.chunkingDtree()[3], key= lambda element: int(element.id))
#for element in testList:
#    print (element.id + " " + element.form + " ")



#dtree = dtreeList[0]
#for item in dtree.chunkingDtreeRercusion():
#    element = mappingTree.getFirstElementOfChunk(item)
#    print ("chunkin: " + element.form + " id " + str(element.id) + " deprel: " + element.deprel )

'''btree = mappingTree.buildTree(dtree.chunkingDtreeRercusion())

btree.drawTree("ccgtagtest",format="png")
print(btree)
print ("chieu cao: " + str (btree.height(btree.root)))
nodeList = []
#print ("Traversal Right Left Node: " + btree.traversalNodeFullChild(btree.root,nodeList))
btree.traversalNodeFullChild(btree.root,nodeList)
print ("node list length: " + str(len(nodeList)))
for item in nodeList:
    print ("NodeItem: " + str(item[0]) + " - "+ str(item[1])+ " - "+ str(item[2]))

    '''


'''
dtree = dtreeList[10]
dtree = dtreeList[28]
dtree = dtreeList[62]
dtree = dtreeList[65]
dtree = dtreeList[66]
dtree = dtreeList[112]

dtree = dtreeList[381]
dtree = dtreeList[244]
'''


def ExecuteOne(dtree):
    print(dtree.sentence.to_normal_sentence())
    # dtree.drawTreeInGraphics("dtreeTest",directory=None)

    # mappingTree = MappingTree()
    # for item in dtree.chunkingDtreeRercusion():
    #    element = mappingTree.getFirstElementOfChunk(item)
    #    print("chunking: " + element.form + " id " + str(element.id) + " deprel: " + element.deprel)
    # bTree = mappingTree.buildTree(dtree.chunkingDtreeRercusion(),dtree.sentence._elements)
    # print (bTree.traversalRightLeftNode(bTree.root))
    # print("tree: " + dtree.dTreeChunkRecursiveInText(dtree.chunkingDtreeRercusion()))
    sentenceConlls = dtree
    ccgMask = CCGMask()
    ccgMask.ccgTask2(sentenceConlls, "btreeTest", None)


def ExucuteAll():
    if os._exists("compare.txt"):
        os.remove("compare.txt")
    if os._exists("compare_finish.txt"):
        os.remove("compare_finish.txt")
    if os._exists("compare_unfinish.txt"):
        os.remove("compare_unfinish.txt")

    i=0
    for dtree in range(0,len(dtreeList)):
        print (str(i) + " : " + dtreeList[dtree].sentence.to_normal_sentence())
        # .drawTreeInGraphics(str(i)+"dtree","/home/lengocluyen/Pictures/test")

        # mappingTree = MappingTree()
        # for item in dtree.chunkingDtreeRercusion():
        #   element = mappingTree.getFirstElementOfChunk(item)
        #   print ("chunking: " + element.form + " id " + str(element.id) + " deprel: " + element.deprel )
        # bTree = mappingTree.buildTree(dtree.chunkingDtreeRercusion())
        # print (bTree.traversalRightLeftNode(bTree.root))
        # print ("tree: "+ dtree.dTreeChunkRecursiveInText(dtree.chunkingDtreeRercusion()))
        sentenceConlls = dtreeList[dtree]
        ccgMask = CCGMask()
        ccgMask.ccgTask222(sentenceConlls, filename=str(i) + "btree", folder="/home/lengocluyen/Pictures/testF"+str(i))

        #ccgMask.ccgTask_Unfinish(sentenceConlls, filename=str(i) + "btree", folder="/home/lengocluyen/Pictures/ATest")
        i += 1

#ExecuteOne(dtreeList[310])
ExucuteAll()


