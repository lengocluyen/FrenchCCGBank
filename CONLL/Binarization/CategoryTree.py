


class CategoryTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def length(self):
        return self.size

    def height(self, node):
        if node is None:
            return 0
        else:
            return max(self.height(node.leftChild), self.height(node.rightChild)) + 1

    def buildTree(self,top,nodeLeft=None,nodeRight=None):
        if nodeLeft is not None and nodeRight is not None and top is not None:
            self.root = top
            self.root.leftChild = nodeLeft
            self.root.rightChild = nodeRight
        elif top is not None:
            self.root = top
            self.root.leftChild = None
            self.root.rightChild = None

    def matchedLeft(self, matchedNode):
        if self.size==1:
            if matchedNode.label == self.root.label:
                return True
            else:
                return False
        else:
            total = self.countNumberChildNode(matchedNode)
            if self.root.hasLeftChild() is None:
                return False
            totalCurrentLeftChild = self.countNumberChildNode(self.root.leftChild)
            if total != totalCurrentLeftChild:
                return False
            if self._matchedLeft(self.root.leftChild, matchedNode) == self.countNumberChildNode(self.root.leftChild):
                return True
            else:
                return False


    def _matchedLeft(self,nodeA,nodeB):
        count = 0
        if nodeA.label == nodeB.label:
            count += 1
        if nodeA.hasLeftChild() and nodeB.hasLeftChild():
            count += self._matchedLeft(nodeA.leftChild, nodeB.leftChild)
        if nodeA.hasRightChild() and nodeB.hasRightChild():
            count += self._matchedLeft(nodeA.rightChild, nodeB.rightChild)
        return count

    def countNumberChildNode(self, node):
        count =0
        if node is not None:
            count += 1
        if node.hasLeftChild():
            count += self.countNumberChildNode(node.leftChild)
        if node.hasRightChild():
            count += self.countNumberChildNode(node.rightChild)
        return count

    def traversalRNLinText(self,treeNode):
        res = self._traversalRNLinText(treeNode)
        if "(" == res[0]:
            res = res[1:len(res) - 1]
        return res

    def _traversalRNLinText(self,node):
        res = ""
        if node.hasLeftChild() is not None and node.hasRightChild() is None:
            if node.underscript is not None:
                res = "(" + self._traversalRNLinText(node.leftChild) + node.label +"["+node.underscript+"]"+ ")"
            else:
                res = "(" + self._traversalRNLinText(node.leftChild) + node.label + ")"
        if node.hasLeftChild() is None and node.hasRightChild() is not None:
            if node.underscript is not None:
                res = "(" + node.label + self._traversalRNLinText(node.rightChild) +"["+node.underscript+"]"+ ")"
            else:
                res = "(" + node.label + self._traversalRNLinText(node.rightChild) + ")"
        if node.hasLeftChild() is not None and node.hasRightChild() is not None:
            if node.underscript is not None:
                res = "(" + self._traversalRNLinText(node.leftChild) + node.label +"["+node.underscript+"]" + self._traversalRNLinText(
                    node.rightChild) + ")"
            else:
                res = "(" + self._traversalRNLinText(node.leftChild) + node.label + self._traversalRNLinText(node.rightChild) + ")"
        else:
            if node.underscript is not None:
                res = node.label+"["+node.underscript+"]"
            else:
                res = node.label
        return res


    def traversalRightNodeLeft(self,root):
        res=[]
        if root:
            if root.hasLeftChild() is not None:
                res = self.traversalRightNodeLeft(root.leftChild)
            res.append(root.label)
            if root.hasRightChild() is not None:
                res = res + self.traversalRightNodeLeft(root.rightChild)
        return res