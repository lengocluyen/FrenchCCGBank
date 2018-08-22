import re
import copy
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
from CONLL.Binarization.MappingComponentTree import MappingComponentTree
from CONLL.Binarization.CCGRules import CCGRules
from CONLL.Binarization.CategoryTree import CategoryTree

from CONLL.Binarization.CategoryTreeNode import CategoryTreeNode

CCGMASK = {
    "N":"NP",
    "Det":"NP\\NP"
}
class CCGMask:
    def wordFunction(self,element=None ):
        mask = "empty"
        if element is None:
            return "empty"
        return element.xpostag

    def ccgTask(self,sentenceConlls,filename=None,folder=None):
        mappingTree = MappingTree()
        dtreeChunk = sentenceConlls.chunkingDtreeRercusion()

        #print("so sanh: " + sentenceConlls.dTreeChunkRecursiveInText(dtreeChunk))
        #sentenceConlls.chunkingDtreeRercusion(dtreeChunk)
        #print("so sanh vs: " + sentenceConlls.dTreeChunkRecursiveInText(dtreeChunk))

        btree = mappingTree.buildTree(dtreeChunk)
        tripleNodeSet = []
        mappingTree.traversalBtreeRightLeftParent(btree.root,tripleNodeSet)
        self.generateCCGTagForNodeTopDown(btree.root)
        self.assignCCGTagForLeafNode(btree,tripleNodeSet,sentenceConlls,dtreeChunk)
        self.generateCCGTagForNodeBottomUp(btree.root)
        countLeafBtree = btree.countLeaf(btree.root)
        countNodeDtree = sentenceConlls.countWord()
        if countLeafBtree == countNodeDtree:
            s = str(countLeafBtree) + " B-D " + str(countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
            print ("export result into image")
            if folder is None:
                btree.drawTree(filename,directory=None, format="png")
                sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
            else:
                btree.drawTree(filename, directory=folder, format="png")
                sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/test")
        else:
            s = str(countLeafBtree) + " B-D " + str(
                countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()

            print("export result into image")
            if folder is None:
                btree.drawTree(filename, directory=None, format="png")
                sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
            else:
                btree.drawTree(filename, directory=folder, format="png")
                sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/testF")


            #print(btree)

        file = open("compare.txt", "a")
        file.write(s + "\n")
        file.close()
        print ("All finish")

    def ccgTask3(self,sentenceConlls,filename=None,folder=None):
        mappingTree = MappingTree()
        dtreeChunk = sentenceConlls.chunkingDtreeRercusion()

        #print("so sanh: " + sentenceConlls.dTreeChunkRecursiveInText(dtreeChunk))
        #sentenceConlls.chunkingDtreeRercusion(dtreeChunk)
        #print("so sanh vs: " + sentenceConlls.dTreeChunkRecursiveInText(dtreeChunk))

        btree = mappingTree.buildTree(dtreeChunk)
        tripleNodeSet = []
        mappingTree.traversalBtreeRightLeftParent(btree.root,tripleNodeSet)
        self.generateCCGTagForNodeTopDown(btree.root)
        self.assignCCGTagForLeafNode(btree,tripleNodeSet,sentenceConlls,dtreeChunk)
        self.generateCCGTagForNodeBottomUp(btree.root)
        countLeafBtree = btree.countLeaf(btree.root)
        countNodeDtree = sentenceConlls.countWord()
        if countLeafBtree != countNodeDtree:
            s = str(countLeafBtree) + " B-D " + str(countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()

        #self.generateCCGTagForNodeTopDown(btree.root)
            print ("export result into image")
            if folder is None:
                btree.drawTree(filename,directory=None, format="png")
                sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
            else:
                btree.drawTree(filename, directory=folder, format="png")
                sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/test")


            #print(btree)

        else:
            s ="__________"
        file = open("compare.txt", "a")
        file.write(s + "\n")
        file.close()
        print ("All finish")
    def isSentence(self,sentence):
        for element in sentence._elements:
            if element.deprel == "root" and str(element.upostag) == "V":
                return element
        return None
    def ccgTask2(self,sentenceConlls,filename=None,folder=None):
        dtreeChunk = sentenceConlls.chunkingDtreeRercusion()
        mappingTree = MappingComponentTree()
        btree = mappingTree.buildTree(dtreeChunk,sentenceConlls.sentence._elements)
        #mappingTree = MappingTree()
        #btree = mappingTree.buildTree(dtreeChunk,sentenceConlls.sentence._elements)
        tripleNodeSet = []
        mappingTree.traversalBtreeRightLeftParent(btree.root,tripleNodeSet)
        self.assignCCGTagForLeafNode(btree,tripleNodeSet,sentenceConlls,dtreeChunk)
        if self.isSentence(sentenceConlls.sentence) is not None:
            self.adjustTreeWithVParametre(dtreeChunk,btree)

        self.generateCCGTagForNodeTopDown(btree.root)

        self.traversalFilterTree(btree, sentenceConlls)

        #self.generateCCGTagForNodeBottomUp(btree.root)

        print(sentenceConlls.dTreeChunkRecursiveInText(dtreeChunk))
        s = sentenceConlls.sentence.to_normal_sentence()
        print (s)
        print ("export result into image")
        btree.drawTree(filename,directory=None, format="png")
        sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
        print ("All finish")


    def ccgTask22(self,sentenceConlls,filename=None,folder=None):
        dtreeChunk = sentenceConlls.chunkingDtreeRercusion()
        mappingTree = MappingComponentTree()
        btree = mappingTree.buildTree(dtreeChunk, sentenceConlls.sentence._elements)
        # mappingTree = MappingTree()
        # btree = mappingTree.buildTree(dtreeChunk,sentenceConlls.sentence._elements)
        tripleNodeSet = []
        mappingTree.traversalBtreeRightLeftParent(btree.root, tripleNodeSet)
        self.assignCCGTagForLeafNode(btree, tripleNodeSet, sentenceConlls, dtreeChunk)

        self.adjustTreeWithVParametre(btree)

        self.generateCCGTagForNodeTopDown(btree.root)

        # self.generateCCGTagForNodeBottomUp(btree.root)

        print(sentenceConlls.dTreeChunkRecursiveInText(dtreeChunk))
        #s = sentenceConlls.sentence.to_normal_sentence()
        #print(s)
        countLeafBtree = btree.countLeaf(btree.root)
        countNodeDtree = len(sentenceConlls.sentence._elements)
        countMissed = self.missCCGNode(btree.root)

        if countLeafBtree == countNodeDtree:
            s = "-------------------------------------"
            # if countMissed == 0:
            # s = "finish - Good" + str(countLeafBtree) + " B-D " + str(
            # countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
            # if folder is None:
            #    btree.drawTree(filename, directory=None, format="png")
            #    sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
            # else:
            #    btree.drawTree(filename, directory=folder, format="png")
            #    sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/T2")

            # else:
            # s = "unfinish - Bad " + str(countLeafBtree) + " B-D " + str(
            # countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
            file = open("compare_finish.txt", "a")
            file.write(s + "\n")
            file.close()
        else:
            # if countMissed == 0:

            # s = "finish - bad" + str(countLeafBtree) + " B-D " + str(
            #    countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
            # s= "Btree Unfinish: " + str(j) + " phrases"
            # if folder is None:
            #    btree.drawTree(filename, directory=None, format="png")
            #    sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
            # else:
            #    btree.drawTree(filename, directory=folder, format="png")
            #    sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/T22")

            # print(btree)
            # else:
            s = "Unfinish - bad" + str(countLeafBtree) + " B-D " + str(
                countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
            file = open("compare_unfinish.txt", "a")
            file.write(s + "\n")
            file.close()

        file = open("compare.txt", "a")
        file.write(s + "\n")
        file.close()
        print("All finish")

    def ccgTask222(self,sentenceConlls,filename=None,folder=None):
        dtreeChunk = sentenceConlls.chunkingDtreeRercusion()
        mappingTree = MappingComponentTree()
        btree = mappingTree.buildTree(dtreeChunk, sentenceConlls.sentence._elements)
        # mappingTree = MappingTree()
        # btree = mappingTree.buildTree(dtreeChunk,sentenceConlls.sentence._elements)
        tripleNodeSet = []
        mappingTree.traversalBtreeRightLeftParent(btree.root, tripleNodeSet)
        self.assignCCGTagForLeafNode(btree, tripleNodeSet, sentenceConlls, dtreeChunk)
        if self.isSentence(sentenceConlls.sentence) is not None:
            self.adjustTreeWithVParametre(dtreeChunk,btree)

        #self.generateCCGTagForNodeTopDown(btree.root)
        self.generateCCGTagForNodeBottomUp(btree.root)
        self.traversalFilterTree(btree,sentenceConlls)

        #print(sentenceConlls.dTreeChunkRecursiveInText(dtreeChunk))
        #s = sentenceConlls.sentence.to_normal_sentence()
        #print(s)
        countLeafBtree = btree.countLeaf(btree.root)
        countNodeDtree = len(sentenceConlls.sentence._elements)
        countMissed = self.missCCGNode(btree.root)

        if countMissed == 0:
            if countLeafBtree == countNodeDtree:
                s = "Positive finish " + str(countLeafBtree) + " B-D " + str(
                    countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
                '''if folder is None:
                    btree.drawTree(filename, directory=None, format="png")
                    sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
                else:
                    btree.drawTree(filename, directory=folder, format="png")
                    sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/T2")
'''
            else:
                s = "Negative finish " + str(countLeafBtree) + " B-D " + str(
                    countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
            file = open("scompare_finish28.txt", "a")
            file.write(s + "\n")
            file.close()
        else:
            if countLeafBtree == countNodeDtree:
                 s = "Positive Unfinish " + str(countLeafBtree) + " B-D " + str(
                    countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
                 #s= "Btree Unfinish: " + str(j) + " phrases"
                 '''if folder is None:
                    btree.drawTree(filename, directory=None, format="png")
                    sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
                 else:
                    btree.drawTree(filename, directory=folder, format="png")
                    sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/T22")
'''
                # print(btree)
            else:
                s = "Negative Unfinish " + str(countLeafBtree) + " B-D " + str(
                    countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()
            file = open("scompare_unfinish28.txt", "a")
            file.write(s + "\n")
            file.close()

        file = open("scompare28.txt", "a")
        file.write(s + "\n")
        file.close()

        self.saveSentenceAndCCG(btree,"ccgresult28.txt")

        print("All finish")

    def saveSentenceAndCCG(self,btree,filename):
        wordsNodeList=[]
        wordsNodeList = self.getListOfLeaf(btree.root,wordsNodeList)
        sentence = ""
        categoryTree = CategoryTree()
        for word in wordsNodeList:
            if len(word.nodeInfo.ccgTag)>0:
                sentence += str(word.nodeInfo.element.id) + "\t" + word.nodeInfo.element.form + "\t" +word.nodeInfo.element.lemma + "\t" \
                            + self.isEmptyInStr(word.nodeInfo.element.upostag)  + "\t" + self.isEmptyInStr(word.nodeInfo.element.xpostag) + "\t" \
                            + self.isEmptyInStr(str(word.nodeInfo.element.head))+ "\t"+ self.isEmptyInStr(str(word.nodeInfo.element.deprel))  + "\t"+ self.isEmptyInStr(word.nodeInfo.element.deps)  + "\t" \
                            + self.isEmptyInStr(categoryTree.traversalRNLinText(word.nodeInfo.ccgTag[0].root))+"\n"
        sentence +="\n"
        file = open(filename, "a")
        file.write(sentence + "\n")
        file.close()
    def isEmptyInStr(self, s):
        if s is None:
            s="-"
        return s
    def ccgTask_Unfinish(self,sentenceConlls,filename=None,folder=None):
        dtreeChunk = sentenceConlls.chunkingDtreeRercusion()
        mappingTree = MappingComponentTree()
        btree = mappingTree.buildTree(dtreeChunk, sentenceConlls.sentence._elements)
        # mappingTree = MappingTree()
        # btree = mappingTree.buildTree(dtreeChunk,sentenceConlls.sentence._elements)
        tripleNodeSet = []
        mappingTree.traversalBtreeRightLeftParent(btree.root, tripleNodeSet)
        self.assignCCGTagForLeafNode(btree, tripleNodeSet, sentenceConlls, dtreeChunk)
        if self.isSentence(sentenceConlls.sentence) is not None:
            self.adjustTreeWithVParametre(dtreeChunk,btree)
        self.generateCCGTagForNodeTopDown(btree.root)
        self.traversalFilterTree(btree)
        # self.generateCCGTagForNodeBottomUp(btree.root)

        print(sentenceConlls.dTreeChunkRecursiveInText(dtreeChunk))
        #s = sentenceConlls.sentence.to_normal_sentence()
        #print(s)
        countLeafBtree = btree.countLeaf(btree.root)
        countNodeDtree = len(sentenceConlls.sentence._elements)
        countMissed = self.missCCGNode(btree.root)
        if countMissed == 0:
            if countLeafBtree == countNodeDtree:
                s = "finish"
                # if folder is None:
                #    btree.drawTree(filename, directory=None, format="png")
                #    sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
                # else:
                #    btree.drawTree(filename, directory=folder, format="png")
                #    sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/T2")

            else:
                s = "finish " + str(countLeafBtree) + " B-D " + str(
                    countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()

            btree.drawTree(filename, directory="/home/lengocluyen/Pictures/ATest", format="png")
            sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/ATest/Correction")

            file = open("qcompare_finish.txt", "a")
            file.write(s + "\n")
            file.close()
        else:
            if countLeafBtree == countNodeDtree:
                s = "Unfinish"
                # s= "Btree Unfinish: " + str(j) + " phrases"
                # if folder is None:
                #    btree.drawTree(filename, directory=None, format="png")
                #    sentenceConlls.drawTreeInGraphics(filename + "dtree", "")
                # else:
                #    btree.drawTree(filename, directory=folder, format="png")
                #    sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/T22")

                # print(btree)
            else:
                s = "Unfinish " + str(countLeafBtree) + " B-D " + str(
                    countNodeDtree) + ": " + sentenceConlls.sentence.to_normal_sentence()


            btree.drawTree(filename, directory="/home/lengocluyen/Pictures/ATest", format="png")
            sentenceConlls.drawTreeInGraphics(filename + "dtree", "/home/lengocluyen/Pictures/ATest/Incorrection")

            file = open("qcompare_unfinish.txt", "a")
            file.write(s + "\n")
            file.close()

        file = open("qcompare.txt", "a")
        file.write(s + "\n")
        file.close()
        print("All finish")

    def getListOfLeaf(self,node, listLeaf=None):
        if node.isLeaf():
            listLeaf.append(node)
        if node.hasLeftChild():
            self.getListOfLeaf(node.leftChild,listLeaf)
        if node.hasRightChild():
            self.getListOfLeaf(node.rightChild,listLeaf)
        return listLeaf

    def getListofNonLeaves(self, node, listNonLeaf = None):
        if node.nodeInfo.element is None:
            listNonLeaf.append(node)
        if node.hasLeftChild():
            self.getListofNonLeaves(node.leftChild,listNonLeaf)
        if node.hasRightChild():
            self.getListofNonLeaves(node.rightChild,listNonLeaf)
        return listNonLeaf

    def traversalFilterTree(self,bTree,dTree):
        self.traversalFilterTreeForLeaves(bTree)
        self.traversalFilterTreeForNonLeaves(bTree,bTree.root,dTree)

    def traversalFilterTreeForLeaves(self, bTree):
        listLeaf = []
        listLeaf = self.getListOfLeaf(bTree.root,listLeaf)

        print ("leaf:" + str(len(listLeaf)))
        listResult = []
        i=0
        backback=False
        while i<len(listLeaf):
            ccgForNode = []
            node_i = listLeaf[i]
            listResultLen = len(listResult)
            k=0
            if backback==True:
                if len(listResult)>1:
                    k=listResult[len(listResult)-1][0]-1
                else:
                    break
            for j in range(k,len(node_i.nodeInfo.ccgTag)):
                oldCCGTag = node_i.nodeInfo.ccgTag
                newCCGTag = []
                newCCGTag.append(node_i.nodeInfo.ccgTag[j])
                #listLeaf danh sach cac node la
                #listResult chua danh sach cac ket qua danh duoc
                self.updateCCGTreeForNode(bTree.root, node_i,newCCGTag)
                self.cleanNodeNotLeaf(bTree.root)
                self.generateCCGTagForNodeBottomUp(bTree.root)
                countMissed = self.missCCGNode(bTree.root)
                if countMissed == 0:
                    backback=False
                    ccgForNode.append(j)
                    ccgForNode.append(oldCCGTag[j])
                    listResult.append(ccgForNode)
                    break
                else:
                    self.updateCCGTreeForNode(bTree.root, node_i, oldCCGTag)
            self.newsCCGPathValidation(bTree, listLeaf, listResult)
            if listResultLen==len(listResult):
                backback = True
                i-=1
            i+=1
        if len(listResult)==len(listLeaf):
            self.cleanNodeNotLeaf(bTree.root)
            self.newsCCGPathValidation(bTree,listLeaf,listResult)
            self.generateCCGTagForNodeBottomUp2(bTree.root)

    def traversalFilterTreeForNonLeaves(self, bTree,root,dTree):
        listNonLeaf = []
        listNonLeaf = self.getListofNonLeaves(bTree.root,listNonLeaf)

        print ("None leaf:" + str(len(listNonLeaf)))
        listResult = []
        i=0
        backback=False
        while i<len(listNonLeaf):
            ccgForNode = []
            node_i = listNonLeaf[i]
            listResultLen = len(listResult)
            k=0
            if backback==True:
                if len(listResult)>1:
                    k=listResult[len(listResult)-1][0]-1
                else:
                    break
            for j in range(k,len(node_i.nodeInfo.ccgTag)):
                oldCCGTag = node_i.nodeInfo.ccgTag
                newCCGTag = []
                newCCGTag.append(node_i.nodeInfo.ccgTag[j])
                #listLeaf danh sach cac node la
                #listResult chua danh sach cac ket qua danh duoc
                self.updateCCGTreeForNodeNonLeaves(bTree.root, node_i,newCCGTag)
                #self.cleanNodeNotLeaf(bTree.root)
                self.generateCCGTagForNodeBottomUpForNonLeaves(bTree.root)
                countMissed = self.missCCGNode(bTree.root)

                if countMissed == 0:
                    #if (dTree.isSentence()==True and len(bTree.root.nodeInfo.ccgTag)==1 and bTree.root.nodeInfo.ccgTag[0].root == "S") or (dTree.isSentence()==False and len(bTree.root.nodeInfo.ccgTag)==1):
                    backback=False
                    ccgForNode.append(j)
                    ccgForNode.append(oldCCGTag[j])
                    listResult.append(ccgForNode)
                    break
                else:
                    self.updateCCGTreeForNodeNonLeaves(bTree.root, node_i, oldCCGTag)
            self.newsCCGPathValidationNonLeaves(bTree, listNonLeaf, listResult)


            if listResultLen==len(listResult):
                backback = True
                i-=1
            i+=1
        if len(listResult)==len(listNonLeaf):
            self.cleanNodeNotLeaf(bTree.root)
            self.newsCCGPathValidationNonLeaves(bTree,listNonLeaf,listResult)
            #self.generateCCGTagForNodeBottomUp2(bTree.root)

    def cleanNodeNotLeaf(self,node):
        if node.nodeInfo.element is None and node.parent is not None:
            node.nodeInfo.ccgTag=[]
        if node.hasLeftChild():
            self.cleanNodeNotLeaf(node.leftChild)
        if node.hasRightChild():
            self.cleanNodeNotLeaf(node.rightChild)


    def newsCCGPathValidation(self,bTree, listLeaf, listResult):
        for i in range(0,len(listResult)):
            ccg=[]
            ccg.append(listResult[i][1])
            self.updateCCGTreeForNode(bTree.root, listLeaf[i],ccg)

    def existantCCGPathValidation(self, bTree, listLeaf, listResult):
        for i in range(0,len(listResult)):
            self.updateCCGTreeForNode(bTree.root, listLeaf[i], listLeaf[i].nodeInfo.ccgTag)

    def updateCCGTreeForNode(self,btreeNode, nodeUpdate, ccgUpdate):
        if btreeNode.isLeaf():
            if int(btreeNode.key) == int(nodeUpdate.key):
               btreeNode.nodeInfo.ccgTag = ccgUpdate
        if btreeNode.hasLeftChild():
            self.updateCCGTreeForNode(btreeNode.leftChild, nodeUpdate, ccgUpdate)
        if btreeNode.hasRightChild():
            self.updateCCGTreeForNode(btreeNode.rightChild, nodeUpdate, ccgUpdate)

    def newsCCGPathValidationNonLeaves(self,bTree, listNonLeaves, listResult):
        for i in range(0,len(listResult)):
            ccg=[]
            ccg.append(listResult[i][1])
            self.updateCCGTreeForNodeNonLeaves(bTree.root, listNonLeaves[i],ccg)

    def existantCCGPathValidationNonLeaves(self, bTree, listLeaf, listResult):
        for i in range(0,len(listResult)):
            self.updateCCGTreeForNodeNonLeaves(bTree.root, listLeaf[i], listLeaf[i].nodeInfo.ccgTag)

    def updateCCGTreeForNodeNonLeaves(self,btreeNode, nodeUpdate, ccgUpdate):
        if btreeNode.nodeInfo.element is None:
            if int(btreeNode.key) == int(nodeUpdate.key):
               btreeNode.nodeInfo.ccgTag = ccgUpdate
        if btreeNode.hasLeftChild():
            self.updateCCGTreeForNodeNonLeaves(btreeNode.leftChild, nodeUpdate, ccgUpdate)
        if btreeNode.hasRightChild():
            self.updateCCGTreeForNodeNonLeaves(btreeNode.rightChild, nodeUpdate, ccgUpdate)


    def _traversalFilterTree(self, node,bTree):
        if node.isLeaf():
            ccgLabelList = node.nodeInfo.ccgTag
            length = len(ccgLabelList)
            if length>1:
                i=0
                while i<length:
                    print("i:"+ str(i))
                    self.generateCCGTagForNodeBottomUp(bTree.root)
                    countMissed = self.missCCGNode(bTree.root)
                    if countMissed>0:
                        ccgLabelList.remove(ccgLabelList[i])
                    i+=1
        if node.hasLeftChild():
            self._traversalFilterTree(node.leftChild,bTree)
        if node.hasRightChild():
            self._traversalFilterTree(node.rightChild,bTree)


    def adjustTreeWithVParametre(self,dtreeRercusive,bTree):
        treeNode = bTree.root
        modifiedNodeList = []
        modifiedNodeList = self._adjustTreeWithParametre(treeNode,bTree,modifiedNodeList)
        for item in modifiedNodeList:
            node = item[1]
            numberNode=item[0]
            # tim cha cua root trong cay
            parentVerbChunk = None

            isRootInLeftTree = self.isRootAndLeftTree(node,bTree)

            parentVerbChunk = self.getParentNodeOfChunk(dtreeRercusive,bTree, bTree.root, node,isRootInLeftTree)
            # nut trai la cum verb
            # tach con trai cho den khi no bang numberNode
            headList = []  # chua phan tu dau cua moi chunk cua cac tap con trai

            #parentVerbChunk.leftChild.parent = None
            #parentVerbChunk.rightChild.parent = None
            rightChildNode = parentVerbChunk.rightChild
            if rightChildNode.isLeaf(): break
            leftChildNode = parentVerbChunk.leftChild
            parentVerbChunk.leftChild = None
            parentVerbChunk.rightChild = None
            i = 1
            while i < numberNode:
                # tach nut con phai cua cha lam 2
                if rightChildNode.hasLeftChild():
                    rightChildNode.leftChild.parent = None
                headList.append(rightChildNode.leftChild)
                rightChildNode = rightChildNode.rightChild
                i += 1
            rightChildNode.parent = None
            headList.append(rightChildNode)
            # ghep noi
            key = bTree.size + 100
            newChildTree = BTree()

            newChildTree.put(leftChildNode)
            for childNode in headList:
                tempTree = BTree()
                # can be difine CCG here for node
                treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
                key += 1
                treeNode.parent = None
                tempTree.put(treeNode)
                tt = BTree()
                tt.put(childNode)
                tempTree.putTree(tt, treeNode, 1)
                tempTree.putTree(newChildTree, treeNode, 0)
                newChildTree = tempTree

            # ghep vao vi tri chinh
            if int(parentVerbChunk.key)==int(bTree.root.key):
                parentVerbChunk.root = newChildTree.root
                parentVerbChunk.leftChild = newChildTree.root.leftChild
                parentVerbChunk.rightChild = newChildTree.root.rightChild
            else:
                newChildTree.root.parent = parentVerbChunk.parent
                if parentVerbChunk is parentVerbChunk.parent.leftChild:
                    parentVerbChunk.parent.leftChild = newChildTree.root
                else:
                    parentVerbChunk.parent.rightChild = newChildTree.root
                newChildTree.root = None
            #parentVerbChunk.rightChild=None
            #bTree.putTree(newChildTree, parentVerbChunk, 1)



    def _adjustTreeWithParametre(self,node,bTree, res=[]):
        if node is not None:
            if node.isLeaf()==True and (node.nodeInfo.element.xpostag=="V" or node.nodeInfo.element.xpostag=="VINF" or \
                                        node.nodeInfo.element.xpostag == "VPR" or node.nodeInfo.element.xpostag=="VIMP"):
                numberNode =  self.countFsInLeafNode(node.nodeInfo.ccgTag[0].root)
                if numberNode>1:
                    res.append([numberNode,node])
        if node.hasLeftChild():
            self._adjustTreeWithParametre(node.leftChild,bTree,res)
        if node.hasRightChild():
            self._adjustTreeWithParametre(node.rightChild,bTree,res)

        return res



    #isRootAndLeft use for the question
    def isRootAndLeftTree(self,node, btree):
        fin = False
        res = []
        nodeRoot = btree.root
        if nodeRoot.hasLeftChild() and node.nodeInfo is not None and  str(node.nodeInfo.element.deprel)=="root":
            res = self._isRootAndLeftTree(node,nodeRoot.leftChild,btree,res)
            if len(res)>0:
                fin = True
        return fin

    def _isRootAndLeftTree(self, node, nodeRoot, btree, res):
        if nodeRoot.hasLeftChild():
            self._isRootAndLeftTree(node,nodeRoot.leftChild,btree,res)
        if nodeRoot.hasRightChild():
            self._isRootAndLeftTree(node,nodeRoot.rightChild,btree,res)
        if nodeRoot.isLeaf():
            if int(nodeRoot.key)==int(node.key):
                res.append(nodeRoot)
        return res

    def searchChunkofElementinChunk(self,node,chunk,fChunk=None):
        if hasattr(chunk[0], "form") == False:
            for i in range(0,len(chunk)):
                self.searchChunkofElementinChunk(node, chunk[i],fChunk)
        else:
            for item in chunk:
                if int(node.nodeInfo.element.id) == int(item.id):
                    fChunk.append(chunk)
        return fChunk

    def getParentNodeOfChunk(self,dtreeRercusive,btree,node, searchedNode,isRootInLeftTree,res=None):
        if node.hasLeftChild():
            res = self.getParentNodeOfChunk(dtreeRercusive,btree,node.leftChild,searchedNode,isRootInLeftTree,res)
        if node.hasRightChild():
            res = self.getParentNodeOfChunk(dtreeRercusive,btree,node.rightChild,searchedNode,isRootInLeftTree,res)
        if int(node.key) == int(searchedNode.key):
            fChunk= []
            fChunk = self.searchChunkofElementinChunk(node,dtreeRercusive,fChunk)
            length = len(fChunk[0])
            if length> 5: length=1
            i=0
            tempNode = node
            while i<length:
                tempNode = tempNode.parent
                i+=1
            res = tempNode

            '''parentNode = node.parent
            grandParent = parentNode.parent
            if grandParent is not None:
                if isRootInLeftTree==False and (int(parentNode.leftChild.key) == int(node.key) or int(parentNode.rightChild.key) == int(node.key))  and \
                        (int(grandParent.rightChild.key) ==int(parentNode.key)):
                    res = parentNode
                elif isRootInLeftTree==True and (int(parentNode.leftChild.key) == int(node.key) or int(parentNode.rightChild.key) == int(node.key))  and \
                        int(grandParent.leftChild.key) ==int(parentNode.key):
                    if int(btree.root.key)==int(grandParent.key):
                        res = grandParent
                    else:
                        res = parentNode
                else:
                    res = self.getParentNodeOfChunk(btree,btree.root,parentNode,isRootInLeftTree,res)
            else:
                if int(parentNode.leftChild.key) == int(node.key) or int(parentNode.rightChild.key) == int(node.key):
                    res = parentNode
                else:
                    res = self.getParentNodeOfChunk(btree,btree.root,parentNode,isRootInLeftTree,res)
            '''
        return res
    def countFsInLeafNode(self,nodeLabel):
        count=0
        if nodeLabel.label=="/":
            count+=1
            if nodeLabel.hasLeftChild():
                count += self.countFsInLeafNode(nodeLabel.leftChild)
        return count

    def missCCGNode(self,node):
        count =0
        if node is not None:
            if len(node.nodeInfo.ccgTag)<=0:
                count = 1
        if node.hasLeftChild():
            count += self.missCCGNode(node.leftChild)
        if node.hasRightChild():
            count += self.missCCGNode(node.rightChild)
        return count



    def generateCCGTagForNodeBottomUp(self,currentNode):
        catTree = CategoryTree()
        if currentNode.hasRightChild():
            self.generateCCGTagForNodeBottomUp(currentNode.rightChild)
        if currentNode.hasLeftChild():
            self.generateCCGTagForNodeBottomUp(currentNode.leftChild)
        if currentNode.hasLeftChild() and currentNode.hasRightChild():
            leftNode = currentNode.leftChild
            rightNode = currentNode.rightChild
            parentNode = currentNode
            ccgRule = CCGRules()
            if leftNode.nodeInfo.ccgTag is None:
                leftNode.nodeInfo.ccgTag = []
            if rightNode.nodeInfo.ccgTag is None:
                rightNode.nodeInfo.ccgTag = []
            if parentNode.nodeInfo.ccgTag is None:
                parentNode.nodeInfo.ccgTag = []
            argLeft = leftNode.nodeInfo.ccgTag
            argRight = rightNode.nodeInfo.ccgTag
            resultTop = parentNode.nodeInfo.ccgTag

            if leftNode.nodeInfo.element is None:
                argLeft = self.addEquivalentCCG(leftNode.nodeInfo.ccgTag)
            if rightNode.nodeInfo.element is None:
                argRight = self.addEquivalentCCG(rightNode.nodeInfo.ccgTag)
            if parentNode.nodeInfo.element is None:
               resultTop = self.addEquivalentCCG(parentNode.nodeInfo.ccgTag)

            if len(parentNode.nodeInfo.ccgTag)>0 and len(rightNode.nodeInfo.ccgTag)>0:
                for iArgRight in argRight:
                    for iResultTop in resultTop:
                        iArgRightCopy  = copy.deepcopy(iArgRight)
                        iResultOpCopy = copy.deepcopy(iResultTop)
                        ccg = ccgRule.allRules(argRight=iArgRightCopy,resultTop=iResultOpCopy)
                        #if ccg is None and (self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg) == True or self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg) == True):
                        if ccg is not None and  self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg)==False:
                            leftNode.nodeInfo.ccgTag.append(ccg)
            elif len(leftNode.nodeInfo.ccgTag) >0 and len(rightNode.nodeInfo.ccgTag) > 0:
                for iArgLeft in argLeft:
                    for iArgRight in argRight:
                        iArgLeftCopy = copy.deepcopy(iArgLeft)
                        iArgRightCopy = copy.deepcopy(iArgRight)
                        ccg = ccgRule.allRules(argLeft=iArgLeftCopy, argRight=iArgRightCopy)
                        if ccg is not None and self.ccgExistCheck(parentNode.nodeInfo.ccgTag,ccg) is False:
                            parentNode.nodeInfo.ccgTag.append(ccg)


                #self.updateTreeNode(parentNode, btree.root)
            elif len(parentNode.nodeInfo.ccgTag)>0 and len(leftNode.nodeInfo.ccgTag)>0:
                for iArgLeft in argLeft:
                    for iResultTop in resultTop:
                        iArgLeftCopy = copy.deepcopy(iArgLeft)
                        iResultTopCopy = copy.deepcopy(iResultTop)
                        ccg = ccgRule.allRules(argLeft=iArgLeftCopy,resultTop=iResultTopCopy)
                        if ccg is not None and self.ccgExistCheck(rightNode.nodeInfo.ccgTag,ccg)==False:
                            rightNode.nodeInfo.ccgTag.append(ccg)

    def generateCCGTagForNodeBottomUpForNonLeaves(self,currentNode):
        catTree = CategoryTree()
        if currentNode.hasRightChild():
            self.generateCCGTagForNodeBottomUp(currentNode.rightChild)
        if currentNode.hasLeftChild():
            self.generateCCGTagForNodeBottomUp(currentNode.leftChild)
        if (currentNode.hasLeftChild() and currentNode.hasRightChild()) is False:
            if (currentNode.hasLeftChild() and currentNode.hasRightChild()):
                leftNode = currentNode.leftChild
                rightNode = currentNode.rightChild
                parentNode = currentNode
                ccgRule = CCGRules()
                if leftNode.nodeInfo.ccgTag is None:
                    leftNode.nodeInfo.ccgTag = []
                if rightNode.nodeInfo.ccgTag is None:
                    rightNode.nodeInfo.ccgTag = []
                if parentNode.nodeInfo.ccgTag is None:
                    parentNode.nodeInfo.ccgTag = []
                argLeft = leftNode.nodeInfo.ccgTag
                argRight = rightNode.nodeInfo.ccgTag

                if leftNode.nodeInfo.element is None:
                    argLeft = self.addEquivalentCCG(leftNode.nodeInfo.ccgTag)
                if rightNode.nodeInfo.element is None:
                    argRight = self.addEquivalentCCG(rightNode.nodeInfo.ccgTag)
                if len(leftNode.nodeInfo.ccgTag) > 0 and len(rightNode.nodeInfo.ccgTag) > 0:
                    for iArgLeft in argLeft:
                        for iArgRight in argRight:
                            iArgLeftCopy = copy.deepcopy(iArgLeft)
                            iArgRightCopy = copy.deepcopy(iArgRight)
                            ccg = ccgRule.allRules(argLeft=iArgLeftCopy, argRight=iArgRightCopy)
                            if ccg is not None and self.ccgExistCheck(parentNode.nodeInfo.ccgTag, ccg) is False:
                                parentNode.nodeInfo.ccgTag.append(ccg)
                '''if len(parentNode.nodeInfo.ccgTag)>0 and len(rightNode.nodeInfo.ccgTag)>0:
                    for iArgRight in argRight:
                        for iResultTop in resultTop:
                            iArgRightCopy  = copy.deepcopy(iArgRight)
                            iResultOpCopy = copy.deepcopy(iResultTop)
                            ccg = ccgRule.allRules(argRight=iArgRightCopy,resultTop=iResultOpCopy)
                            #if ccg is None and (self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg) == True or self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg) == True):
                            if ccg is not None and  self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg)==False:
                                leftNode.nodeInfo.ccgTag.append(ccg)
                elif len(leftNode.nodeInfo.ccgTag) >0 and len(rightNode.nodeInfo.ccgTag) > 0:
                    for iArgLeft in argLeft:
                        for iArgRight in argRight:
                            iArgLeftCopy = copy.deepcopy(iArgLeft)
                            iArgRightCopy = copy.deepcopy(iArgRight)
                            ccg = ccgRule.allRules(argLeft=iArgLeftCopy, argRight=iArgRightCopy)
                            if ccg is not None and self.ccgExistCheck(parentNode.nodeInfo.ccgTag,ccg) is False:
                                parentNode.nodeInfo.ccgTag.append(ccg)

            
                    #self.updateTreeNode(parentNode, btree.root)
                elif len(parentNode.nodeInfo.ccgTag)>0 and len(leftNode.nodeInfo.ccgTag)>0:
                    for iArgLeft in argLeft:
                        for iResultTop in resultTop:
                            iArgLeftCopy = copy.deepcopy(iArgLeft)
                            iResultTopCopy = copy.deepcopy(iResultTop)
                            ccg = ccgRule.allRules(argLeft=iArgLeftCopy,resultTop=iResultTopCopy)
                            if ccg is not None and self.ccgExistCheck(rightNode.nodeInfo.ccgTag,ccg)==False:
                                rightNode.nodeInfo.ccgTag.append(ccg)'''

    def generateCCGTagForNodeBottomUp2(self,currentNode):
        catTree = CategoryTree()
        if currentNode.hasRightChild():
            self.generateCCGTagForNodeBottomUp2(currentNode.rightChild)
        if currentNode.hasLeftChild():
            self.generateCCGTagForNodeBottomUp2(currentNode.leftChild)
        if currentNode.hasLeftChild() and currentNode.hasRightChild():
            leftNode = currentNode.leftChild
            rightNode = currentNode.rightChild
            parentNode = currentNode
            ccgRule = CCGRules()
            if leftNode.nodeInfo.ccgTag is None:
                leftNode.nodeInfo.ccgTag = []
            if rightNode.nodeInfo.ccgTag is None:
                rightNode.nodeInfo.ccgTag = []
            if parentNode.nodeInfo.ccgTag is None:
                parentNode.nodeInfo.ccgTag = []
            argLeft = leftNode.nodeInfo.ccgTag
            argRight = rightNode.nodeInfo.ccgTag
            resultTop = parentNode.nodeInfo.ccgTag

            if leftNode.nodeInfo.element is None:
                argLeft = self.addEquivalentCCG(leftNode.nodeInfo.ccgTag)
            if rightNode.nodeInfo.element is None:
                argRight = self.addEquivalentCCG(rightNode.nodeInfo.ccgTag)
            if parentNode.nodeInfo.element is None:
               resultTop = self.addEquivalentCCG(parentNode.nodeInfo.ccgTag)

            if len(parentNode.nodeInfo.ccgTag)>0 and len(rightNode.nodeInfo.ccgTag)>0:
                for iArgRight in argRight:
                    for iResultTop in resultTop:
                        iArgRightCopy  = copy.deepcopy(iArgRight)
                        iResultOpCopy = copy.deepcopy(iResultTop)
                        ccg = ccgRule.allRules(argRight=iArgRightCopy,resultTop=iResultOpCopy)
                        #if ccg is None and (self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg) == True or self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg) == True):
                        if ccg is not None and  self.ccgExistCheck(leftNode.nodeInfo.ccgTag,ccg)==False:
                            leftNode.nodeInfo.ccgTag.append(ccg)
            elif len(leftNode.nodeInfo.ccgTag) >0 and len(rightNode.nodeInfo.ccgTag) > 0:
                for iArgLeft in argLeft:
                    for iArgRight in argRight:
                        iArgLeftCopy = copy.deepcopy(iArgLeft)
                        iArgRightCopy = copy.deepcopy(iArgRight)
                        ccg = ccgRule.allRules(argLeft=iArgLeftCopy, argRight=iArgRightCopy)
                        if ccg is not None and self.ccgExistCheck(parentNode.nodeInfo.ccgTag,ccg) is False:
                            parentNode.nodeInfo.ccgTag.append(ccg)


                #self.updateTreeNode(parentNode, btree.root)
            elif len(parentNode.nodeInfo.ccgTag)>0 and len(leftNode.nodeInfo.ccgTag)>0:
                for iArgLeft in argLeft:
                    for iResultTop in resultTop:
                        iArgLeftCopy = copy.deepcopy(iArgLeft)
                        iResultTopCopy = copy.deepcopy(iResultTop)
                        ccg = ccgRule.allRules(argLeft=iArgLeftCopy,resultTop=iResultTopCopy)
                        if ccg is not None and self.ccgExistCheck(rightNode.nodeInfo.ccgTag,ccg)==False:
                            rightNode.nodeInfo.ccgTag.append(ccg)

    def ccgExistCheck(self,ccgTagCollection,ccg):
        catTree = CategoryTree()
        for ic in ccgTagCollection:
            if str(catTree.traversalRNLinText(ic.root))==str(catTree.traversalRNLinText(ccg.root)):
                return True
        return False

        #if currentNode.hasRightChild():
        #    self.generateCCGTagForNodeTopDown(currentNode.rightChild)
        #if currentNode.hasLeftChild():
        #    self.generateCCGTagForNodeTopDown(currentNode.leftChild)
    def assignCCGTagForLeafNode(self,btree,tripleNodeSet,sentenceConll, dTree ):
        for itemTriple in tripleNodeSet:
            leftNode = itemTriple[1]
            rightNode = itemTriple[0]
            parentNode = itemTriple[2]
            #for the leaf node
            if rightNode.nodeInfo.element  is not None:
                #assigne ccg tag for node
                rightNode.nodeInfo.ccgTag = self.ccgTagForElement(rightNode.nodeInfo.element,sentenceConll,dTree,position=1)
                self.updateTreeNode(rightNode,btree.root)
            if leftNode.nodeInfo.element  is not None:
                leftNode.nodeInfo.ccgTag = self.ccgTagForElement(leftNode.nodeInfo.element, sentenceConll, dTree,position=0)
                self.updateTreeNode(leftNode, btree.root)


    def updateTreeNode(self,nodeUpdate,node):
        if nodeUpdate.key is node.key:
            node.nodeInfo = nodeUpdate.nodeInfo
        else:
            if node.hasLeftChild():
                self.updateTreeNode(nodeUpdate,node.leftChild)
            if node.hasRightChild():
                self.updateTreeNode(nodeUpdate,node.rightChild)

    def searchDependencyWithVerb(self,element,sentenceConll):
        dependencyList = []
        for itemE in sentenceConll.sentence._elements:
            if itemE.head  == element.id and (str(itemE.deprel) == "a_obj" or str(itemE.deprel) == "p_obj" \
                                              or str(itemE.deprel) == "obj" or str(itemE.deprel) == "obj.p" or \
                                              str(itemE.deprel) == "de_obj" or str(itemE.deprel) == "obj.cpl" or \
                                              str(itemE.deprel) == "p_obj" or str(itemE.deprel) == "de_objobj" or str(itemE.deprel) == "dep_cpd" or\
                    str(itemE.deprel)=="ats" or str(itemE.deprel)=="ato"  or str(itemE.deprel)=="aff"):
                    #dependencyList = self.existeItem(element,itemE,dependencyList)
                    dependencyList.append(itemE)
            elif itemE.head  == element.id and str(itemE.deprel) == "suj":
                dependencyList = self.searchSujetDependency(itemE,dependencyList)
            elif itemE.head  == element.id and str(itemE.deprel) == "mod" and int(itemE.id) > int(element.id):
                if len(self.dependencyAfterItem(element,sentenceConll))<=0:
                    dependencyList.append(itemE)
        return dependencyList

    def searchSujetDependency(self,item,depencyList):
        for it in depencyList:
            if str(it.deprel)==str(item.deprel):
                depencyList.remove(it)
                depencyList.append(item)
        return depencyList


    def dependencyAfterItem(self,element,sentenceConll):
        dependencyList = []
        for itemE in sentenceConll.sentence._elements:
            if itemE.head == element.id and int(itemE.id) > int(element.id)  and (
                    str(itemE.deprel) == "suj" or str(itemE.deprel) == "a_obj" or str(itemE.deprel) == "p_obj" \
                    or str(itemE.deprel) == "obj" or str(itemE.deprel) == "obj.p" or \
                    str(itemE.deprel) == "de_obj" or str(itemE.deprel) == "obj.cpl" or \
                    str(itemE.deprel) == "p_obj" or str(itemE.deprel) == "de_objobj" or str(itemE.deprel) == "dep_cpd" or \
                    str(itemE.deprel) == "ats" or str(itemE.deprel) == "ato" or str(itemE.deprel) == "aff"):
                dependencyList.append(itemE)
        return dependencyList



    #group verbal
        '''
            V: Verbes conjuges
            VINF: Verbes a l'infinitif
            VPR: Participles presents
            VPP: Participles passes
            VIMP: Verbes a l'imperatif
        '''
    def generateCCGTagForNodeTopDown(self, currentNode):

        #root.nodeInfo.label = "Sentence"
        #currentNode.nodeInfo.ccgTag.append(self.catTreeSingleNode("S"))
        if currentNode.hasLeftChild():
            self._ccgTagTopDown(currentNode.leftChild)
        if currentNode.hasRightChild():
            self._ccgTagTopDown(currentNode.rightChild)

        catTree = CategoryTree()
        if currentNode.hasRightChild():
            self.generateCCGTagForNodeBottomUp(currentNode.rightChild)
        if currentNode.hasLeftChild():
            self.generateCCGTagForNodeBottomUp(currentNode.leftChild)
        if currentNode.hasLeftChild() and currentNode.hasRightChild():
            leftNode = currentNode.leftChild
            rightNode = currentNode.rightChild
            parentNode = currentNode
            ccgRule = CCGRules()
            if leftNode.nodeInfo.ccgTag is None:
                leftNode.nodeInfo.ccgTag = []
            if rightNode.nodeInfo.ccgTag is None:
                rightNode.nodeInfo.ccgTag = []
            if parentNode.nodeInfo.ccgTag is None:
                parentNode.nodeInfo.ccgTag = []

            argLeft = leftNode.nodeInfo.ccgTag
            argRight = rightNode.nodeInfo.ccgTag
            resultTop = parentNode.nodeInfo.ccgTag

            if leftNode.nodeInfo.element is None:
                argLeft = self.addEquivalentCCG(leftNode.nodeInfo.ccgTag)
            if rightNode.nodeInfo.element is None:
                argRight = self.addEquivalentCCG(rightNode.nodeInfo.ccgTag)
            if parentNode.nodeInfo.element is None:
                resultTop = self.addEquivalentCCG(parentNode.nodeInfo.ccgTag)
            #print ("len: " + str(len(parentNode.nodeInfo.ccgTag)) + " - " + str(len(rightNode.nodeInfo.ccgTag)))

            if len(parentNode.nodeInfo.ccgTag) > 0 and len(rightNode.nodeInfo.ccgTag) > 0:
                for iArgRight in argRight:
                    for iResultTop in resultTop:
                        iArgRightCopy = copy.deepcopy(iArgRight)
                        iResultOpCopy = copy.deepcopy(iResultTop)
                        ccg = ccgRule.allRules(argRight=iArgRightCopy, resultTop=iResultOpCopy)
                        if ccg is not None and self.ccgExistCheck(leftNode.nodeInfo.ccgTag, ccg) == False:
                            leftNode.nodeInfo.ccgTag.append(ccg)

            elif len(leftNode.nodeInfo.ccgTag) > 0 and len(rightNode.nodeInfo.ccgTag) > 0:
                for iArgLeft in argLeft:
                    for iArgRight in argRight:
                        iArgLeftCopy = copy.deepcopy(iArgLeft)
                        iArgRightCopy = copy.deepcopy(iArgRight)
                        ccg = ccgRule.allRules(argLeft=iArgLeftCopy, argRight=iArgRightCopy)
                        if ccg is not None and self.ccgExistCheck(parentNode.nodeInfo.ccgTag, ccg) is False:
                            parentNode.nodeInfo.ccgTag.append(ccg)


                # self.updateTreeNode(parentNode, btree.root)
            elif len(parentNode.nodeInfo.ccgTag) > 0 and len(leftNode.nodeInfo.ccgTag) > 0:
                for iArgLeft in argLeft:
                    for iResultTop in resultTop:
                        iArgLeftCopy = copy.deepcopy(iArgLeft)
                        iResultTopCopy = copy.deepcopy(iResultTop)
                        ccg = ccgRule.allRules(argLeft=iArgLeftCopy, resultTop=iResultTopCopy)
                        if ccg is not None and self.ccgExistCheck(rightNode.nodeInfo.ccgTag, ccg) == False:
                            rightNode.nodeInfo.ccgTag.append(ccg)

    def _ccgTagTopDown(self,currentNode):
        #if str(currentNode.nodeInfo.dependency) == "mod":
            #currentNode.nodeInfo.ccgTag=[r"S/S"]
        #if str(currentNode.nodeInfo.dependency) == "suj" or re.match(r"obj",str(currentNode.nodeInfo.dependency)) or re.match(r"a_obj",str(currentNode.nodeInfo.dependency)) or re.match(r"p_obj",str(currentNode.nodeInfo.dependency)):
        #    npCCG = self.catTreeSingleNode("NP")
        #    if currentNode.nodeInfo.ccgTag is not None:
        #        print (str(currentNode.nodeInfo.ccgTag) + "   "+ str(npCCG) + "  " + str(self.ccgExistCheck(currentNode.nodeInfo.ccgTag,npCCG)))
        #        if self.ccgExistCheck(currentNode.nodeInfo.ccgTag,npCCG) is False:
        #            currentNode.nodeInfo.ccgTag.append(npCCG)
        if currentNode.hasLeftChild():
            self._ccgTagTopDown(currentNode.leftChild)
        if currentNode.hasRightChild():
            self._ccgTagTopDown(currentNode.rightChild)

    def addEquivalentCCG(self,ccgTagList):
        #NP == S/(S\NP)
        key =  1
        rootNode = CategoryTreeNode(key, "/")
        childTree = self.catfullTreeNodeWithLabelInput ("\\", "S", "NP")
        leftNodeChild = CategoryTreeNode(childTree.size + 2,"S")
        catTreeTypeRaising = self.catfullTreeNodeWithNodeInput(rootNode, leftNodeChild, childTree.root)

        #NP == (S\NP)/((S\NP)/NP)
        key = 1
        rootNode = CategoryTreeNode(key, "/")
        leftChildTree = self.catfullTreeNodeWithLabelInput("\\","S","NP")
        rightRootNode = CategoryTreeNode(key, "/")
        rightchildleftTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        rightRightNodeChild = CategoryTreeNode(childTree.size + 2, "S")
        rightChildTree = self.catfullTreeNodeWithNodeInput(rightRootNode, rightchildleftTree.root, rightRightNodeChild)
        catTreeTypeRaisingSandNP = self.catfullTreeNodeWithNodeInput(rootNode,leftChildTree.root,rightChildTree.root)
        #S\NP == NP\NP
        sbnp = self.catfullTreeNodeWithLabelInput("\\","S","NP")
        npnp = self.catfullTreeNodeWithLabelInput("\\","NP","NP")
        #S/NP == NP\NP
        sfnp = self.catfullTreeNodeWithLabelInput("/", "S", "NP")
        #S\NP == S\S
        sbs = self.catfullTreeNodeWithLabelInput("\\", "S", "S")
        npCCG = self.catTreeSingleNode("NP")
        if self.ccgExistCheck(ccgTagList,npCCG) is True:
            if self.ccgExistCheck(ccgTagList,catTreeTypeRaising) is False:
                ccgTagList.append(catTreeTypeRaising)
            if self.ccgExistCheck(ccgTagList,catTreeTypeRaisingSandNP) is False:
                ccgTagList.append(catTreeTypeRaisingSandNP)
        if self.ccgExistCheck(ccgTagList,npnp) is True:
            if self.ccgExistCheck(ccgTagList, sbnp) is False:
                ccgTagList.append(sbnp)
            if self.ccgExistCheck(ccgTagList, sfnp) is False:
                ccgTagList.append(sfnp)
        if self.ccgExistCheck(ccgTagList,sfnp) is True:
            if self.ccgExistCheck(ccgTagList,npnp) is False:
                ccgTagList.append(npnp)
        if self.ccgExistCheck(ccgTagList,sbnp) is True:
            if self.ccgExistCheck(ccgTagList,npnp) is False:
                ccgTagList.append(npnp)
        if self.ccgExistCheck(ccgTagList,sbnp) is True:
            if self.ccgExistCheck(ccgTagList,sbs) is False:
                ccgTagList.append(sbs)
        if self.ccgExistCheck(ccgTagList,sbs) is True:
            if self.ccgExistCheck(ccgTagList,sbnp) is False:
                ccgTagList.append(sbnp)
        np = self.catTreeSingleNode("NP")
        if self.ccgExistCheck(ccgTagList,catTreeTypeRaising) is True:
            if self.ccgExistCheck(ccgTagList,np) is False:
                ccgTagList.append(np)
        return ccgTagList


    def catTreeSingleNode(self,categoryLabel,key=None):
        catTree = CategoryTree()
        if key is None:
            key = 1
        rootNode= CategoryTreeNode(key, categoryLabel)
        catTree.buildTree(rootNode)
        return catTree
    def catfullTreeNodeWithLabelInput(self,topLabel,leftLabel,rightLabel):
        catTree = CategoryTree()
        key = catTree.size + 1
        topNode = CategoryTreeNode(key, topLabel)
        key +=1
        leftNode = CategoryTreeNode(key, leftLabel)
        key +=1
        rightNode = CategoryTreeNode(key,rightLabel)
        catTree.buildTree(topNode,nodeLeft=leftNode, nodeRight=rightNode)
        return catTree
    def catfullTreeNodeWithNodeInput(self,top,left,right):
        catTree = CategoryTree()
        catTree.buildTree(top,nodeLeft=left, nodeRight=right)
        return catTree

    def ccgTagForElement(self, element, sentenceInConll,dtree,position=None):
        #for verbal group
        ccgTag = []
        if element is not None:
            if str(element.xpostag) == "PONCT":
                ccgTag =self.assigneXpostagPontc(element, sentenceInConll,position)
            elif str(element.xpostag) == "CC":
                ccgTag = self.assigneXpostagConj(element, sentenceInConll, position)
                #ccgTag.append(self.catTreeSingleNode("conj"))
            elif str(element.xpostag) == "VPP":
                ccgTag=self.assigeXpostagVPP(element, sentenceInConll)
            elif str(element.xpostag) == "V" or str(element.xpostag) == "VINF" or str(element.xpostag) == "VPR":
               ccgTag.append(self.assigeXpostagV(element,sentenceInConll))
            elif str(element.xpostag) == "VIMP":
                ccgTag.append(self.assigeXpostagVIMP(element, sentenceInConll))
            elif str(element.xpostag) == "VS":
                ccgTag = self.assigeXpostagVS(element, sentenceInConll)
            #Article is alway putting before noun in the sentence
            elif str(element.xpostag) == "DET":
                ccgTag.append(self.catfullTreeNodeWithLabelInput("/","NP","NP"))
            #In french, adj can be put before or after noun
            elif str(element.xpostag) == "ADJ":
                ccgTag=self.assigneXpostagADJ(element, sentenceInConll)
            elif str(element.xpostag) == "P+D":
                ccgTag=self.assigneXpostagPD(element,sentenceInConll)
            elif str(element.xpostag) == "P":
                ccgTag=self.assigneXpostagP(element,sentenceInConll)
            elif str(element.xpostag) == "ET":
                ccgTag = self.assigneXpostagP(element, sentenceInConll)
            elif str(element.xpostag) == "PRO":
                ccgTag = self.assigeXpostagPRO(element, sentenceInConll)
            elif  str(element.xpostag) == "CLS":
                ccgTag.append(self.catTreeSingleNode("NP"))
            elif str(element.xpostag) == "CLO":
                ccgTag = self.assigeXpostagCLO(element, sentenceInConll)
            elif str(element.xpostag) == "NC":
                ccgTag = self.assigeXpostagNC(element,sentenceInConll)
            elif str(element.xpostag) == "CS":
                ccgTag = self.assigeXpostagCS(element, sentenceInConll)
            elif str(element.xpostag) == "CLR":
                ccgTag = self.assigneXpostagCLR(element,sentenceInConll)
            elif str(element.xpostag) == "NPP":
                ccgTag = self.assigneXpostagNPP(element,sentenceInConll,position)
            elif str(element.xpostag) == "ADV":
                #ccgTag.append(r"(S\NP)\(S\NP)")
                ccgTag = self.assigneXpostagADV(element,sentenceInConll,position)
            elif str(element.xpostag) == "PROWH":
                catChildTree  = self.catfullTreeNodeWithLabelInput("/","S","NP")
                key = catChildTree.size + 1
                catTreeNodeTop = CategoryTreeNode(key,"/")
                key +=1
                catTreeNodeLeft = CategoryTreeNode(key,"S",underscript="wq")
                catTreeNodeRight = catChildTree.root
                ccgTag.append(self.catfullTreeNodeWithNodeInput(catTreeNodeTop,catTreeNodeLeft,catTreeNodeRight))
                ccgTag.append(self.catTreeSingleNode("NP"))
                #ccgTag.append(r"S[wq]/(S/NP)")
            elif str(element.xpostag) == "PROREL":
                ccgTag = self.assigneXpostagPROREL(element,sentenceInConll)
            elif str(element.xpostag) == "ADJWH":
                ccgTag = self.assigneXpostagADJWH(element, sentenceInConll)
            elif str(element.xpostag) == "ADVWH":
                ccgTag = self.assigneXpostagADVWH(element, sentenceInConll)
            elif str(element.xpostag) == "DETWH":
                ccgTag = self.assigneXpostagDETWH(element, sentenceInConll)

            elif str(element.xpostag) == "PREF":
                ccgTag = self.assigneXpostagPREF(element, sentenceInConll)
            elif str(element.xpostag) == "I":
                ccgTag.append(self.catTreeSingleNode("NP"))
        return ccgTag

    # category for Xpostag
    def assigneXpostagDETWH(self, element, sentenceInConll):
        ccg=[]
        catRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catRight.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catChildTree = CategoryTreeNode(key, "S",underscript=element.form)
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree, catRight.root))
        # ccg = r"(S/(S\NP)"

        ccg = []
        ccg.append( self.catfullTreeNodeWithLabelInput("/", "S", "NP"))
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))

        return ccg

    def assigneXpostagADJWH(self, element, sentenceInConll):
        ccg=[]
        catRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catRight.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catChildTree = CategoryTreeNode(key, "S",underscript=element.form)
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree, catRight.root))
        # ccg = r"(Squel/(S\NP)"

        return ccg
    def assigneXpostagADVWH(self, element, sentenceInConll):
        ccg=[]
        catRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catRight.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catChildTree = CategoryTreeNode(key, "S",underscript=element.form)
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree, catRight.root))
        # ccg = r"(Squel/(S\NP)"
        catRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catRight.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catrootChild = CategoryTreeNode(key, "\\")
        key += 1
        catrootleft = CategoryTreeNode(key, "S")#, underscript=element.form
        key += 1
        catrootRight = CategoryTreeNode(key, "NP")
        catLeft = self.catfullTreeNodeWithNodeInput(catrootChild,catrootleft,catrootRight)
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catLeft.root, catRight.root))
        # ccg = r"(Squel\NP)/(S\NP)"
        return ccg

    def assigneXpostagPROREL(self, element, sentenceInConll):
        ccg=[]
        if element.deprel=="suj":
            ccg.append(self.catTreeSingleNode("NP"))

        catTree1 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTree2 = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root))
        #ccg=r"(NP\NP)/(S\NP)"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP\NP)/NP"
        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "S")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP\NP)/S"
        return ccg

    def assigneXpostagPontc(self, element, sentenceInConll, position):
        ccg = []
        ccg.append(self.catTreeSingleNode("ponct"))
        if element.form==",":
            catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
            key = catChildTree.size + 1
            catTop = CategoryTreeNode(key, "/")
            key += 1
            catRight = CategoryTreeNode(key, "NP")
            ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
            # ccg = r"(NP\NP)/NP"
            ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
            ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))
            ccg.append(self.catTreeSingleNode("NP"))
        return ccg

    def assigneXpostagConj(self, element, sentenceInConll, position=None):

        ccg = []
        ccg.append(self.catTreeSingleNode("conj"))
        for item in self.assigneXpostagPontc(element,sentenceInConll, position):
            ccg.append(item)
        return ccg

    def assigeXpostagNC(self,element,sentenceInConll):
        ccg = []
        ccg.append(self.catTreeSingleNode("NP"))
        nextElementInArray = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
        prevElementInArray=None
        if int(element.id)>0:
            prevElementInArray = self.getElementWithId(int(element.id) - 1, sentenceInConll.sentence._elements)
        if prevElementInArray is not None and (prevElementInArray.xpostag=="NC" or \
                                               prevElementInArray.xpostag == "DET" or \
                                               prevElementInArray.form == "-"):
            ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
            ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))
        if nextElementInArray is not None and nextElementInArray.form=="\"":
            ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        return ccg

    def assigeXpostagCLO(self,element,sentenceInConll):
        ccg = []
        ccg.append(self.catTreeSingleNode("NP"))

        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))

        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))

        catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catleftChildTree.size + catRightChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root))
        # ccg = r"(S\NP)/(S\NP)"
        return ccg

    def assigeXpostagCS(self,element,sentenceInConll):
        ccg = []
        ccg.append(self.catTreeSingleNode("NP"))
        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))
        # ccg = "NP\\NP
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        # ccg = "NP/NP
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        #ccg = r"(S\NP)/(S\NP)"
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        #ccg = "NP/NP
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catTreeSingleNode("NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        #ccg = "r(S\NP)/NP
        return ccg

    def assigeXpostagPRO(self, element, sentenceInConll, position=None):
        ccg=[]

        ccg.append(self.catTreeSingleNode("NP"))
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP\NP)/NP"
        return ccg


    def assigneXpostagNPP(self, element, sentenceInConll, position):
        ccg=[]
        ccg.append(self.catTreeSingleNode("NP"))
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP\NP)/NP"


        return ccg

    def assigneXpostagCLR(self,element,sentenceInConll):
        ccg = []

        ccg.append(self.catTreeSingleNode("NP"))

        catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catleftChildTree.size + catRightChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root))
        # ccg = r"(S\NP)/(S\NP)"

        catleftChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "NP")
        catRightChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "NP")
        key = catleftChildTree.size + catRightChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root))
        # ccg = r"(S/NP)/(S/NP)"

        return ccg

    def assigneXpostagADJ(self,element,sentenceInConll):
        ccg = []
        #ccg = r"NP/NP"
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        #ccg = r"NP\NP"
        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))
        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP\NP)/NP"

        return ccg

    def assigneXpostagP(self,element,sentenceInConll):
        ccg=[]
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        # ccg = "NP/NP"

        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))
        # ccg = "NP\NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(S\NP)/NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "S")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "\\")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # (S/S)\\NP

        catChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "S")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # (S/S)/NP

        catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catleftChildTree.size + catRightChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root))
        # ccg = r"(S\NP)/(S\NP)"

        catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catleftChildTree.size + catRightChildTree.size + 1
        catTop = CategoryTreeNode(key, "\\")
        key += 1
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root))
        # ccg = r"(S\NP)\(S\NP)"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "\\")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP\NP)\NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "\\")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        newChilLeftChild = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
        newTopChild = CategoryTreeNode(key, "/")
        key += 1
        newCatRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(newTopChild,newChilLeftChild.root,newCatRight))
        # ccg = r"((NP\NP)\NP)/NP"
        catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catleftChildTree.size + catRightChildTree.size + 1
        catTop = CategoryTreeNode(key, "\\")
        key += 1
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root))
        # ccg = r"(NP\NP)\(NP\NP)"

        catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catleftChildTree.size + catRightChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root))
        # ccg = r"(NP\NP)\(NP\NP)"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\","NP","NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key,"/")
        key +=1
        catRight = CategoryTreeNode(key,"NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop,catChildTree.root,catRight))
        #ccg = r"(NP\NP)/NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "\\")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        newChilLeftChild = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
        newTopChild = CategoryTreeNode(key, "\\")
        key += 1
        newCatRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(newTopChild, newChilLeftChild.root, newCatRight))
        # ccg = r"((NP\NP)\NP)\NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP/NP)/NP"


        return ccg

    def assigneXpostagPD(self,element,sentenceInConll):
        ccg = []
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        # ccg = "NP/NP"



        catChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "S")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = "(S/S)/NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP\NP)/NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(S\NP)/NP"



        return ccg

    def assigeXpostagVPP(self,element,sentenceInConll):
        ccg = []
        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))

        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
                    #ccg = r"(S\NP)/(S\NP)"
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "\\")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        # ccg = r"(S\NP)\(S\NP)"
        catTreeLeft = self.catfullTreeNodeWithLabelInput("/", "S", "NP")
        catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "\\")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        # ccg = r"(S/NP)\(S\NP)"
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")

        catTreeLeftRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRightRight = self.catTreeSingleNode("NP")
        catTopNodeRight = CategoryTreeNode(catTreeLeft.size + catTreeLeftRight.size +catTreeRightRight.size + 1, "/")
        catTreeRight = self.catfullTreeNodeWithNodeInput(catTopNodeRight, catTreeLeftRight.root, catTreeRightRight.root)

        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "\\")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode,  catTreeRight.root,catTreeLeft.root))

        # ccg = r"(S/NP)\((S\NP)/NP)"
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))

        #ccg = "r(S\NP)/NP"
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catTreeSingleNode("NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "\\")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        #ccg = "r(S\NP)/NP
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catTreeSingleNode("NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        # ccg = "r((S\NP)/NP)/NP
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catTreeSingleNode("NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
        catTree = self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root)#ccg = "r(S\NP)/NP
        catTreeRight2 = self.catTreeSingleNode("NP")
        catTopNode2 = CategoryTreeNode(catTree.size + catTreeRight2.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode2,catTree.root,catTreeRight2.root))


        return ccg

    def assigeXpostagVS(self,element,sentenceInConll):
        ccg = []
        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))

        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        #ccg = r"(S\NP)/(S\NP)"
        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))

        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "\\")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        # ccg = r"(S\NP)\(S\NP)"
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        # ccg = r"NP/NP"
        #ccg = "r(S\NP)/NP
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catTreeSingleNode("NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root))
        # ccg = "r((S\NP)/NP)/NP
        catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTreeRight = self.catTreeSingleNode("NP")
        catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
        catTree = self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root)#ccg = "r(S\NP)/NP
        catTreeRight2 = self.catTreeSingleNode("NP")
        catTopNode2 = CategoryTreeNode(catTree.size + catTreeRight2.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode2,catTree.root,catTreeRight2.root))
        return ccg

    def assigeXpostagVIMP(self,element,sentenceInConll):
        dependencyList = self.searchDependencyWithVerb(element, sentenceInConll)
        ccg = None
        #consider for the group verb
        if int(element.id) <= len(sentenceInConll.sentence._elements):
                catTree = CategoryTree()
                catChildTree = self.catTreeSingleNode("S")
                key = catChildTree.size + 1
                for itemD in dependencyList:
                    if int(itemD.id) > int(element.id):
                        if itemD.upostag=="V":
                            topNode = CategoryTreeNode(key, "/")
                            key += 1
                            rightTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                            catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root,
                                                                                     rightTree.root)
                            key+=1
                        else:
                            key+=1
                            topNode = CategoryTreeNode(key,"/")
                            key+=1
                            rightNode = CategoryTreeNode(key,"NP")
                            catChildTree = self.catfullTreeNodeWithNodeInput(topNode,catChildTree.root,rightNode)
                            key+=1
                            #ccg = r"(" + ccg
                            #ccg += r")/NP"
                    else:
                        if itemD.upostag == "V":
                            topNode = CategoryTreeNode(key, "/")
                            key += 1
                            rightTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                            catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root,
                                                                                     rightTree.root)
                            key += 1
                        else:
                            key += 1
                            topNode = CategoryTreeNode(key, "\\")
                            key += 1
                            rightNode = CategoryTreeNode(key, "NP")
                            catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root, rightNode)
                            key += 1
                            # ccg = r"(" + ccg
                            # ccg += r")/NP"
                ccg = catChildTree
        return ccg

    def assigeXpostagV(self,element,sentenceInConll):
        dependencyList = self.searchDependencyWithVerb(element, sentenceInConll)
        ccg = None
        #consider for the group verb
        if int(element.id) <= len(sentenceInConll.sentence._elements):
            nextElementInArray = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
            prevElementInArray = self.getElementWithId(int(element.id) - 1, sentenceInConll.sentence._elements)
            elementNext = self.getElementWithId(element.head, sentenceInConll.sentence._elements)
            if nextElementInArray is not None and (str(nextElementInArray.xpostag) == "V" or str(nextElementInArray.xpostag) == "VINF" or str(nextElementInArray.xpostag) == "VPR" or str(nextElementInArray.xpostag) == "VPP" or str(nextElementInArray.xpostag) == "VIMP" or str(nextElementInArray.xpostag) == "ADV"):
                catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
                ccg = self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root)
            elif nextElementInArray is not None and int(element.id) < int(element.head) and (str(nextElementInArray.xpostag) == "V" or str(nextElementInArray.xpostag) == "VINF" or str(nextElementInArray.xpostag) == "VPR" or str(nextElementInArray.xpostag) == "VPP" or str(nextElementInArray.xpostag) == "VIMP" or str(nextElementInArray.xpostag) == "ADV"):
                # before verb
                catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
                ccg = self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root)
                #ccg = r"(S\NP)/(S\NP)"
            else:
                #cas question with verb + sujet ex: Quel est le principal objectif de Gorbatchev en matière de politique étrangère ?
                getsuj =None
                for item in dependencyList:
                    if str(item.deprel)=="suj":
                        getsuj=item
                if getsuj is not None:
                    catTree = CategoryTree()
                    catChildTree = self.catTreeSingleNode("S")
                    key = catChildTree.size + 1
                    for itemD in dependencyList:
                        if int(itemD.id) > int(element.id):
                            if itemD.upostag=="V":
                                topNode = CategoryTreeNode(key, "/")
                                key += 1
                                rightTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                                catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root,
                                                                                     rightTree.root)
                                key+=1
                            else:
                                key+=1
                                topNode = CategoryTreeNode(key,"/")
                                key+=1
                                rightNode = CategoryTreeNode(key,"NP")
                                catChildTree = self.catfullTreeNodeWithNodeInput(topNode,catChildTree.root,rightNode)
                                key+=1
                                #ccg = r"(" + ccg
                                    #ccg += r")/NP"
                        else:
                            if itemD.upostag == "V":
                                topNode = CategoryTreeNode(key, "/")
                                key += 1
                                rightTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                                catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root,
                                                                                     rightTree.root)
                                key += 1
                            else:
                                key += 1
                                topNode = CategoryTreeNode(key, "\\")
                                key += 1
                                rightNode = CategoryTreeNode(key, "NP")
                                catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root, rightNode)
                                key += 1
                                # ccg = r"(" + ccg
                                # ccg += r")/NP"
                else:
                    catTree = CategoryTree()
                    catChildTree = self.catfullTreeNodeWithLabelInput("\\","S","NP")
                    #ccg = r"S\NP"
                    key = catChildTree.size+1
                    for itemD in dependencyList:
                        if re.match(r"obj", str(itemD.deprel)) or re.match(r"dep_cpd", str(itemD.deprel))  or \
                                re.match(r"de_obj", str(itemD.deprel)) or \
                                re.match(r"a_obj", str(itemD.deprel)) or re.match(r"p_obj", str(itemD.deprel)) or str(itemD.deprel) == "ats":
                            if int(itemD.id) > int(element.id):
                                if itemD.upostag=="V":
                                    topNode = CategoryTreeNode(key, "/")
                                    key += 1
                                    rightTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                                    catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root,
                                                                                     rightTree.root)
                                    key+=1
                                else:
                                    key+=1
                                    topNode = CategoryTreeNode(key,"/")
                                    key+=1
                                    rightNode = CategoryTreeNode(key,"NP")
                                    catChildTree = self.catfullTreeNodeWithNodeInput(topNode,catChildTree.root,rightNode)
                                    key+=1
                                    #ccg = r"(" + ccg
                                    #ccg += r")/NP"
                            else:
                                if itemD.upostag == "V":
                                    topNode = CategoryTreeNode(key, "/")
                                    key += 1
                                    rightTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                                    catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root,
                                                                                     rightTree.root)
                                    key += 1
                                else:
                                    key += 1
                                    topNode = CategoryTreeNode(key, "\\")
                                    key += 1
                                    rightNode = CategoryTreeNode(key, "NP")
                                    catChildTree = self.catfullTreeNodeWithNodeInput(topNode, catChildTree.root, rightNode)
                                    key += 1
                                    # ccg = r"(" + ccg
                                    # ccg += r")/NP"
                        elif str(itemD.deprel) == "mod" and int(itemD.id) > int(element.id):
                            #ccg = r"(" + ccg
                            topNode = CategoryTreeNode(key, "/")
                            key += 1
                            rightTree = self.catfullTreeNodeWithLabelInput("\\","S","NP")
                            catChildTree = self.catfullTreeNodeWithNodeInput(topNode,catChildTree.root,rightTree.root)
                            #ccg += r")/(S\NP)"
                ccg = catChildTree
        return ccg

    def assigneXpostagADV(self, element, sentenceInConll, position):
        ccg = []
        catTree1 = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        catTree2 = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root))

        # before verb
        catTree1 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTree2 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root))
        # ccg = r"(S\NP)/(S\NP)"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(S\NP)/NP"

        catTree1 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTree2 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "\\")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root))
        # ccg = r"(S\NP)\(S\NP)"

        ccg.append(self.catfullTreeNodeWithLabelInput("\\","NP","NP"))
        # ccg = r"NP\NP"
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        # ccg = r"NP)/NP"
        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "S", "NP"))
        # ccg = r"(S\NP)"
        return ccg

    def assigneXpostagPREF(self, element, sentenceInConll):
        ccg = []

        ccg.append(self.catfullTreeNodeWithLabelInput("\\","NP","NP"))
        #ccg = NP//NP
        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        # ccg = NP\NP
        catTree1 = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        catTree2 = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root))
        # ccg = (NP\NP)/(NP\NP)
        # before verb
        catTree1 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTree2 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "/")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root))
        # ccg = r"(S\NP)/(S\NP)"

        catTree1 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTree2 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "\\")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root))
        # ccg = r"(S\NP)\(S\NP)"

        return ccg
    # Etranger
    def assigneXpostagET(self, element, sentenceInConll):
        ccg = []
        ccg.append(self.catTreeSingleNode("NP"))

        ccg.append(self.catfullTreeNodeWithLabelInput("/", "NP", "NP"))
        # ccg = "NP/NP"

        ccg.append(self.catfullTreeNodeWithLabelInput("\\", "NP", "NP"))
        # ccg = "NP\NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "S")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = (S/S)/NP

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(S\NP)/NP"

        catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
        key = catleftChildTree.size + catRightChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root))
        # ccg = r"(S\NP)/(S\NP)"

        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP\NP)/NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))
        # ccg = r"(NP/NP)/NP"

        catChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "S")
        key = catChildTree.size + 1
        catTop = CategoryTreeNode(key, "/")
        key += 1
        catRight = CategoryTreeNode(key, "NP")
        ccg.append(self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight))


        return ccg

    #def addParenthesis(self,category):

    def countCharacter(self,category,character):
        return category.count(character)

    def getElementWithId(self,elementID,chunk):
        for item in chunk:
            if int(item.id) == int(elementID):
                return item
        return None
    def getElementListByHead(self, elementID, chunk):
        result = []
        for item in chunk:
            if int(item.head) == int(elementID):
                result.append(item)
        return result

    r'''
    def assigeXpostagVPP22(self,element,sentenceInConll):
        dependencyList = self.searchDependencyWithVerb(element, sentenceInConll)
        ccg = None
        #consider for the group verb
        if int(element.id) <= len(sentenceInConll.sentence._elements):
            elementNext = self.getElementWithId(element.head, sentenceInConll.sentence._elements)
            nextElementInArray = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
            prevElementInArray = None
            if int(element.id)>0:
                prevElementInArray = self.getElementWithId(int(element.id) - 1, sentenceInConll.sentence._elements)
            #elementParent = self.getElementListByHead(element.head, sentenceInConll.sentence._elements)
            # before verb
            if int(element.id) < int(element.head) and (str(elementNext.xpostag) == "V" or str(elementNext.xpostag) == "VINF" or str(elementNext.xpostag) == "VPR" or str(elementNext.xpostag) == "VPP" or str(elementNext.xpostag) == "VIMP"):

                if prevElementInArray is not None and (str(prevElementInArray.xpostag) == "NC" or str(prevElementInArray.xpostag) == "ADV"):# les réfugies reparties
                    ccg = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                else:
                    catTreeLeft = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                    catTreeRight = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                    catTopNode = CategoryTreeNode(catTreeLeft.size + catTreeRight.size + 1, "/")
                    ccg = self.catfullTreeNodeWithNodeInput(catTopNode, catTreeLeft.root, catTreeRight.root)
                    #ccg = r"(S\NP)/(S\NP)"
            else:# after verb
                if prevElementInArray is not None and (str(prevElementInArray.xpostag) == "NC" or str(prevElementInArray.xpostag) == "ADV"):# les réfugies reparties
                    ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
                else:
                    catTree = CategoryTree()
                    catChildTree = self.catfullTreeNodeWithLabelInput("\\","S","NP")
                    #ccg = r"S\NP"
                    key = catChildTree.size+1
                    for itemD in dependencyList:
                        if re.match(r"obj", str(itemD.deprel)) or re.match(r"a_obj", str(itemD.deprel)) or re.match(r"p_obj", str(itemD.deprel)) or str(itemD.deprel) == "ats":
                            topNode = CategoryTreeNode(key,"/")
                            key+=1
                            rightNode = CategoryTreeNode(key,"NP")
                            key+=1
                            catChildTree = self.catfullTreeNodeWithNodeInput(topNode,catChildTree.root,rightNode)
                            key+=1
                            #ccg = r"(" + ccg
                            #ccg += r")/NP"
                        elif str(itemD.deprel) == "mod":
                            #ccg = r"(" + ccg
                            topNode = CategoryTreeNode(key, "/")
                            key += 1
                            rightTree = self.catfullTreeNodeWithLabelInput("\\","S","NP")
                            catChildTree = self.catfullTreeNodeWithNodeInput(topNode,catChildTree.root,rightTree.root)
                            #ccg += r")/(S\NP)"
                    ccg = catChildTree
        return ccg

    def assigneXpostagADV2(self, element,sentenceInConll,position):
        ccg = None
        if int(element.id) <= len(sentenceInConll.sentence._elements):
            elementNext = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
            nextElementInArray = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
            prevElementInArray = None
            if int(element.id)>0:
                prevElementInArray = self.getElementWithId(int(element.id) - 1, sentenceInConll.sentence._elements)
            if int(element.id)<int(element.head):
                #before adj
                if str(elementNext.xpostag) == "ADJ" or str(elementNext.xpostag)=="VPP":
                    catTree1 = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                    catTree2 = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                    catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "/")
                    ccg = self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root)

                #before verb
                else:
                    catTree1 = self.catfullTreeNodeWithLabelInput("\\","S","NP")
                    catTree2 = self.catfullTreeNodeWithLabelInput("\\","S","NP")
                    catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "/")
                    ccg = self.catfullTreeNodeWithNodeInput(catTopNode,catTree2.root,catTree1.root)
                #ccg = r"(S\NP)/(S\NP)"
            else:
                #after verb

                if position == 1:
                    catTree1 = self.catfullTreeNodeWithLabelInput("\\","S","NP")
                    catTree2 = self.catfullTreeNodeWithLabelInput("\\","S","NP")
                    catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "\\")
                    ccg = self.catfullTreeNodeWithNodeInput(catTopNode,catTree2.root,catTree1.root)
                else:
                    catTree1 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                    catTree2 = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                    catTopNode = CategoryTreeNode(catTree1.size + catTree2.size + 1, "/")
                    ccg = self.catfullTreeNodeWithNodeInput(catTopNode, catTree2.root, catTree1.root)
                #ccg =  r"(S\NP)\(S\NP)"
        return ccg

    def assigneXpostagPD2(self, element, sentenceInConll):
        ccg = None
        if int(element.id) < len(sentenceInConll.sentence._elements):
            elementPrev = self.getElementWithId(element.head, sentenceInConll.sentence._elements)
            elist = self.getElementListByHead(element.id, sentenceInConll.sentence._elements)
            if len(elist) == 1:
                elementNext = elist[0]
                if (
                        elementPrev.xpostag == "NC" or elementPrev.xpostag == "NPP" or elementPrev.xpostag == "CLS" or elementPrev.xpostag == "CLO") and (
                        elementNext.xpostag == "NC" or elementNext.xpostag == "NPP" or elementNext.xpostag == "CLS" or elementNext.xpostag == "CLO"):
                    catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                    key = catChildTree.size + 1
                    catTop = CategoryTreeNode(key, "/")
                    key += 1
                    catRight = CategoryTreeNode(key, "NP")
                    ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                    # ccg = r"(NP\NP)/NP"
                elif (
                        elementPrev.xpostag == "VPR" or elementPrev.xpostag == "VPP" or elementPrev.xpostag == "V" or elementPrev.xpostag == "VINF" or elementPrev.xpostag == "VIMP") and (
                        elementNext.xpostag == "NC" or elementNext.xpostag == "NPP" or elementNext.xpostag == "CLS" or elementNext.xpostag == "CLO"):
                    if int(element.id) > int(elementPrev.id):
                        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                        key = catChildTree.size + 1
                        catTop = CategoryTreeNode(key, "/")
                        key += 1
                        catRight = CategoryTreeNode(key, "NP")
                        ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                        # ccg = r"(S\NP)/NP"
                    else:
                        catChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "S")
                        key = catChildTree.size + 1
                        catTop = CategoryTreeNode(key, "/")
                        key += 1
                        catRight = CategoryTreeNode(key, "NP")
                        ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                        # ccg = "(S/S)/NP"
                # condition1 = str(elementNext.xpostag) == "V" or str(elementNext.xpostag) == "VINF" or str(
                #    elementNext.xpostag) == "VPR" or str(elementNext.xpostag) == "VPP" or str(
                #    elementNext.xpostag) == "VIMP"
                # condition2 = str(elementPrev.xpostag) == "V" or str(elementPrev.xpostag) == "VINF" or str(
                #    elementPrev.xpostag) == "VPR" or str(elementPrev.xpostag) == "VPP" or str(
                #    elementPrev.xpostag) == "VIMP"
                # if condition1 and condition2:
                #    ccg = r"(S\NP)/(S\NP)"
            elif len(elist) == 0:
                elementNext = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
                if (
                        elementPrev.xpostag == "NC" or elementPrev.xpostag == "NPP" or elementPrev.xpostag == "CLS" or elementPrev.xpostag == "CLO") and (
                        elementNext.xpostag == "NC" or elementNext.xpostag == "NPP" or elementNext.xpostag == "CLS" or elementNext.xpostag == "CLO"):
                    catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                    key = catChildTree.size + 1
                    catTop = CategoryTreeNode(key, "/")
                    key += 1
                    catRight = CategoryTreeNode(key, "NP")
                    ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                    # ccg = r"(NP\NP)/NP"
            else:
                ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
                # ccg = "NP/NP"
        return ccg

    def assigneXpostagP2(self,element,sentenceInConll):
        ccg=None
        if int(element.id) < len(sentenceInConll.sentence._elements):
            nextElementInArray = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
            prevElementInArray = None
            if int(element.id)>0:
                prevElementInArray = self.getElementWithId(int(element.id) - 1, sentenceInConll.sentence._elements)
            elementPrev = self.getElementWithId(element.head, sentenceInConll.sentence._elements)
            elist = self.getElementListByHead(element.id, sentenceInConll.sentence._elements)

            if len(elist)==1:
                elementNext = elist[0]
                if elementNext.xpostag == "VPR" or elementNext.xpostag =="VINF":#en(P) atendant (VPR), d'(P) avoir(VINF)
                    catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")

                    catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                    key = catleftChildTree.size + catRightChildTree.size + 1
                    catTop = CategoryTreeNode(key, "/")
                    key += 1
                    ccg = self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root)
                    # ccg = r"(S\NP)/(S\NP)"
                if elementNext.xpostag=="NC" or nextElementInArray.xpostag=="PRO": #d'enfants
                    ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")

                if (elementPrev.xpostag == "NC" or elementPrev.xpostag == "NPP" or elementPrev.xpostag == "CLS" or elementPrev.xpostag == "CLO") and ( elementNext.xpostag == "NC" or elementNext.xpostag == "NPP" or elementNext.xpostag == "CLS" or elementNext.xpostag == "CLO"):
                    catChildTree = self.catfullTreeNodeWithLabelInput("\\","NP","NP")
                    key = catChildTree.size + 1
                    catTop = CategoryTreeNode(key,"/")
                    key +=1
                    catRight = CategoryTreeNode(key,"NP")
                    ccg = self.catfullTreeNodeWithNodeInput(catTop,catChildTree.root,catRight)
                    #ccg = r"(NP\NP)/NP"
                elif (elementPrev.xpostag == "V" or elementPrev.xpostag == "VINF" or elementPrev.xpostag == "VIMP") and (elementNext.xpostag == "NC" or elementNext.xpostag == "NPP" or elementNext.xpostag == "CLS" or elementNext.xpostag == "CLO"):
                    if int(element.id)>int(elementPrev.id):
                        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                        key = catChildTree.size + 1
                        catTop = CategoryTreeNode(key, "/")
                        key += 1
                        catRight = CategoryTreeNode(key, "NP")
                        ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                        #ccg = r"(S\NP)/NP"
                    else:
                        catChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "S")
                        key = catChildTree.size + 1
                        catTop = CategoryTreeNode(key, "/")
                        key += 1
                        catRight = CategoryTreeNode(key, "NP")
                        ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                elif (elementPrev.xpostag == "VPP" or elementPrev.xpostag == "VINF") and (elementNext.xpostag == "DET" or elementNext.xpostag == "NC" or elementNext.xpostag == "NPP" or elementNext.xpostag == "CLS" or elementNext.xpostag == "CLO"):
                    if int(element.id)>int(elementPrev.id):
                        catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                        key = catChildTree.size + 1
                        catTop = CategoryTreeNode(key, "/")
                        key += 1
                        catRight = CategoryTreeNode(key, "NP")
                        ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                        #ccg = r"(NP\NP)/NP"
                    else:
                        catChildTree = self.catfullTreeNodeWithLabelInput("/", "S", "S")
                        key = catChildTree.size + 1
                        catTop = CategoryTreeNode(key, "/")
                        key += 1
                        catRight = CategoryTreeNode(key, "NP")
                        ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
            elif len(elist)==0:
                elementNext= self.getElementWithId(int(element.id)+1, sentenceInConll.sentence._elements)
                if (
                        elementPrev.xpostag == "NC" or elementPrev.xpostag == "NPP" or elementPrev.xpostag == "CLS" or elementPrev.xpostag == "CLO") and (
                        elementNext.xpostag == "NC" or elementNext.xpostag == "NPP" or elementNext.xpostag == "CLS" or elementNext.xpostag == "CLO" ):
                    catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                    key = catChildTree.size + 1
                    catTop = CategoryTreeNode(key, "/")
                    key += 1
                    catRight = CategoryTreeNode(key, "NP")
                    ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                    #ccg = r"(NP\NP)/NP"
                else:
                    ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
                    # ccg = "NP/NP"
            else:

                if prevElementInArray is not None and (prevElementInArray.xpostag=="NC" or prevElementInArray.xpostag=="PRO" ) and (nextElementInArray.xpostag=="DET" or nextElementInArray.xpostag=="NC" or nextElementInArray.xpostag=="P"):
                    catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                    key = catChildTree.size + 1
                    catTop = CategoryTreeNode(key, "/")
                    key += 1
                    catRight = CategoryTreeNode(key, "NP")
                    ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                    # ccg = r"(NP\NP)/NP"
                else:
                    ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
                #ccg = "NP/NP"
        return ccg

    def assigneXpostagADJ2(self,element,sentenceInConll):
        ccg = None
        if int(element.id) < len(sentenceInConll.sentence._elements):
            nextElement = self.getElementWithId(element.head, sentenceInConll.sentence._elements)
            nextElementInArray = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
            prevElementInArray=None
            if int(element.id)>1:
                prevElementInArray  = self.getElementWithId(int(element.id) - 1, sentenceInConll.sentence._elements)

            if int(element.id) < int(element.head):
                    #ccg = r"NP/NP"
                ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
            else:
                #ccg = r"NP\NP"
                if str(nextElementInArray.xpostag) == "ADJ":
                    ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
                else:
                    ccg = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
            #some special case
            if  int(element.id) > int(element.head) and (str(nextElementInArray.xpostag)=="N" or str(nextElementInArray.xpostag)=="NC"):
                #ccg = r"NP/NP"
                ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
            elif int(element.id) > int(element.head) and prevElementInArray is not None and (prevElementInArray.xpostag == "VPR" or prevElementInArray.xpostag == "VPP" or prevElementInArray.xpostag == "V" or prevElementInArray.xpostag == "VINF" or prevElementInArray.xpostag == "VIMP"):
                #ccg = r"NP/NP"
                ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
            elif str(nextElementInArray.xpostag) == "DET" and prevElementInArray is not None and str(prevElementInArray.xpostag)=="DET": #la pluspart des
                ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
        return ccg

    def assigneXpostagCLR2(self,element,sentenceInConll):
        ccg = None
        if int(element.id) < len(sentenceInConll.sentence._elements):
            nextElement = self.getElementWithId(element.head, sentenceInConll.sentence._elements)
            nextElementInArray = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
            prevElementInArray  = self.getElementWithId(int(element.id) - 1, sentenceInConll.sentence._elements)
            if int(element.id) < int(element.head) and (nextElement.xpostag == "VINF" or nextElement.xpostag == "V" or nextElement.xpostag == "VPP" or nextElement.xpostag == "VIMP") :
                catleftChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")

                catRightChildTree = self.catfullTreeNodeWithLabelInput("\\", "S", "NP")
                key = catleftChildTree.size + catRightChildTree.size + 1
                catTop = CategoryTreeNode(key, "/")
                key += 1
                ccg = self.catfullTreeNodeWithNodeInput(catTop, catleftChildTree.root, catRightChildTree.root)
                # ccg = r"(S\NP)/(S\NP)"
            else:
                ccg = self.catTreeSingleNode("NP")

        return ccg

    def assigneXpostagNPP2(self, element,sentenceInConll,position):
        ccg = None
        #if int(element.id) <= len(sentenceInConll.sentence._elements)-1:
        nextElement = self.getElementWithId(element.head, sentenceInConll.sentence._elements)
        nextElementInArray = self.getElementWithId(int(element.id) + 1, sentenceInConll.sentence._elements)
        prevElementInArray = self.getElementWithId(int(element.id) - 1, sentenceInConll.sentence._elements)
        #    if int(element.id) < int(element.head):
        #        # ccg = r"NP/NP"
        #        ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
        #    else:
        #        # ccg = r"NP\NP"
        #        ccg = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        #    # some special case
        #    if int(element.id) > int(element.head) and (
        #            str(nextElementInArray.xpostag) == "N" or str(nextElementInArray.xpostag) == "NC"):
        #        # ccg = r"NP/NP"
        #        ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
        #    elif int(element.id) > int(element.head) and (
        #            prevElementInArray.xpostag == "VPR" or prevElementInArray.xpostag == "VPP" or prevElementInArray.xpostag == "V" or prevElementInArray.xpostag == "VINF" or prevElementInArray.xpostag == "VIMP"):
        #        # ccg = r"NP/NP"
        #        ccg = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        #    elif prevElementInArray.xpostag == "P": # A quelqu'un
        #        ccg = self.catTreeSingleNode("NP")
        #    else:
        #        ccg = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        if position == 0:
            if nextElementInArray.xpostag == "VPP" or nextElementInArray.xpostag == "DET" or nextElementInArray.xpostag == "ADJ" or nextElementInArray.xpostag == "NPP":
                catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                key = catChildTree.size + 1
                catTop = CategoryTreeNode(key, "/")
                key += 1
                catRight = CategoryTreeNode(key, "NP")
                ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                # ccg = r"(NP\NP)/NP"
            else:
                ccg = self.catfullTreeNodeWithLabelInput("/", "NP", "NP")
        else:
            if nextElementInArray.xpostag == "VPP" or nextElementInArray.xpostag == "DET" or nextElementInArray.xpostag == "ADJ" or nextElementInArray.xpostag == "NPP":
                catChildTree = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
                key = catChildTree.size + 1
                catTop = CategoryTreeNode(key, "\\")
                key += 1
                catRight = CategoryTreeNode(key, "NP")
                ccg = self.catfullTreeNodeWithNodeInput(catTop, catChildTree.root, catRight)
                # ccg = r"(NP\NP)/NP"
            else:
                ccg = self.catfullTreeNodeWithLabelInput("\\", "NP", "NP")
        return ccg
    
    '''