import os, re

from CONLL.Binarization.CategoryTree import CategoryTree

from CONLL.Binarization.CategoryTreeNode import CategoryTreeNode

class CCGRules:
    def __init__(self,argLeft=None,argRight=None,resultTop=None):
        self.argLeft = argLeft
        self.argRight = argRight
        self.resultTop = resultTop



    def allRules(self, argLeft=None,argRight=None,resultTop=None):
        if argLeft is not None and argRight is not None:
            coordinationRules = self.coordiationRules(argLeft=argLeft, argRight=argRight)
            ponctRule  = self.ponctRule(argLeft=argLeft, argRight=argRight)
            if ponctRule is not None:
                return ponctRule
            if coordinationRules is not None:
                return coordinationRules
            applicationRules = self.applicationRules(argLeft=argLeft, argRight=argRight)
            if applicationRules is not None:
               return applicationRules
            substitutionRule = self.subsitutionRules(argLeft=argLeft, argRight=argRight)
            if substitutionRule is not None:
                return substitutionRule
            compositionRule = self.compositionRules(argLeft=argLeft, argRight=argRight)
            if compositionRule is not None:
                return compositionRule
        elif argLeft and resultTop:
            applicationRules = self.applicationRules(argLeft=argLeft, resultTop=resultTop)
            if applicationRules is not None:
                return applicationRules
            substitutionRule = self.subsitutionRules(argLeft=argLeft, resultTop=resultTop)
            if substitutionRule is not None:
                return substitutionRule
            compositionRule = self.compositionRules(argLeft=argLeft, resultTop=resultTop)
            if compositionRule is not None:
                return compositionRule
        elif argRight and resultTop:
            applicationRules = self.applicationRules(argRight=argRight, resultTop=resultTop)
            if applicationRules is not None:
                return applicationRules
            substitutionRule = self.subsitutionRules(argRight=argRight, resultTop=resultTop)
            if substitutionRule is not None:
                return substitutionRule
            compositionRule = self.compositionRules(argRight=argRight, resultTop=resultTop)
            if compositionRule is not None:
                return compositionRule
        return None

    def coordiationRules(self,argLeft=None,argRight=None):
        if str(argLeft.root.label) == "conj" and argRight is not None:
            #argRight = self.removeBackSlash(argRight)
            nodeLeft = argRight.root
            nodeRight = argRight.root
            nodeTop = CategoryTreeNode(argLeft.size + argRight.size + 1, "\\")
            return self.catFullTreeNodeWithNodeInput(nodeTop,nodeLeft, nodeRight)
            #return r"{0}\{1}".format(argRight,argRight)
        return None
    def ponctRule(self,argLeft=None,argRight=None):
        if str(argLeft.root.label) == "ponct" and argRight is not None:
            temp = argRight
            return temp
            #return self.catFullTreeNodeWithNodeInput(nodeTop,nodeLeft, nodeRight)
        elif str(argRight.root.label) == "ponct" and argLeft is not None:
            temp = argLeft
            return temp
            #nodeLeft = argLeft.root
            #nodeRight = argLeft.root
            #nodeTop = argLeft.root
            #return self.catFullTreeNodeWithNodeInput(nodeTop, nodeLeft, nodeRight)
            #return r"{0}\{1}".format(argRight,argRight)
        return None

    def subsitutionRules(self,argLeft=None,argRight=None,resultTop=None):
        '''Forward Crossing Substitution
                (X/Y)\\Z    Y\Z    =>   X\Z
                            X\Z :resultTop
                           /  \
                          /    \
         :argLeft   (X/Y)\\Z----Y/Z :argRight
            Backward Substitution
                Y\Z     (X\Y\Z)    =>   X\Z
            Backward Crossing Substitution
                Y/Z     (X\Y)/Z    =>   X/Z
            Forward Subsitution
                (X/Y)/Z     Y/Z    =>   X/Z

        '''
        rs = None
        if argLeft is not None and argRight is not None:#(X/Y)\\Z    Y\Z    =>   X\Z
            # case1: (X/Y)\\Z    Y\Z    =>   X\Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="\\" and argRight.root.hasLeftChild() and argRight.root.hasLeftChild() and argRight.root.label == "\\":
                XY = argLeft.root.leftChild
                if XY.hasLeftChild() and XY.hasRightChild() and XY.label == "/":
                    X = XY.leftChild
                    Y1 = XY.rightChild

                    Z1 = argLeft.root.rightChild

                    Y2 = argRight.root.leftChild
                    Z2 = argRight.root.rightChild
                    catTree = CategoryTree()
                    if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)) and str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        X.parent = None
                        leftNode = X
                        Z2.parent = None
                        rightNode = Z2
                        topNode = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Z2) + 1,"\\")
                        rs =  self.catFullTreeNodeWithNodeInput(topNode,leftNode,rightNode)
            '''matchLeft1 = self.getMatching(r"\((.*)/(.*)\)\\(.*)", argLeft)
            matchRight11 = self.getMatching(r"(.*)\\(.*)", argRight)
            if matchLeft1 and matchRight11:
                X = matchLeft1.group(1)
                Y1 = matchLeft1.group(2)
                Z1 = matchLeft1.group(3)

                Y2 = matchRight11.group(1)
                Z2 = matchRight11.group(2)
                if str(Y1) == str(Y2) and str(Z1) == str(Z2):
                    return self.removeBackSlash(r"{0}\{1}".format(X, Z1))'''
            # case 2: Y\Z     (X\Y)\Z    =>   X\Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="\\" and argRight.root.hasLeftChild() and argRight.root.hasLeftChild() and argRight.root.label == "\\":
                XY = argRight.root.leftChild
                if XY.hasLeftChild() and XY.hasRightChild() and XY.label == "\\":
                    X = XY.leftChild
                    Y2 = XY.rightChild

                    Z2 = argRight.root.rightChild

                    Y1 = argLeft.root.leftChild
                    Z1 = argLeft.root.rightChild
                    catTree = CategoryTree()
                    if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)) and str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        X.parent = None
                        leftNode = X
                        Z2.parent = None
                        rightNode = Z2
                        topNode = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Z2) + 1,"\\")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,leftNode,rightNode)
            '''matchLeft2 = self.getMatching(r"(.*)\\(.*)", argLeft)
            matchRight2 = self.getMatching(r"\((.*)\\(.*)\)\\(.*)", argRight)
            if matchLeft2 and matchRight2:
                Y1 = matchLeft2.group(1)
                Z1 = matchLeft2.group(2)

                X = matchRight2.group(1)
                Y2 = matchRight2.group(2)
                Z2 = matchRight2.group(3)

                if str(Y1) == str(Y2) and str(Z1) == str(Z2):
                    return self.removeBackSlash(r"{0}\{1}".format(X, Z1))'''
            # case 3: Y/Z     (X\Y)/Z    =>   X/Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="/" and argRight.root.hasLeftChild() and argRight.root.hasLeftChild() and argRight.root.label == "/":
                XY = argRight.root.leftChild
                if XY.hasLeftChild() and XY.hasRightChild() and XY.label == "\\":
                    X = XY.leftChild
                    Y2 = XY.rightChild

                    Z2 = argRight.root.rightChild

                    Y1 = argLeft.root.leftChild
                    Z1 = argLeft.root.rightChild
                    catTree = CategoryTree()
                    if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)) and str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        X.parent = None
                        leftNode = X
                        Z2.parent = None
                        rightNode = Z2
                        topNode = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Z2) + 1,"/")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,leftNode,rightNode)
            '''matchLeft3 = self.getMatching(r"(.*)/(.*)", argLeft)
            matchRight3 = self.getMatching(r"\((.*)\(.*)\)/(.*)", argRight)
            if matchLeft3 and matchRight3:
                Y2 = matchLeft3.group(1)
                Z2 = matchLeft3.group(2)

                X = matchRight3.group(1)
                Y1 = matchRight3.group(2)
                Z1 = matchRight3.group(3)

                if str(Y1) == str(Y2) and str(Z1) == str(Z2):
                    return self.removeBackSlash(r"{0}/{1}".format(X, Z1))'''
            # case 4: (X/Y)/Z     Y/Z    =>   X/Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "/" and argRight.root.hasLeftChild() and argRight.root.hasLeftChild() and argRight.root.label == "/":
                XY = argLeft.root.leftChild
                if XY.hasLeftChild() and XY.hasRightChild() and XY.label == "/":
                    X = XY.leftChild
                    Y1 = XY.rightChild

                    Z1 = argLeft.root.rightChild

                    Y2 = argRight.root.leftChild
                    Z2 = argRight.root.rightChild
                    catTree = CategoryTree()
                    if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)) and str(
                            catTree.traversalRNLinText(Z1)) == str(catTree.traversalRNLinText(Z2)):
                        X.parent = None
                        leftNode = X
                        Z2.parent = None
                        rightNode = Z2
                        topNode = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Z2) + 1,
                                                   "/")
                        rs = self.catFullTreeNodeWithNodeInput(topNode, leftNode, rightNode)
            '''matchLeft4 = self.getMatching(r"\((.*)/(.*)\)/(.*)", argLeft)
            matchRight4 = self.getMatching(r"(.*)/(.*)", argRight)
            if matchLeft4 and matchRight4:
                X = matchLeft4.group(1)
                Y1 = matchLeft4.group(2)
                Z1 = matchLeft4.group(3)

                Y2 = matchRight4.group(1)
                Z2 = matchRight4.group(2)
                if str(Y1) == str(Y2) and str(Z1) == str(Z2):
                    return self.removeBackSlash(r"{0}/{1}".format(X, Z1))
            '''
            return None

        elif argLeft is not None and resultTop is not None:
            argRight = ""
            # case1: (X/Y)\\Z Left   Y\Z =>   X\Z Top
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="\\" and resultTop.root.hasLeftChild() and resultTop.root.hasLeftChild() and resultTop.root.label == "\\":
                XY = argLeft.root.leftChild
                if XY.hasLeftChild() and XY.hasRightChild() and XY.label == "/":
                    X1 = XY.leftChild
                    Y = XY.rightChild

                    Z1 = argLeft.root.rightChild

                    X2 = resultTop.root.leftChild
                    Z2 = resultTop.root.rightChild
                    catTree = CategoryTree()
                    if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)) and str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        Y.parent = None
                        leftNode = Y
                        Z2.parent = None
                        rightNode = Z2
                        topNode = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(Z2) + 1,"\\")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,leftNode,rightNode)
            '''matchLeft1 = self.getMatching(r"\((.*)/(.*)\)\\(.*)", argLeft)
            matchTop1 = self.getMatching(r"(.*)\\(.*)", resultTop)
            if matchLeft1 and matchTop1:
                X1 = matchLeft1.group(1)
                Y = matchLeft1.group(2)
                Z1 = matchLeft1.group(3)

                X2 = matchTop1.group(1)
                Z2 = matchTop1.group(2)
                if str(X1) == str(X2) and str(Z1) == str(Z2):
                    return self.removeBackSlash(r"{0}\{1}".format(Y, Z1))'''
            # case 4: (X/Y)/Z  Left   Y/Z    =>   X/Z Top
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="/" and resultTop.root.hasLeftChild() and resultTop.root.hasLeftChild() and resultTop.root.label == "/":
                XY = argLeft.root.leftChild
                if XY.hasLeftChild() and XY.hasRightChild() and XY.label == "/":
                    X1 = XY.leftChild
                    Y = XY.rightChild

                    Z1 = argLeft.root.rightChild

                    X2 = resultTop.root.leftChild
                    Z2 = resultTop.root.rightChild
                    catTree = CategoryTree()
                    if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)) and str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        Y.parent = None
                        leftNode = Y
                        Z2.parent = None
                        rightNode = Z2
                        topNode = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(Z2) + 1,"/")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,leftNode,rightNode)
            '''matchLeft4 = self.getMatching(r"\((.*)/(.*)\)/(.*)", argLeft)
            matchTop4 = self.getMatching(r"(.*)/(.*)", resultTop)
            if matchLeft4 and matchTop4:
                X1 = matchLeft4.group(1)
                Y = matchLeft4.group(2)
                Z1 = matchLeft4.group(3)

                X2 = matchTop4.group(1)
                Z2 = matchTop4.group(2)
                if str(X1) == str(X2) and str(Z1) == str(Z2):
                    return self.removeBackSlash(r"{0}/{1}".format(Y, Z1))'''
            # case 2: Y\Z Left    (X\Y)\Z    =>   X\Z Top
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="\\" and resultTop.root.hasLeftChild() and resultTop.root.hasLeftChild() and resultTop.root.label == "\\":
                Y = argLeft.root.leftChild
                Z1 = argLeft.root.rightChild

                X = resultTop.root.leftChild

                Z2 = resultTop.root.rightChild
                catTree = CategoryTree()
                if str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        X.parent= None
                        Y.parent = None
                        childRootNode = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Y) +1, "\\")
                        childTree = self.catFullTreeNodeWithNodeInput(childRootNode,X,Y)

                        rightNode = Z1

                        topNode = CategoryTreeNode(catTree.countNumberChildNode(childTree.root) + catTree.countNumberChildNode(Z1) + 1,"\\")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,childRootNode,rightNode)
            '''matchLeft2 = self.getMatching(r"(.*)\\(.*)", argLeft)
            matchTop2 = self.getMatching(r"(.*)\\(.*)", resultTop)
            if matchLeft2 and matchTop2:
                Y = matchLeft2.group(1)
                Z1 = matchLeft2.group(2)

                X = matchTop2.group(1)
                Z2 = matchTop2.group(2)

                if str(Z1) == str(Z2):
                    return self.removeBackSlash(r"({0}\{1})\{2}".format(X,Y, Z1,))'''
            # case 3: Y/Z  Left   (X\Y)/Z    =>   X/Z Top
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="/" and resultTop.root.hasLeftChild() and resultTop.root.hasLeftChild() and resultTop.root.label == "/":
                Y = argLeft.root.leftChild
                Z1 = argLeft.root.rightChild

                X = resultTop.root.leftChild

                Z2 = resultTop.root.rightChild
                catTree = CategoryTree()
                if str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        X.parent= None
                        Y.parent = None
                        childRootNode = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Y) +1, "\\")
                        childTree = self.catFullTreeNodeWithNodeInput(childRootNode,X,Y)

                        rightNode = Z1

                        topNode = CategoryTreeNode(catTree.countNumberChildNode(childTree.root) + catTree.countNumberChildNode(Z1) + 1,"/")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,childRootNode,rightNode)
            '''matchLeft3 = self.getMatching(r"(.*)/(.*)", argLeft)
            matchTop3 = self.getMatching(r"(.*)/(.*)", resultTop)
            if matchLeft3 and matchTop3:
                Y = matchLeft3.group(1)
                Z1 = matchLeft3.group(2)

                X = matchTop3.group(1)
                Z2 = matchTop3.group(2)

                if str(Z1) == str(Z2):
                    return self.removeBackSlash(r"({0}\{1})/{2}".format(X, Y, Z1, ))
            return None'''
        elif argRight is not None and resultTop is not None:
            argLeft = ""
            # case 2: Y\Z     (X\Y)\Z Right    =>   X\Z Top
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label =="\\" and resultTop.root.hasLeftChild() and resultTop.root.hasLeftChild() and resultTop.root.label == "\\":
                XY = argRight.root.leftChild
                if XY.hasLeftChild() and XY.hasRightChild() and XY.label == "\\":
                    X1 = XY.leftChild
                    Y = XY.rightChild

                    Z1 = argRight.root.rightChild

                    X2 = resultTop.root.leftChild
                    Z2 = resultTop.root.rightChild
                    catTree = CategoryTree()
                    if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)) and str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        Y.parent = None
                        leftNode = Y
                        Z2.parent = None
                        rightNode = Z2
                        topNode = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(Z2) + 1,"/")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,leftNode,rightNode)
            '''matchRight2 = self.getMatching(r"\((.*)\\(.*)\)\\(.*)", argRight)
            matchTop2 = self.getMatching(r"(.*)\\(.*)", resultTop)
            if matchRight2 and matchTop2:
                X1 = matchRight2.group(1)
                Y = matchRight2.group(2)
                Z1 = matchRight2.group(3)

                X2 = matchTop2.group(1)
                Z2 = matchTop2.group(2)
                if str(X1) == str(X2) and str(Z1) == str(Z2):
                    return self.removeBackSlash(r"{0}\{1}".format(Y, Z1))'''
            # case 3: Y/Z     (X\Y)/Z Right    =>   X/Z Top
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label =="/" and resultTop.root.hasLeftChild() and resultTop.root.hasLeftChild() and resultTop.root.label == "/":
                XY = argRight.root.leftChild
                if XY.hasLeftChild() and XY.hasRightChild() and XY.label == "\\":
                    X1 = XY.leftChild
                    Y = XY.rightChild

                    Z1 = argRight.root.rightChild

                    X2 = resultTop.root.leftChild
                    Z2 = resultTop.root.rightChild
                    catTree = CategoryTree()
                    if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)) and str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        Y.parent = None
                        leftNode = Y
                        Z2.parent = None
                        rightNode = Z2
                        topNode = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(Z2) + 1,"/")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,leftNode,rightNode)
            '''matchRight3 = self.getMatching(r"\((.*)\\(.*)\)/(.*)", argRight)
            matchTop3 = self.getMatching(r"(.*)/(.*)", resultTop)
            if matchRight3 and matchTop3:
                X1 = matchRight3.group(1)
                Y = matchRight3.group(2)
                Z1 = matchRight3.group(3)

                X2 = matchTop3.group(1)
                Z2 = matchTop3.group(2)
                if str(X1) == str(X2) and str(Z1) == str(Z2):
                    return self.removeBackSlash(r"{0}/{1}".format(Y, Z1))'''
            # case1: (X/Y)\\Z    Y\Z Right   =>   X\Z Top
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label =="\\" and resultTop.root.hasLeftChild() and resultTop.root.hasLeftChild() and resultTop.root.label == "\\":
                Y = argRight.root.leftChild
                Z1 = argRight.root.rightChild

                X = resultTop.root.leftChild

                Z2 = resultTop.root.rightChild
                catTree = CategoryTree()
                if str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        X.parent= None
                        Y.parent = None
                        childRootNode = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Y) +1, "/")
                        childTree = self.catFullTreeNodeWithNodeInput(childRootNode,X,Y)

                        rightNode = Z1

                        topNode = CategoryTreeNode(catTree.countNumberChildNode(childTree.root) + catTree.countNumberChildNode(Z1) + 1,"\\")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,childRootNode,rightNode)
            '''matchRight1 = self.getMatching(r"(.*)\\(.*)", argRight)
            matchTop1 = self.getMatching(r"(.*)\\(.*)", resultTop)
            if matchRight1 and matchTop1:
                Y = matchRight1.group(1)
                Z1 = matchRight1.group(2)

                X = matchTop1.group(1)
                Z2 = matchTop1.group(2)

                if str(Z1) == str(Z2):
                    return self.removeBackSlash(r"({0}/{1})\{2}".format(X, Y, Z1, ))'''
            # case 4: (X/Y)/Z     Y/Z Right    =>   X/Z Top
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label =="/" and resultTop.root.hasLeftChild() and resultTop.root.hasLeftChild() and resultTop.root.label == "/":
                Y = argRight.root.leftChild
                Z1 = argRight.root.rightChild

                X = resultTop.root.leftChild

                Z2 = resultTop.root.rightChild
                catTree = CategoryTree()
                if str(catTree.traversalRNLinText(Z1))== str(catTree.traversalRNLinText(Z2)):
                        X.parent= None
                        Y.parent = None
                        childRootNode = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Y) +1, "/")
                        childTree = self.catFullTreeNodeWithNodeInput(childRootNode,X,Y)

                        rightNode = Z1

                        topNode = CategoryTreeNode(catTree.countNumberChildNode(childTree.root) + catTree.countNumberChildNode(Z1) + 1,"/")
                        rs = self.catFullTreeNodeWithNodeInput(topNode,childRootNode,rightNode)
            '''matchRight4 = self.getMatching(r"(.*)/(.*)", argRight)
            matchTop4 = self.getMatching(r"(.*)/(.*)", resultTop)
            if matchRight4 and matchTop4:
                Y = matchRight4.group(1)
                Z1 = matchRight4.group(2)

                X = matchTop4.group(1)
                Z2 = matchTop4.group(2)

                if str(Z1) == str(Z2):
                    return self.removeBackSlash(r"({0}/{1})/{2}".format(X, Y, Z1 ))'''
        return rs

    def typeRaisingRules(self,arg,catExtension,type="Forward"):
        catTree = CategoryTree()
        rs = None
        if type =="Forward":
            key = catTree.countNumberChildNode(arg)  + catTree.countNumberChildNode(catExtension) +1
            childRootNode = CategoryTreeNode(key,"\\")
            childTree = self.catFullTreeNodeWithNodeInput(childRootNode,catExtension,arg)
            key +=1
            rootNode = CategoryTreeNode(key,"/")
            rs = self.catFullTreeNodeWithNodeInput(rootNode,catExtension,childTree.root)
            #return self.removeBackSlash(r"{0}/({0}\{1})".format(catExtension,arg))
        elif type == "Backward":
            key = catTree.countNumberChildNode(arg)  + catTree.countNumberChildNode(catExtension) +1
            childRootNode = CategoryTreeNode(key,"/")
            childTree = self.catFullTreeNodeWithNodeInput(childRootNode,catExtension,arg)
            key +=1
            rootNode = CategoryTreeNode(key,"\\")
            rs = self.catFullTreeNodeWithNodeInput(rootNode,catExtension,childTree.root)

            #return self.removeBackSlash(r"{0}\({0}/{1})".format(catExtension, arg))
        return rs

    def compositionRules(self,argLeft=None,argRight=None,resultTop=None):
        ''' case1.1: Forward Composition
                X/Y     Y/Z     =>  X/Z
                        X/Z :resultTop
                      /  \
                     /    \
         :argLeft   X/Y----Y/Z :argRight

            case1.2: Forward Crossing Composition
                X/Y     Y\Z     =>  X\Z
            case2.1: Backward Composition
                Y\Z     X\Y     =>  X\Z
            case2.2: Backward Crossing Composition
                Y/Z     X\Y     =>  X/Z

        '''
        catTree = CategoryTree()
        if argLeft is not None and argRight is not None:
            #case1.1: Forward Composition
            #    X/Y     Y/Z     =>  X/Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "/" and argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label=="/":
                X = argLeft.root.leftChild
                Y1 = argLeft.root.rightChild

                Y2 = argRight.root.leftChild
                Z = argRight.root.rightChild
                if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Z) + 1, "/")
                    X.parent = None
                    leftNode = X
                    Z.parent = None
                    rightNode = Z
                    return self.catFullTreeNodeWithNodeInput(nodeRoot,leftNode,rightNode)

            '''
            matchLeft1 = self.getMatching(r"(.*)/(.*)",argLeft)
            matchRight11 = self.getMatching(r"(.*)/(.*)",argRight)
            if matchLeft1 and matchRight11:
                X = matchLeft1.group(1)
                Y1 = matchLeft1.group(2)
                Y2 = matchRight11.group(1)
                Z = matchRight11.group(2)
                if str(Y1) == str(Y2):
                    resultTop = r"{0}/{1}".format(X,Z)'''
            #case1.2: Forward Crossing Composition
            #    X/Y     Y\Z     =>  X\Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "/" and argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label=="\\":
                X = argLeft.root.leftChild
                Y1 = argLeft.root.rightChild

                Y2 = argRight.root.leftChild
                Z = argRight.root.rightChild
                if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Z) + 1, "\\")
                    X.parent = None
                    leftNode = X
                    Z.parent = None
                    rightNode = Z
                    return self.catFullTreeNodeWithNodeInput(nodeRoot,leftNode,rightNode)
            '''matchRight12 = self.getMatching(r"(.*)\\(.*)",argRight)
            if matchLeft1 and matchRight12:
                X = matchLeft1.group(1)
                Y1 = matchLeft1.group(2)
                Y2 = matchRight12.group(1)
                Z = matchRight12.group(2)
                if str(Y1) == str(Y2):
                    resultTop = r"{0}\{1}".format(X,Z)'''
            #case2.1: Backward Composition
            #Y\Z     X\Y     =>  X\Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "\\" and argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label == "\\":
                Y1 = argLeft.root.leftChild
                Z = argLeft.root.rightChild

                X = argRight.root.leftChild
                Y2 = argRight.root.rightChild
                if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Z) + 1,
                                                "\\")
                    X.parent = None
                    leftNode = X
                    Z.parent = None
                    rightNode = Z
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchRight2 = self.getMatching(r"(.*)\\(.*)", argRight)
            matchLeft21 = self.getMatching(r"(.*)\\(.*)", argLeft)
            if matchLeft21 and matchRight2:
                Y1 = matchLeft21.group(1)
                Z = matchLeft21.group(2)
                X = matchRight2.group(1)
                Y2 = matchRight2.group(2)
                if str(Y1) == str(Y2):
                    resultTop = r"{0}\{1}".format(X,Z)'''
            #case2.2: Backward Crossing Composition
            #    Y/Z     X\Y     =>  X/Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "/" and argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label == "\\":
                Y1 = argLeft.root.leftChild
                Z = argLeft.root.rightChild

                X = argRight.root.leftChild
                Y2 = argRight.root.rightChild
                if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(X) + catTree.countNumberChildNode(Z) + 1,
                                                "/")
                    X.parent = None
                    leftNode = X
                    Z.parent = None
                    rightNode = Z
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchLeft22 = self.getMatching(r"(.*)/(.*)", argLeft)
            print ("xem: " + str(matchRight2.groups() ))
            if matchLeft22 and matchRight2:
                Y1 = matchLeft22.group(1)
                Z = matchLeft22.group(2)
                X = matchRight2.group(1)
                Y2 = matchRight2.group(2)
                print ("vao day chu" +  Y1 + "  " + Y2)
                if str(Y1) == str(Y2):
                    resultTop = r"{0}/{1}".format(X,Z)
            return self.removeBackSlash(resultTop)'''
        elif argLeft is not None and resultTop is not None:
            # case1.1: Forward Composition
            #    X/Y left    Y/Z     =>  X/Z top
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "/" and resultTop.root.hasLeftChild() and resultTop.root.hasRightChild() and resultTop.root.label == "/":
                X1 = argLeft.root.leftChild
                Y = argLeft.root.rightChild

                X2 = resultTop.root.leftChild
                Z = resultTop.root.rightChild
                if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(Z) + 1,
                                                "\\")
                    Y.parent = None
                    leftNode = Y
                    Y.parent = None
                    rightNode = Z
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchLeft1 = self.getMatching(r"(.*)/(.*)", argLeft)#X/Y     Y/Z     =>  X/Z
            matchTop1 = self.getMatching(r"(.*)/(.*)", resultTop)
            if matchLeft1 and matchTop1:
                X1 = matchLeft1.group(1)
                Y = matchLeft1.group(2)
                X2 = matchTop1.group(1)
                Z = matchTop1.group(2)
                if str(X1) == str(X2):
                    argRight = r"{0}/{1}".format(Y, Z)'''
            # case1.2: Forward Crossing Composition
            #    X/Y     Y\Z     =>  X\Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "/" and resultTop.root.hasLeftChild() and resultTop.root.hasRightChild() and resultTop.root.label == "\\":
                X1 = argLeft.root.leftChild
                Y = argLeft.root.rightChild

                X2 = resultTop.root.leftChild
                Z = resultTop.root.rightChild
                if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(Z) + 1,
                                                "\\")
                    Y.parent = None
                    leftNode = Y
                    Y.parent = None
                    rightNode = Z
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchLeft2 = self.getMatching(r"(.*)/(.*)", argLeft)  # X/Y     Y\Z     =>  X\Z
            matchTop2 = self.getMatching(r"(.*)\\(.*)", resultTop)
            if matchLeft2 and matchTop2:
                X1 = matchLeft2.group(1)
                Y = matchLeft2.group(2)
                X2 = matchTop2.group(1)
                Z = matchTop2.group(2)
                if str(X1) == str(X2):
                    argRight = r"{0}\{1}".format(Y, Z)'''
            # case2.1: Backward Composition
            # Y\Z     X\Y     =>  X\Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "\\" and resultTop.root.hasLeftChild() and resultTop.root.hasRightChild() and resultTop.root.label == "\\":
                Y = argLeft.root.leftChild
                Z1 = argLeft.root.rightChild

                X = resultTop.root.leftChild
                Z2 = resultTop.root.rightChild
                if str(catTree.traversalRNLinText(Z1)) == str(catTree.traversalRNLinText(Z2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(X) + 1,
                                                "\\")
                    X.parent = None
                    leftNode = X
                    Y.parent = None
                    rightNode = Y
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchLeft3 = self.getMatching(r"(.*)\\(.*)", argLeft)  # Y\Z     X\Y     =>  X\Z
            matchTop3 = self.getMatching(r"(.*)\\(.*)", resultTop)
            if matchLeft3 and matchTop3:
                Y = matchLeft3.group(1)
                Z1 = matchLeft3.group(2)
                X = matchTop3.group(1)
                Z2 = matchTop3.group(2)
                if str(Z1) == str(Z2):
                    argRight = r"{0}\{1}".format(X, Y)'''
            # case2.2: Backward Crossing Composition
            #    Y/Z     X\Y     =>  X/Z
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label == "/" and resultTop.root.hasLeftChild() and resultTop.root.hasRightChild() and resultTop.root.label == "/":
                Y = argLeft.root.leftChild
                Z1 = argLeft.root.rightChild

                X = resultTop.root.leftChild
                Z2 = resultTop.root.rightChild
                if str(catTree.traversalRNLinText(Z1)) == str(catTree.traversalRNLinText(Z2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(X) + 1,
                                                "\\")
                    X.parent = None
                    leftNode = X
                    Y.parent = None
                    rightNode = Y
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchLeft4 = self.getMatching(r"(.*)/(.*)", argLeft)  # Y/Z     X\Y     =>  X/Z
            matchTop4 = self.getMatching(r"(.*)/(.*)", resultTop)
            if matchLeft4 and matchTop4:
                Y = matchLeft4.group(1)
                Z1 = matchLeft4.group(2)
                X = matchTop4.group(1)
                Z2 = matchTop4.group(2)
                if str(Z1) == str(Z2):
                    argRight = r"{0}\{1}".format(X, Y)
            return self.removeBackSlash(argRight)'''
        elif argRight is not None and resultTop is not None:
            # case1.1: Forward Composition
            #    X/Y     Y/Z     =>  X/Z
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label == "/" and resultTop.root.hasLeftChild() and resultTop.root.hasRightChild() and resultTop.root.label == "/":
                Y = argRight.root.leftChild
                Z1 = argRight.root.rightChild

                X = resultTop.root.leftChild
                Z2 = resultTop.root.rightChild
                if str(catTree.traversalRNLinText(Z1)) == str(catTree.traversalRNLinText(Z2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(X) + 1,
                                                "/")
                    X.parent = None
                    leftNode = X
                    Y.parent = None
                    rightNode = Y
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchRight1 = self.getMatching(r"(.*)/(.*)", argRight)  # X/Y     Y/Z     =>  X/Z
            matchTop1 = self.getMatching(r"(.*)/(.*)", resultTop)
            if matchRight1 and matchTop1:
                Y = matchRight1.group(1)
                Z1 = matchRight1.group(2)
                X = matchTop1.group(1)
                Z2 = matchTop1.group(2)
                if str(Z1) == str(Z2):
                    argLeft = r"{0}/{1}".format(X, Y)'''
            # case1.2: Forward Crossing Composition
            #    X/Y     Y\Z     =>  X\Z
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label == "\\" and resultTop.root.hasLeftChild() and resultTop.root.hasRightChild() and resultTop.root.label == "\\":
                Y = argRight.root.leftChild
                Z1 = argRight.root.rightChild

                X = resultTop.root.leftChild
                Z2 = resultTop.root.rightChild
                if str(catTree.traversalRNLinText(Z1)) == str(catTree.traversalRNLinText(Z2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(X) + 1,
                                                "/")
                    X.parent = None
                    leftNode = X
                    Y.parent = None
                    rightNode = Y
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchRight2 = self.getMatching(r"(.*)\\(.*)", argRight)  # X/Y     Y\Z     =>  X\Z
            matchTop2 = self.getMatching(r"(.*)\\(.*)", resultTop)
            if matchRight2 and matchTop2:
            Y = matchRight2.group(1)
            Z1 = matchRight2.group(2)
            X = matchTop2.group(1)
            Z2 = matchTop2.group(2)
            if str(Z1) == str(Z2):
                argLeft = r"{0}/{1}".format(X, Y)'''
            # case2.1: Backward Composition
            # Y\Z     X\Y     =>  X\Z
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label == "\\" and resultTop.root.hasLeftChild() and resultTop.root.hasRightChild() and resultTop.root.label == "\\":
                X1 = argRight.root.leftChild
                Y = argRight.root.rightChild

                X2 = resultTop.root.leftChild
                Z = resultTop.root.rightChild
                if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(X) + 1,
                                                "\\")
                    Y.parent = None
                    leftNode = Y
                    Z.parent = None
                    rightNode = Z
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchRiht3 = self.getMatching(r"(.*)\\(.*)", argRight)  # Y\Z     X\Y     =>  X\Z
            matchTop3 = self.getMatching(r"(.*)\\(.*)", resultTop)
            if matchRiht3 and matchTop3:
            X1 = matchRiht3.group(1)
            Y = matchRiht3.group(2)
            X2 = matchTop3.group(1)
            Z = matchTop3.group(2)
            if str(X1) == str(X2):
                argLeft = r"{0}\{1}".format(Y, Z)'''
            # case2.2: Backward Crossing Composition
            #    Y/Z     X\Y     =>  X/Z
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label == "/" and resultTop.root.hasLeftChild() and resultTop.root.hasRightChild() and resultTop.root.label == "/":
                X1 = argRight.root.leftChild
                Y = argRight.root.rightChild

                X2 = resultTop.root.leftChild
                Z = resultTop.root.rightChild
                if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)):
                    nodeRoot = CategoryTreeNode(catTree.countNumberChildNode(Y) + catTree.countNumberChildNode(X) + 1,
                                                "/")
                    Y.parent = None
                    leftNode = Y
                    Z.parent = None
                    rightNode = Z
                    return self.catFullTreeNodeWithNodeInput(nodeRoot, leftNode, rightNode)
            '''matchRight4 = self.getMatching(r"(.*)\\(.*)", argRight)  # Y/Z     X\Y     =>  X/Z
            matchTop4 = self.getMatching(r"(.*)/(.*)", resultTop)
            if matchRight4 and matchTop4:
                X1 = matchRight4.group(1)
                Y = matchRight4.group(2)
                X2 = matchTop4.group(1)
                Z = matchTop4.group(2)
                if str(X1) == str(X2):
                    argLeft = r"{0}/{1}".format(Y, Z)
            return self.removeBackSlash(argLeft)'''
        else:
            return None

    def applicationRules(self,argLeft=None,argRight=None,resultTop=None):
        catTree = CategoryTree()
        '''Forward Application:
                X/Y      Y      => X
           Backward Application
                Y        X\Y    => X
                       X :resultTop                              X :resultTop
                      /  \                                     /   \
                     /    \                                   /     \
         :argLeft   X/Y----Y :argRight          :argLeft     Y------X\Y :argRight

        '''
        rs = None
        if argLeft is not None and argRight is not None:
            #print("vao day chu" + str(catTree.traversalRNLinText(argLeft.root)) + " " + catTree.traversalRNLinText(argRight.root))
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="/":
                X = argLeft.root.leftChild
                Y1 = argLeft.root.rightChild

                Y2 = argRight.root
                catTree = CategoryTree()
                if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)):
                    rs = self.copyNodeIntoNewsTree(X)
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label == "\\":
                X = argRight.root.leftChild
                Y1 = argRight.root.rightChild

                Y2 = argLeft.root
                catTree = CategoryTree()
                if str(catTree.traversalRNLinText(Y1)) == str(catTree.traversalRNLinText(Y2)):
                    rs = self.copyNodeIntoNewsTree(X)

            '''resultTop = ""
            regexLeft = r"(.*)/{0}".format(re.escape(argRight))
            matchLeft = self.getMatching(regexLeft,argLeft)
            if matchLeft: #Forward
                resultTop = matchLeft.group(1)
            regexRight = r"(.*)\\{0}".format(re.escape(argLeft))
            matchRight = self.getMatching(regexRight, argRight)
            if matchRight:
                resultTop = matchRight.group(1)
            return self.removeBackSlash(resultTop)'''
        elif argLeft is not None and resultTop is not None:
            if argLeft.root.hasLeftChild() and argLeft.root.hasRightChild() and argLeft.root.label =="/":
                X1 = argLeft.root.leftChild
                Y = argLeft.root.rightChild

                X2 = resultTop.root
                catTree = CategoryTree()
                if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)):
                    Y.parent = None
                    #Y.root = Y
                    rs =  Y
            if argLeft is not None and resultTop is not None:
                catTree = CategoryTree()
                key = catTree.countNumberChildNode(argLeft.root) + catTree.countNumberChildNode(resultTop.root) +1
                rootNode = CategoryTreeNode(key,"\\")

                X_leftNode = argLeft.root
                Y_rightNode = resultTop.root
                rs = self.catFullTreeNodeWithNodeInput(rootNode,X_leftNode,Y_rightNode)
            '''regexLeft = r"{0}/(.*)".format(re.escape(resultTop))
            matchLeft = self.getMatching(regexLeft,argLeft)
            if matchLeft:
                argRight = matchLeft.group(1)
            else:
                argRight = r"{0}\{1}".format(resultTop,argLeft)
            return argRight'''
        elif argRight is not None and resultTop is not None:#Y        X\Y right    => X top
            if argRight.root.hasLeftChild() and argRight.root.hasRightChild() and argRight.root.label =="\\":
                X1 = argRight.root.leftChild
                Y = argRight.root.rightChild

                X2 = resultTop.root
                catTree = CategoryTree()
                if str(catTree.traversalRNLinText(X1)) == str(catTree.traversalRNLinText(X2)):
                    rs = self.copyNodeIntoNewsTree(Y)
            if argRight is not None and resultTop is not None:
                catTree = CategoryTree()
                key = catTree.countNumberChildNode(argRight.root) + catTree.countNumberChildNode(resultTop.root) +1
                rootNode = CategoryTreeNode(key,"/")

                X_leftNode = resultTop.root
                Y_rightNode = argRight.root
                rs = self.catFullTreeNodeWithNodeInput(rootNode,X_leftNode,Y_rightNode)

            '''regexRight =r"{0}\\(.*)".format(re.escape(resultTop))
            matchRight = self.getMatching(regexRight,argRight)
            if matchRight:
                argLeft = matchRight.group(1)
            else:
                argLeft = "{0}/{1}".format(resultTop,argRight)
            return self.removeBackSlash(argLeft)'''

        return rs
            #raise Exception("Missing the parameter! Need at least 2 parameter for this function!")

    def copyNodeIntoNewsTree(self,nodeInput):
        catTree = CategoryTree()
        catTree.parent = None
        catTree.root = nodeInput
        if nodeInput.hasLeftChild():
            catTree.leftChild = nodeInput.leftChild
        if nodeInput.hasRightChild():
            catTree.rightChild = nodeInput.rightChild
        return catTree

    def getMatching(self,regex,text):
        return re.match(regex,text, re.M|re.I)

    def removeBackSlash(self,line):
        if line.count("(")==1 and line.count(")")==0:
            line = line.replace("(","")
        if (line.count("/")==1 and line.count("(")==0 and line.count(")")==0) or (line.count("\\")==1 and line.count("(")==0 and line.count(")")==0):
            line = "("+line+")"
        return line
 #       return line.replace("\\(","(").replace("\\)",")").replace("\\\\","\\")

    def catTreeSingleNode(self,category):
        catTree = CategoryTree()
        catTreeNode = CategoryTreeNode(catTree.size + 1, category)
        catTree.buildTree(catTreeNode)
        return catTree
    def catFullTreeNodeWithLabelInput(self,top,left,right):
        catTree = CategoryTree()
        key = catTree.size + 1
        topNode = CategoryTreeNode(key, top)
        key +=1
        leftNode = CategoryTreeNode(key, left)
        key +=1
        rightNode = CategoryTreeNode(key,right)
        catTree.buildTree(topNode,nodeLeft=leftNode, nodeRight=rightNode)
        return catTree
    def catFullTreeNodeWithNodeInput(self,top,left,right):
        catTree = CategoryTree()
        catTree.buildTree(top,nodeLeft=left, nodeRight=right)
        return catTree
def test2():
    ccgRule = CCGRules()
    print(ccgRule.allRules(argLeft=r"NP\NP", argRight=r"(NP\NP)\(NP\NP)"))
    print(ccgRule.allRules(argLeft=r"(S\NP)/NP", argRight=r"(S\NP)\(S\NP)"))
    print ("test")
    print(ccgRule.compositionRules(argLeft=r"(S\NP)/NP", argRight=r"(S\NP)\(S\NP)"))
    print ("test")
def test():
    ccgRule = CCGRules()
    print (ccgRule.applicationRules(argLeft=r"(S\NP)",argRight=r"NP\(S\NP)"))
    print (ccgRule.applicationRules(argLeft=r"(S/NP)/(S/NP)",resultTop=r"(S/NP)"))
    print (ccgRule.applicationRules(argRight=r"X\Y",resultTop=r"X"))

    '''case1.1: Forward Composition
                    X/Y     Y/Z     =>  X/Z
                            X/Z :resultTop
                          /  \
                         /    \
             :argLeft   X/Y----Y/Z :argRight
    
                case1.2: Forward Crossing Composition
                    X/Y     Y\Z     =>  X\Z
                case2.1: Backward Composition
                    Y\Z     X\Y     =>  X\Z
                case2.2: Backward Crossing Composition
                    Y/Z     X\Y     =>  X/Z'''

    print ("Left and Right => Top")
    print ("Type 1: X/Z == " +  ccgRule.compositionRules(argLeft=r"X/Y",argRight=r"Y/Z"))
    print ("Type 2: X\Z == " + ccgRule.compositionRules(argLeft=r"X/Y",argRight=r"Y\Z"))
    print ("Type 3: X\Z == " + ccgRule.compositionRules(argLeft=r"Y\Z",argRight=r"X\Y"))
    print ("Type 4: X/Z == " + ccgRule.compositionRules(argLeft=r"Y/Z",argRight=r"X\Y"))
    print ("Left and Top => Right")
    print ("Type 1: Y/Z == " +  ccgRule.compositionRules(argLeft=r"X/Y",resultTop=r"X/Z"))
    print ("Type 2: Y\Z == " + ccgRule.compositionRules(argLeft=r"X/Y",resultTop=r"X\Z"))
    print ("Type 3: X\Y == " + ccgRule.compositionRules(argLeft=r"Y\Z",resultTop=r"X\Z"))
    print ("Type 4: X\Y == " + ccgRule.compositionRules(argLeft=r"Y/Z",resultTop=r"X/Z"))
    print ("Right and Top => Left")
    print ("Type 1: X/Y == " +  ccgRule.compositionRules(argRight=r"Y/Z",resultTop=r"X/Z"))
    print ("Type 2: X/Y == " + ccgRule.compositionRules(argRight=r"Y\Z",resultTop=r"X\Z"))
    print ("Type 3: Y\Z == " + ccgRule.compositionRules(argRight=r"X\Y",resultTop=r"X\Z"))
    print ("Type 4: Y/Z == " + ccgRule.compositionRules(argRight=r"X\Y",resultTop=r"X/Z"))

    # Type 1: (X/Y)\\Z    Y\Z    =>   X\Z
    # Type 2: Y\Z     (X\Y\Z)    =>   X\Z
    # Type 3: Y/Z     (X\Y)/Z    =>   X/Z
    # Type 4: (X/Y)/Z     Y/Z    =>   X/Z
    print ("Substitution")
    print ("Left and Right => Top")
    print ("Type 1: X\Z == " +  ccgRule.subsitutionRules(argLeft=r"(X/Y)\Z",argRight=r"Y\Z"))
    print ("Type 2: X\Z == " + ccgRule.subsitutionRules(argLeft=r"Y\Z",argRight=r"(X\Y)\Z"))
    print ("Type 3: X/Z == " + ccgRule.subsitutionRules(argLeft=r"Y/Z",argRight=r"(X\Y)/Z"))
    print ("Type 4: X/Z == " + ccgRule.subsitutionRules(argLeft=r"(X/Y)/Z",argRight=r"Y/Z"))
    print ("Left and Top => Right")
    print ("Type 1: Y\Z == " +  ccgRule.subsitutionRules(argLeft=r"(X/Y)\Z",resultTop=r"X\Z"))
    print ("Type 2: (X\Y)\Z == " + ccgRule.subsitutionRules(argLeft=r"Y\Z",resultTop=r"X\Z"))
    print ("Type 3: (X\Y)/Z == " + ccgRule.subsitutionRules(argLeft=r"Y/Z",resultTop=r"X/Z"))
    print ("Type 4: Y/Z == " + ccgRule.subsitutionRules(argLeft=r"(X/Y)/Z",resultTop=r"X/Z"))
    print ("Right and Top => Left")
    print ("Type 1: (X/Y)\Z == " +  ccgRule.subsitutionRules(argRight=r"Y\Z",resultTop=r"X\Z"))
    print ("Type 2: Y\Z == " + ccgRule.subsitutionRules(argRight=r"(X\Y)\Z",resultTop=r"X\Z").strip("\\"))
    print ("Type 3: Y/Z == " + ccgRule.subsitutionRules(argRight=r"(X\Y)/Z",resultTop=r"X/Z").strip("\\"))
    print ("Type 4: (X/Y)/Z == " +ccgRule.subsitutionRules(argRight=r"Y/Z",resultTop=r"X/Z").strip("\\"))

    print("All Rule Function test with Type 1: X\Z == " + ccgRule.allRules(argLeft=r"(X/Y)\Z", argRight=r"Y\Z"))
#test()
#test2()