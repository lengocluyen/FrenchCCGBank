from CONLL.Binarization.NodeInfo import NodeInfo

class CategoryTreeNode:
    def __init__(self,key, label,underscript = None, left=None, right=None, parent=None):
        self.key = key
        self.label = label
        self.underscript = underscript
        self.rightChild=right
        self.leftChild=left
        self.parent=parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild is self

    def isRightChild(self):
        return self.parent and self.parent.rightChild is self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self, label, lc, rc):
        self.label = label
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def __str__(self, level=0):
        return repr(self.label)

    def __repr__(self):
        return '<tree node representation>'