import re, sys, os
from CONLL.Binarization.NodeInfo import NodeInfo
from CONLL.Binarization.TreeNode import TreeNode
import graphviz
import asciitree

from CONLL.Binarization.CategoryTree import CategoryTree

from CONLL.Binarization.CategoryTreeNode import CategoryTreeNode

class BTree:
    def __init__(self):
        self.root = None
        self.size=0

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def length(self):
        return self.size

    def height(self,node):
        if node is None:
            return 0
        else:
            return max(self.height(node.leftChild),self.height(node.rightChild)) + 1
    def searchElementinTree(self,element):
        return self._searchElemetnInTree(self.root,element)

    def _searchElemetnInTree(self,node,element):
        if node.hasLeftChild():
            return self._searchElemetnInTree(node.leftChild,element)
        if node.hasRightChild():
            return self._searchElemetnInTree(node.rightChild,element)
        if node.nodeInfo.element:
            if int(node.nodeInfo.element.id) == int(element.id):
                return node.nodeInfo.element
            else:
                return None
        else:
            return None

    def traversalRightLeftNode(self,node):
        #traversal a tree and result will bind into a tuple
        if node.hasLeftChild() and node.hasRightChild():
            return "["+ self.traversalRightLeftNode(node.rightChild) + " " + self.traversalRightLeftNode(node.leftChild) + " " + str(node.key) + "]"
        elif node.hasLeftChild():
            return self.traversalRightLeftNode(node.leftChild) + " " + str(node.key)
        elif node.hasRightChild():
            return self.traversalRightLeftNode(node.rightChild) + " " + str(node.key)
        else:
            return str(node.key)

    def getRoot(self):
        return self.root

    def put(self, treeNode, position=None):
        if self.root:
            self._put(treeNode, position, self.root)
        else:
            self.root = treeNode
        self.size += 1


    def _put(self,treeNode, position, currentNode):
        if position==0:#0: left 1: right
            if currentNode.hasLeftChild():
                self._put(treeNode, position, currentNode.leftChild)
            else:
                treeNode.parent = currentNode
                currentNode.leftChild = treeNode
        else:
            if currentNode.hasRightChild():
                self._put(treeNode, position, currentNode.rightChild)
            else:
                treeNode.parent = currentNode
                currentNode.rightChild = treeNode

    def putNode(self,treeNode, position, currentNode):
        if position==0:#0: left 1: right
            if currentNode.hasLeftChild():
                self.putNode(treeNode, position, currentNode.leftChild)
            else:
                treeNode.parent = currentNode
                currentNode.leftChild = treeNode
        else:
            if currentNode.hasRightChild():
                self.putNode(treeNode, position, currentNode.rightChild)
            else:
                treeNode.parent = currentNode
                currentNode.rightChild = treeNode

    def findNode(self, bTree, node):
        return self._findNode(bTree.root,node)

    def _findNode(self, currentNode,node):
        if currentNode.hasRightChild():
            return self._findNode(currentNode.rightChild,node)
        if currentNode.hasLeftChild():
            return self._findNode(currentNode.leftChild,node)
        if currentNode is node:
            return node
        else: return None

    def putTree(self, childTree,currentNode, position=None):
        self._putTree(childTree,currentNode,position)
        self.size += childTree.size

    def _putTree(self,childTree,currentNode, position):
        if position==0:#0: left 1: right
            if currentNode.hasLeftChild():
                self._put(childTree.root, position, currentNode.leftChild)
            else:
                childTree.root.parent = currentNode
                currentNode.leftChild = childTree.root
        else:
            if currentNode.hasRightChild():
                self._put(childTree.root, position, currentNode.rightChild)
            else:
                childTree.root.parent = currentNode
                currentNode.rightChild = childTree.root

    def getExtremeRightNode(self):
        return self._getExtremeRightNode(self.root)

    def _getExtremeRightNode(self,currentNode):
        if currentNode.hasRightChild():
            return self._getExtremeRightNode(currentNode.rightChild)
        else:
            return currentNode


    def findNodeHasRightNode(self,currentNode):
        if currentNode.hasRightChild():
            return self.findNodeHasRightNode(currentNode.rightChild)
        else:
            if currentNode.hasLeftChild():
                if currentNode.leftChild.isLeaf():
                    return currentNode

                else:
                    return self.findNodeHasRightNode(currentNode.leftChild)
            else:
                return currentNode

    def getExtremeLeftNode(self):
        return self._getExtremeLeftNode(self.root)

    def _getExtremeLeftNode(self,currentNode):
        if currentNode.hasLeftChild():
            return self._getExtremeLeftNode(currentNode.rightChild)
        else:
            return currentNode

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.nodeInfo
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        self.delete(key)

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def remove(self, currentNode):
        if currentNode.isLeaf():  # leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():  # interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.nodeInfo = succ.nodeInfo

        else:  # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                                currentNode.leftChild.nodeInfo,
                                                currentNode.leftChild.leftChild,
                                                currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                                currentNode.rightChild.nodeInfo,
                                                currentNode.rightChild.leftChild,
                                                currentNode.rightChild.rightChild)

    def __str__(self):
        return self.getTreeInStr(self.root,0,"")

    def drawTree(self,filenam,directory=None,format="pdf"):
        graph = self.build_graph_tree(self.root, graphviz.Digraph())
        #print (graph)
        graph.format=format
        graph.render(filename=filenam,directory=directory,cleanup=True)

    def getTreeInStr(self, currentNode,level,rs):

        rs += '\t' * level + str(currentNode.key) + "-"+str(currentNode) + "\n"
        if currentNode.hasLeftChild():
            level += 1
            rs = self.getTreeInStr(currentNode.leftChild, level, rs)
        if currentNode.hasRightChild():
            level += 1
            rs = self.getTreeInStr(currentNode.rightChild, level, rs)
        return rs

    def build_graph_tree(self,currentNode, graph, node_formatter=None, edge_formatter=None):
        node_formatter = node_formatter or (lambda element: {})
        edge_formatter = edge_formatter or (lambda element: {})
        labelNode = ""
        catTree = CategoryTree()
        if currentNode.nodeInfo.label == "ccg":
            currentNode.nodeInfo.label=""
        labelNode = str(currentNode.key) + " - "+currentNode.nodeInfo.label
        if currentNode.nodeInfo.ccgTag is not None:
            catTreeList = currentNode.nodeInfo.ccgTag

            string = ""
            for itemCattree in catTreeList:
                if itemCattree is not None:
                    string += str(itemCattree.traversalRNLinText(itemCattree.root)) + " , "
            if currentNode.nodeInfo.element:
                labelNode = str(currentNode.nodeInfo.element.id) +" - "+ str(currentNode.nodeInfo.element.form)
            labelNode = str(currentNode.key) + " - "+currentNode.nodeInfo.label
            if currentNode.nodeInfo.element:
                labelNode += " - " + currentNode.nodeInfo.element.xpostag + "\n" + "i: " + str(currentNode.nodeInfo.element.id) + " h: " +str(currentNode.nodeInfo.element.head)
                labelNode += "\n "+ repr(string) + ""
            else:
                labelNode += repr(string)
        strs = ""
        graph.node(str(currentNode.key), label=labelNode,**node_formatter(currentNode))
        if currentNode.hasLeftChild():
            setLabel =""
            if currentNode.leftChild.nodeInfo.cluster is not None:
                strs = " \n ID: " + str(currentNode.leftChild.nodeInfo.cluster[0]) + " Head: " + str(currentNode.leftChild.nodeInfo.cluster[1])
            if currentNode.leftChild.nodeInfo.dependency is not None:
                setLabel = currentNode.leftChild.nodeInfo.dependency
            graph.edge(str(currentNode.key), str(currentNode.leftChild.key),label=setLabel + strs,**edge_formatter(currentNode.leftChild))
            graph = self.build_graph_tree(currentNode.leftChild,graph,node_formatter,edge_formatter)
        if currentNode.hasRightChild():
            strs = ""
            setLabel = ""
            if currentNode.rightChild.nodeInfo.cluster is not None:
                strs = " \n ID: " + str(currentNode.rightChild.nodeInfo.cluster[0]) + " Head: " + str(currentNode.rightChild.nodeInfo.cluster[1])
            if currentNode.rightChild.nodeInfo.dependency is not None:
                setLabel = currentNode.rightChild.nodeInfo.dependency
            graph.edge(str(currentNode.key), str(currentNode.rightChild.key),label=setLabel  + strs ,**edge_formatter(currentNode.rightChild))
            graph = self.build_graph_tree(currentNode.rightChild, graph,node_formatter,edge_formatter)
        return graph
    def build_graph_tree2(self,currentNode, graph, node_formatter=None, edge_formatter=None):
        node_formatter = node_formatter or (lambda element: {})
        edge_formatter = edge_formatter or (lambda element: {})
        labelNode = ""
        catTree = CategoryTree()
        if currentNode.nodeInfo.label == "ccg":
            currentNode.nodeInfo.label=""
        labelNode = str(currentNode.key) + " - "+currentNode.nodeInfo.label
        if currentNode.nodeInfo.ccgTag is not None:
            catTreeList = currentNode.nodeInfo.ccgTag

            string = ""
            for itemCattree in catTreeList:
                if itemCattree is not None:
                    string += str(itemCattree.traversalRNLinText(itemCattree.root)) + " , "
            if currentNode.nodeInfo.element:
                labelNode = str(currentNode.nodeInfo.element.id) +" - "+ str(currentNode.nodeInfo.element.form)
            labelNode = str(currentNode.key) + " - "+currentNode.nodeInfo.label
            if currentNode.nodeInfo.element:
                labelNode += " - " + currentNode.nodeInfo.element.xpostag + "\n" + "i: " + str(currentNode.nodeInfo.element.id) + " h: " +str(currentNode.nodeInfo.element.head)
                labelNode += "\n "+ repr(string) + ""
            else:
                labelNode += repr(string)
        #for id and head
        strs = ""

        labelNode=""
        if currentNode.nodeInfo.element:
            labelNode =  str(currentNode.nodeInfo.element.form)

        graph.node(str(currentNode.key), label=labelNode,**node_formatter(currentNode))
        if currentNode.hasLeftChild():
            setLabel =""
            #if currentNode.leftChild.nodeInfo.cluster is not None:
                #strs = " \n ID: " + str(currentNode.leftChild.nodeInfo.cluster[0]) + " Head: " + str(currentNode.leftChild.nodeInfo.cluster[1])
            if currentNode.leftChild.nodeInfo.dependency is not None:
                setLabel = currentNode.leftChild.nodeInfo.dependency
            graph.edge(str(currentNode.key), str(currentNode.leftChild.key),label=setLabel + strs,**edge_formatter(currentNode.leftChild))
            graph = self.build_graph_tree(currentNode.leftChild,graph,node_formatter,edge_formatter)
        if currentNode.hasRightChild():
            strs = ""
            setLabel = ""
            #if currentNode.rightChild.nodeInfo.cluster is not None:
                #strs = " \n ID: " + str(currentNode.rightChild.nodeInfo.cluster[0]) + " Head: " + str(currentNode.rightChild.nodeInfo.cluster[1])
            if currentNode.rightChild.nodeInfo.dependency is not None:
                setLabel = currentNode.rightChild.nodeInfo.dependency
            graph.edge(str(currentNode.key), str(currentNode.rightChild.key),label=setLabel  + strs ,**edge_formatter(currentNode.rightChild))
            graph = self.build_graph_tree(currentNode.rightChild, graph,node_formatter,edge_formatter)
        return graph
    def __repr__(self):
        return '<tree node representation>1'

    def countLeaf(self,treeNode):
        count = 0
        if treeNode.isLeaf():
            count += 1
        if treeNode.hasLeftChild():
            count +=self.countLeaf(treeNode.leftChild)
        if treeNode.hasRightChild():
            count +=self.countLeaf(treeNode.rightChild)
        return count