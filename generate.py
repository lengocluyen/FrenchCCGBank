
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

path_conll = "CONLL/ftb_corpus_test/"
dtreeList = readConllFile2(path_conll)

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
        sentenceConlls = dtreeList[dtree]
        ccgMask = CCGMask()
        ccgMask.ccgTask222(sentenceConlls, filename=str(i) + "btree", folder="/home/lengocluyen/Pictures/testF"+str(i))
        i += 1


ExucuteAll()


