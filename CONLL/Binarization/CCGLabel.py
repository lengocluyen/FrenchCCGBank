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
class CCGLabel:
    #axiom
    #1
    def basic_NP(self):
        return self.catTreeSingleNode("NP")
    #2
    def basic_S(self):
        return self.catTreeSingleNode("S")
    #3
    def basic_PP(self):
        return self.catTreeSingleNode("PP")

    #4
    def complex_NP_fs_NP(self):
        return self.catfullTreeNodeWithLabelInput("/","NP","NP")
    #5
    def complex_NP_bs_NP(self):
        return self.catfullTreeNodeWithLabelInput("\\","NP","NP")
    #6
    def complex_NP_bs_NP_and_fs_NP(self):

        return self.catfullTreeNodeWithLabelInput("\\","NP","NP")



    def catTreeSingleNode(self,categoryLabel):
        catTree = CategoryTree()
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