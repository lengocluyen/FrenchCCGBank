import os, re, sys
from CONLL.Binarization.TreeNode import TreeNode
from CONLL.Binarization.NodeInfo import NodeInfo
from CONLL.Binarization.DTree import DTree
from CONLL.Binarization.BTree import BTree


class MappingTree:
    def __init__(self):
        self.btree=None

    def buildTree(self,dTreeCluster,elementList):
        bTree = BTree()
        #for root of tree
        key = 0
        rootTreeNode = TreeNode(key,NodeInfo("Phrase",ccgtag=[]))
        bTree.put(rootTreeNode)
        #for the others
        #left tree
        #self.foreachChunk(bTree, rootTreeNode, dTreeCluster[0], position=0)
        #right tree
        parentChunk = dTreeCluster
        dtree = dTreeCluster
        insertNode = rootTreeNode
        for i in range(0,len(dTreeCluster)):
            self.foreachChunk(bTree,rootTreeNode,dtree,parentChunk,dTreeCluster[i],insertNode,position=0)
        self.assigneDependencyForBTree(bTree,elementList)
        self.adjustTree(bTree)

        return bTree

    def adjustTree(self,btree):
        treeNode = btree.root
        self.adjustAddingNode(treeNode,btree)
        self._adjustTree(treeNode)



    def _adjustTree(self,treeNode):
        if treeNode.hasLeftChild():
            self._adjustTree(treeNode.leftChild)
        if treeNode.hasRightChild():
            self._adjustTree(treeNode.rightChild)

        if treeNode is not None:
            self.adjustNode(treeNode)


    def adjustNode(self,treeNode):
        if treeNode.isLeaf()==False:
            if treeNode.hasRightChild() and treeNode.hasLeftChild() is None:
                changedNode = treeNode.rightChild
                treeNode.key = changedNode.key
                treeNode.nodeInfo = changedNode.nodeInfo
                treeNode.rightChild = changedNode.rightChild
                treeNode.leftChild = changedNode.leftChild
            if treeNode.hasLeftChild() and treeNode.hasRightChild() is None:
                changedNode = treeNode.leftChild
                treeNode.key = changedNode.key
                treeNode.nodeInfo = changedNode.nodeInfo

                treeNode.rightChild = changedNode.rightChild
                treeNode.leftChild = changedNode.leftChild


            #treeNode.rightChild = treeNode


        #if treeNode.nodeInfo.dependency is not None:
            #print ("co ne: " + treeNode.nodeInfo.dependency)
        #    deprel = treeNode.nodeInfo.dependency
        #    self.searchParentofCluster(treeNode,deprel)

    #leaf is an element, if a leaf has children, create new node with 2 child : the leaf and his child
    def adjustAddingNode(self,treeNode,btree):
        if treeNode.hasLeftChild():
            self.adjustAddingNode(treeNode.leftChild,btree)
        if treeNode.hasRightChild():
            self.adjustAddingNode(treeNode.rightChild,btree)

        if treeNode.nodeInfo.element and treeNode.hasAnyChildren():
            #copie temperal node
            temNode = treeNode
            temNode.key = treeNode.key
            temNode.nodeInfo = treeNode.nodeInfo
            temNode.leftChild = treeNode.leftChild
            temNode.rightChild = treeNode.rightChild
            #set parent for news node
            #temNode.parent = treeNode.parent
            #create a new node

            newsNode = TreeNode(btree.size + 1, NodeInfo("", ccgtag=[]))
            btree.size +=1
            newsNode.parent= treeNode
            treeNode.leftChild = newsNode
            newsNode.nodeInfo = temNode.nodeInfo
            treeNode.nodeInfo = NodeInfo("", ccgtag=[],element=None)
            #if treeNode.hasLeftChild():
             #   newsNode.rightChild = treeNode.leftChild
            #elif treeNode.hasRightChild():
             #   newsNode.rightChild = treeNode.rightChild

    def searchParentofCluster(self,treeNode,deprel):
        if treeNode.parent is not None:
            currentNode = treeNode.parent
            if currentNode and currentNode.hasLeftChild() and currentNode.hasRightChild() and currentNode.parent.leftChild is currentNode:
                currentNode.nodeInfo.dependency = deprel
            else:
                self.searchParentofCluster(currentNode,deprel)


    def getFirstElementOfChunk(self,chunk):
        if hasattr(chunk[0], "form"):
            return chunk[0]
        else:
            return self.getFirstElementOfChunk(chunk[0])

    def isElementListChunk(self,chunk):
        if hasattr(chunk[0], "form"):
            return True
        return False



    #def buildingSkeletonTree(self,bTree,currentNode, dtree, parentChunk, chunk, insertNode, position=0):

    def foreachChunkWithComponent(self,bTree,currentNode, dtree, parentChunk, chunk, insertNode, position=0):
        if hasattr(chunk[0], "form") == False:
            for i in range(0, len(chunk)):
                bTree = self.foreachChunkWithComponent(bTree, currentNode, dtree, chunk, chunk[i],
                                          bTree.findNodeHasRightNode(bTree.root), position=position)
            return bTree
        else:
            '''             CurrentNode
                                    \
                                     \
                                    TreeNodeInsert
                                     /
                                    /
                            ChunkChildTree

            '''
            if parentChunk is dtree:
                key = bTree.size
                treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
                treeNode.parent = currentNode
                bTree.put(treeNode, 1)
                key += 1
                btreeChild = self.buildBranch(chunk, key)
                # decide branch for putting the child tree in tree
                bTree.putTree(btreeChild, treeNode, position=position)
            else:
                print("chunk: " + self.dTreeChunkRecursiveInText(chunk))
                print("Tree size: " + str(bTree.size))
                if chunk is not parentChunk[len(parentChunk) - 1]:
                    key = bTree.size
                    treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
                    # treeNode.parent = currentNode
                    print("Insert Node Key: " + str(insertNode.key))
                    bTree._put(treeNode, 1, insertNode)
                    key += 1
                    bTree.size += 1
                    btreeChild = self.buildBranchWithFirstChunk(chunk, key)
                    # decide branch for putting the child tree in tree
                    bTree.putTree(btreeChild, treeNode, position=position)

                    insertNode = btreeChild.findNodeHasRightNode(btreeChild.root)
                    print("Insert Node Key: " + str(insertNode.key))
                else:
                    key = bTree.size
                    treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
                    # treeNode.parent = currentNode
                    bTree._put(treeNode, 1, insertNode)
                    key += 1
                    bTree.size += 1
                    btreeChild = self.buildBranch(chunk, key)
                    # decide branch for putting the child tree in tree
                    bTree.putTree(btreeChild, treeNode, position=position)
                    # insertNode = btreeChild.findNodeHasRightNode(btreeChild.root)
    def foreachChunk(self,bTree, currentNode,dtree,parentChunk, chunk, insertNode, position=0):
        if hasattr(chunk[0], "form") == False:
            for i in range(0,len(chunk)):
                bTree = self.foreachChunk(bTree, currentNode,dtree,chunk,chunk[i],bTree.findNodeHasRightNode(bTree.root), position=position)
            return bTree
        else:
            '''             CurrentNode
                                    \
                                     \
                                    TreeNodeInsert
                                     /
                                    /
                            ChunkChildTree
                                
            '''
            if parentChunk is dtree:
                key = bTree.size
                treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
                treeNode.parent = currentNode
                bTree.put(treeNode, 1)
                key += 1
                btreeChild = self.buildBranch(chunk, key)
                # decide branch for putting the child tree in tree
                bTree.putTree(btreeChild, treeNode, position=position)
            else:
                print ("chunk: " + self.dTreeChunkRecursiveInText(chunk))
                print ("Tree size: " + str(bTree.size))
                if chunk is not parentChunk[len(parentChunk)-1]:
                    key = bTree.size
                    treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
                    #treeNode.parent = currentNode
                    print ("Insert Node Key: " + str(insertNode.key))
                    bTree._put(treeNode, 1 ,insertNode)
                    key += 1
                    bTree.size +=1
                    btreeChild = self.buildBranchWithFirstChunk(chunk, key)
                    # decide branch for putting the child tree in tree
                    bTree.putTree(btreeChild, treeNode, position=position)

                    insertNode = btreeChild.findNodeHasRightNode(btreeChild.root)
                    print ("Insert Node Key: " + str(insertNode.key))
                else:
                    key = bTree.size
                    treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
                    #treeNode.parent = currentNode
                    bTree._put(treeNode, 1, insertNode)
                    key += 1
                    bTree.size += 1
                    btreeChild = self.buildBranch(chunk, key)
                    # decide branch for putting the child tree in tree
                    bTree.putTree(btreeChild, treeNode, position=position)
                    #insertNode = btreeChild.findNodeHasRightNode(btreeChild.root)
                '''print("co kho " + chunk[0].form + " parent " + parentChunk[0][0].form + " length " + str(len(parentChunk)))
print ("detail " + self.dTreeChunkRecursiveInText(chunk))
print("detail parent " + self.dTreeChunkRecursiveInText(parentChunk))
#build btreeChild
if chunk is parentChunk[len(parentChunk)-1]:
    print("value. " + chunk[0].form + " len:" + str(len(chunk)))
    childTree = BTree()
    key = bTree.size
    childTreeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
    childTree.put(childTreeNode)
    insertNode = None
    for ichunk in range(0, len(parentChunk) - 1):
        print("danh gia: " + parentChunk[ichunk][0].form)
        key = childTree.size + bTree.size
        treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
        if ichunk == 0:
            insertNode = childTreeNode
        print("insert node Info: " + str(insertNode.key))
        childTree.putNode(treeNode, 1, insertNode)
        key += 1
        childTree.size += 1
        btreeChild = self.buildBranchWithFirstChunk(parentChunk[ichunk], key)

        # decide branch for putting the child tree in tree
        childTree.putTree(btreeChild, treeNode, position=position)
        insertNode = childTree.findNodeHasRightNode(childTree.root)

    key = childTree.size + bTree.size
    finalChunk = parentChunk[len(parentChunk) - 1]
    treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
    childTree.putNode(treeNode, 1, insertNode)
    key += 1
    childTree.size += 1
    btreeChild = self.buildBranch(finalChunk, key)
    # decide branch for putting the child tree in tree
    childTree.putTree(btreeChild, treeNode, 1)

    key = bTree.size + childTree.size
    treeNode = TreeNode(key, NodeInfo("", ccgtag=[]))
    treeNode.parent = currentNode
    bTree.put(treeNode, 1)

    # decide branch for putting the child tree in tree
    bTree.putTree(childTree, treeNode, position=position)
    bTree = childTree'''
            return bTree

    def assigneDependencyForBTree(self, btree, elementList):
        if btree.root is not None:
            self._assigneDependencyForBtree(btree.root,elementList)

    def isElementNode(self,node,elementList):

        for element in elementList:
            if node.nodeInfo.element is not None and node.nodeInfo.element.id == element.id:
                return element
        return None

    def _assigneDependencyForBtree(self,node,elementList):
        element = self.isElementNode(node,elementList)
        if element is not None:
            node.nodeInfo.dependency = element.deprel
        if node.hasLeftChild():
            self._assigneDependencyForBtree(node.leftChild,elementList)
        if node.hasRightChild():
            self._assigneDependencyForBtree(node.rightChild,elementList)


    def findSmallestHeadinChunk(self, chunk):
        minHead = 1000
        for element in chunk:
            if int(element.head) < minHead:
                minHead = int(element.head)
        for element in chunk:
            if int(element.head) == minHead:
                return element
        return None
    def findSmallestIdinChunk(self,chunk):
        minId = 1000
        for element in chunk:
            if int(element.id) < minId:
                minId = int(element.id)
        for element in chunk:
            if int(element.id) == minId:
                return element
        return None
    #mark a small tree with coupe id-first element, id-relationship element with parent
    def buildBranch(self, cluster,key):
        primaryElement = cluster[0]
        cluster = sorted(cluster,key = lambda element: int(element.id))
        btreeChild = BTree()
        sizeCluster = len(cluster)
        if sizeCluster==1:#Btree with one noeud
            element = cluster[0]
            nodeInfo = NodeInfo(element.form,element=element,ccgtag=[],dependency=element.deprel,cluster=[int(element.id),int(element.id)])
            treeNode = TreeNode(key,nodeInfo)
            btreeChild.put(treeNode)
            key +=1
        elif len(cluster) >= 2:
            for i in range(0,sizeCluster-1):
                if btreeChild.length() < 2:

                    nodeInfo = NodeInfo("ccg",ccgtag=[])
                    treeNode = TreeNode(key,nodeInfo)
                    key=key+1
                    btreeChild.put(treeNode)#left: 0 root right:1
                    element = cluster[i]
                    if element is primaryElement:
                        elementHead = self.findSmallestHeadinChunk(cluster)
                        elementId = self.findSmallestIdinChunk(cluster)
                        if int(element.id) == int(elementId.id) and int(element.head) == int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(element.id), int(elementHead.head)])
                        elif int(element.id) != int(elementId.id) and  int(element.head) == int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(elementId.id), int(elementHead.head)])
                        elif int(element.id) == int(elementId.id) and  int(element.head) != int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(elementId.id), int(elementHead.head)])
                        else:
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel)
                    else:
                        nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element,dependency=None)
                    treeNodeLeaf = TreeNode(key,nodeInfoLeaf,parent=treeNode)
                    key+=1
                    btreeChild.put(treeNodeLeaf,position=0)

                else:
                    btreeChildTemp = BTree()
                    nodeInfo = NodeInfo("ccg" ,ccgtag=[])
                    treeNode = TreeNode(key,nodeInfo)
                    key +=1
                    btreeChildTemp.put(treeNode)  # left: 0 root right:1
                    if cluster[i] is primaryElement:
                        element = cluster[i]
                        elementHead = self.findSmallestHeadinChunk(cluster)
                        elementId = self.findSmallestIdinChunk(cluster)
                        if int(element.id) == int(elementId.id) and int(element.head) == int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(element.id), int(elementHead.head)])
                        elif int(element.id) != int(elementId.id) and  int(element.head) == int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(elementId.id), int(elementHead.head)])
                        elif int(element.id) == int(elementId.id) and  int(element.head) != int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(elementId.id), int(elementHead.head)])
                        else:
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel)
                    else:
                        nodeInfoLeaf = NodeInfo(cluster[i].form, ccgtag=[],element= cluster[i],dependency=None)
                    treeNodeLeaf = TreeNode(key,nodeInfoLeaf, parent=treeNode)
                    key +=1
                    btreeChildTemp.put(treeNodeLeaf, position=0)
                    btreeChild.putTree(btreeChildTemp,btreeChild.getExtremeRightNode(),position=1)
            if cluster[sizeCluster-1] is primaryElement:
                element = cluster[sizeCluster-1]
                elementHead = self.findSmallestHeadinChunk(cluster)
                elementId = self.findSmallestIdinChunk(cluster)
                if int(element.id) == int(elementId.id) and int(element.head) == int(elementHead.head):
                    nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                            cluster=[int(element.id), int(elementHead.head)])
                elif int(element.id) != int(elementId.id) and int(element.head) == int(elementHead.head):
                    nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                            cluster=[int(elementId.id), int(elementHead.head)])
                elif int(element.id) == int(elementId.id) and int(element.head) != int(elementHead.head):
                    nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                            cluster=[int(elementId.id), int(elementHead.head)])
                else:
                    nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel)
            else:
                nodeInfoLeaf = NodeInfo(cluster[sizeCluster-1].form, ccgtag=[],element=cluster[sizeCluster-1],dependency=None)
            treeNodeLeaf = TreeNode(key,nodeInfoLeaf)
            key+=1
            btreeChild.put(treeNodeLeaf,position=1)
        return btreeChild

    def buildBranchWithFirstChunk(self, cluster,key):
        primaryElement = cluster[0]
        cluster = sorted(cluster,key = lambda element: int(element.id))
        btreeChild = BTree()
        sizeCluster = len(cluster)
        if sizeCluster==1:#Btree with one noeud
            element = cluster[0]
            nodeInfo = NodeInfo(element.form,element=element,ccgtag=[],dependency=element.deprel,cluster=[int(element.id),int(element.id)])
            treeNode = TreeNode(key,nodeInfo)
            btreeChild.put(treeNode)
            key +=1
        elif len(cluster) >= 2:
            for i in range(0,sizeCluster):
                if btreeChild.length() < 2:

                    nodeInfo = NodeInfo("ccg",ccgtag=[])
                    treeNode = TreeNode(key,nodeInfo)
                    key=key+1
                    btreeChild.put(treeNode)#left: 0 root right:1
                    if cluster[i] is primaryElement:
                        element = cluster[i]
                        elementHead = self.findSmallestHeadinChunk(cluster)
                        elementId = self.findSmallestIdinChunk(cluster)
                        if int(element.id) == int(elementId.id) and int(element.head) == int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(element.id), int(elementHead.head)])
                        elif int(element.id) != int(elementId.id) and int(element.head) == int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(elementId.id), int(elementHead.head)])
                        elif int(element.id) == int(elementId.id) and int(element.head) != int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(elementId.id), int(elementHead.head)])
                        else:
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel)
                    else:
                        nodeInfoLeaf = NodeInfo(cluster[i].form, ccgtag=[], element=cluster[i],dependency=None)
                    treeNodeLeaf = TreeNode(key,nodeInfoLeaf,parent=treeNode)
                    key+=1
                    btreeChild.put(treeNodeLeaf,position=0)

                else:
                    btreeChildTemp = BTree()
                    nodeInfo = NodeInfo("ccg" ,ccgtag=[])
                    treeNode = TreeNode(key,nodeInfo)
                    key +=1
                    btreeChildTemp.put(treeNode)  # left: 0 root right:1
                    if cluster[i] is primaryElement:
                        element = cluster[i]
                        elementHead = self.findSmallestHeadinChunk(cluster)
                        elementId = self.findSmallestIdinChunk(cluster)
                        if int(element.id) == int(elementId.id) and int(element.head) == int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(element.id), int(elementHead.head)])
                        elif int(element.id) != int(elementId.id) and int(element.head) == int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(elementId.id), int(elementHead.head)])
                        elif int(element.id) == int(elementId.id) and int(element.head) != int(elementHead.head):
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel,
                                                    cluster=[int(elementId.id), int(elementHead.head)])
                        else:
                            nodeInfoLeaf = NodeInfo(element.form, ccgtag=[], element=element, dependency=element.deprel)

                    else:
                        nodeInfoLeaf = NodeInfo(cluster[i].form, ccgtag=[], element=cluster[i],dependency=None)
                    treeNodeLeaf = TreeNode(key,nodeInfoLeaf, parent=treeNode)
                    key +=1
                    btreeChildTemp.put(treeNodeLeaf, position=0)
                    btreeChild.putTree(btreeChildTemp,btreeChild.getExtremeRightNode(),position=1)
        return btreeChild

    def traversalBtreeRightLeftParent(self,node,nodeList):
        #traversal a tree and result will bind into a tuple
        if node.hasRightChild():
            self.traversalBtreeRightLeftParent(node.rightChild,nodeList)
        if node.hasLeftChild():
            self.traversalBtreeRightLeftParent(node.leftChild,nodeList)
        if node.hasLeftChild() and node.hasRightChild():
            triples = []
            triples.append(node.rightChild)
            triples.append(node.leftChild)
            triples.append(node)
            nodeList.append(triples)
    def dTreeChunkRecursiveInText(self,chunk):
        if hasattr(chunk[0], "form"):
            s = "["
            for element in chunk:
                s += element.form + " "
            s += "]"
            return s
        else:
            s = "["
            for iChunk in chunk:
                s += self.dTreeChunkRecursiveInText(iChunk)
            s += "]"
            return s
