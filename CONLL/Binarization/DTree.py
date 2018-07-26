import re
from CONLL.Binarization.NodeInfo import NodeInfo

class DTree:
    def __init__(self,sentence):
        self.sentence = sentence
        self.sentenceSize = sentence.length()
        self.bTree = None

    def drawTreeInText(self):
        dotgraph = self.sentence.as_dotgraph()
        print(dotgraph)

    def drawTreeInGraphics(self, filename, directory, format="png"):
        dotgraph = self.sentence.as_dotgraph()
        dotgraph.format = format
        dotgraph.render(filename=filename, directory=directory, cleanup=True)

    def chunkingDtree(self):
        chunkList = []
        #sentence: chunk1 sujet with head: est 0/ chunk2 verb .../ chunk3 object / chunk4 mod/ example

        elementRoot,elementHeadofChunkList = self.chunkingFilter() #Head of chunk: est 0/ Pour  8 /, 8 / urgence 8 / de 8
        chunkList.append(elementRoot)
        for element in elementHeadofChunkList:
            elementList = []
            elements= []
            elements.append(element)
            elementList.append(element)
            while len(elements) > 0:
                elementFirst = elements[0]
                for word in self.sentence._elements:
                    if elementFirst.id == word.head:
                        elements.append(word)
                        elementList.append(word)
                elements.remove(elementFirst)
            chunkList.append(elementList)

        return chunkList



    def chunkingFilter(self):
        chunkList = self.elementHeadOfChunk()
        newsChunkListRoot = []
        filterChunkList = self.elementHeadOfChunk()
        newsChunkListRoot.append(self.elementHeadOfChunk()[0])
        filterChunkList.remove(self.elementHeadOfChunk()[0])
        for element in chunkList:
            if re.match(r"aux*", element.deprel):
                newsChunkListRoot.append(element)
                filterChunkList.remove(element)
        #for element in filterChunkList:
            #if re.match(r"ponct", element.deprel) or re.match(r"PONCT", element.lemma):
                #filterChunkList.remove(element)
        return newsChunkListRoot, filterChunkList


    def elementHeadOfChunk(self):
        chunkHead = []
        elementRoot = self.findRootinSentence()
        if elementRoot is not None:
            chunkHead.append(elementRoot)
            for element in self.sentence._elements:
                if element.head == elementRoot.id:
                    chunkHead.append(element)
        return chunkHead
    def findRootinSentence(self):
        for element in self.sentence._elements:
            if element.deprel == "root":
                return element
        return None

    def isSentence(self):
        for element in self.sentence._elements:
            if element.deprel == "root" and str(element.upostag) == "V":
                return element
        return None

    #def chunkingDtreeRercusionNonPonct(self, chunk):
        #if len(chunk) > 0:
            #if hasattr(chunk[0], "form"):
                #deleteList = []
                #for element in chunk:
                #    if (str(element.deprel).lower() == "ponct" or str(element.upostag).lower() == "ponct"):
                #        deleteList.append(element)
                #for item in deleteList:
                #    if item in chunk:
                #        chunk.remove(item)
            #else:
                #for iChunk in chunk:
                    #self.chunkingDtreeRercusionNonPonct(iChunk)

    def chunkingDtreeRercusion(self,isSorted = True):
        sentences = self.sentence._elements
        result = None
        if self.isSentence() is None:
            phrase =[]
            phrase.append(sentences)
            result=phrase
        else:
            result = self._chunkingDtreeRercusion(sentences)
        if isSorted:
            result = self.sortedChunk(result)
        return result

    def _chunkingDtreeRercusion(self,chunk):
        chunkList = []
        # In a chunk, we create 3 list:
            # beforeVerb: the elements before the verbs
            # elementListRoot: get all verb phrase
            # elementHeadOfChunkList: get head element of every chunk
        beforeverb,elementListRoot,elementHeadofChunkList = self.chunkingFilterByVerb(chunk) #Head of chunk: est 0/ Pour  8 /, 8 / urgence 8 / de 8
        lenofChunk = len(chunk)
        if elementListRoot is None:
            return chunk
        else:
            if len(beforeverb)>0:
                chunkList.append(beforeverb)
            chunkList.append(elementListRoot)
            #print (": " + self.dTreeChunkRecursiveInText(chunkList))
            for element in elementHeadofChunkList:
                elementList = []
                elements= []
                elements.append(element)
                elementList.append(element)
                while len(elements) > 0:
                    elementFirst = elements[0]
                    for word in self.sentence._elements:
                        if elementFirst.id == word.head:
                            elements.append(word)
                            elementList.append(word)
                    elements.remove(elementFirst)
                temChunk = self._chunkingDtreeRercusion(elementList)
                if len(temChunk) > 0:
                    chunkList.append(temChunk)
            if len(chunk)==1:
                return chunkList
            else:
                return self.sortedChunk(chunkList)

    def getChildOfElementInGroupVerb(self,element,sentencesConll):
        result=[]
        visitedList = []
        visitedList.append(element)
        while len(visitedList)>0:
            for item in sentencesConll:
                if int(item.head) == int(visitedList[0].id):
                    result.append(item)
                    visitedList.append(item)
            visitedList.remove(visitedList[0])
        return result

    def getAllChildOfAnElement(self,element):
        elements=[]
        elements.append(element)
        result = []
        result.append(elements)
        while len(elements)>0:
            temp = elements[0]
            for item in self.sentence._elements:
                if int(item.head)==int(temp.id) and item not in elements:
                    elements.append(item)
                    result.append(item)
            elements.remove(temp)
        return result
    def getAllBesideOfAnElement(self,element,chunk):
        outlist = self.getAllChildOfAnElement(element)
        elements = []
        result = []
        for item in chunk:
            if item not in outlist and int(item.id)>int(element.id):
                elements.append(item)
                result.append(item)
        while len(elements) > 0:
            temp = elements[0]
            for item in self.sentence._elements:
                if int(item.head) == int(temp.id) and item not in elements:
                    elements.append(item)
                    result.append(item)
            elements.remove(temp)
        return result

    def chunkingFilterByVerb(self,chunk):
        #tim dong tu trong chunk, tu do loc ra cac tu dau cua moi chunk dua vao dong tu
        #tuy nhien, voi truong hop: il y a quelques jours, il la root cua chunk, cach tiep can nay ko thuc hien duoc

        chunkList = self.elementHeadOfChunkbyVerb(chunk)

        print ("\nStart of the Chunk")

        print("chunk: " + self.dTreeChunkRecursiveInText(chunk))
        if len(chunkList)>0:
            beforeVerbe = []
            #contain list of head element of the chunk
            filterChunkList = chunkList

            #if have verb, get first element for verb chunk
            if len(filterChunkList) > 0:
                verbeRoot = self.elementHeadOfChunkbyVerb(chunk)[0]
            else:
                verbeRoot = None
            chunkVerbRoot = []
            if verbeRoot:
                chunkVerbRoot.append(verbeRoot)
                #remove this item in the head element list
                filterChunkList.remove(verbeRoot)

            i=0
            print ("elementHeadOfChunkByVerb: ")
            for item in self.elementHeadOfChunkbyVerb(chunk):
                print (str(i)  + " " + item.form + "["+str(item.id)+"] _ ")
                i+=1
            print ('\n')

            print("beforechunk: " + self.dTreeChunkRecursiveInText(beforeVerbe))
            print("chunkVerbRoot: " + self.dTreeChunkRecursiveInText(chunkVerbRoot))
            print("filterChunkList: " + self.dTreeChunkRecursiveInText(filterChunkList))
            #use for the base level: de vancinner ...
            tempChunkList = []
            listSujet = []
            for element in chunk:
                if element.deprel == "suj" and int(element.head) != 0:
                    listSujet = self.getChildsOfElement(element)
                condition1 = (element.deprel != "suj" and element not in listSujet)

                #and element.xpostag != "PROREL" and \
                #    element.xpostag != "CLO" and \
                #    condition1 and \
                #    str(element.xpostag) != "ADV" and element.deprel != "aff" and \
                #    re.match(r"aux*", element.xpostag) != "V"
                #cum tu truoc cau trong cau
                #if ((int(element.head) > int(verbeRoot.id) and int(element.id) < int(verbeRoot.id)) or\
                #     int(element.head) < int(verbeRoot.id) and int(element.id) < int(verbeRoot.id)) and\
                #    element is not verbeRoot and str(verbeRoot.deprel) != "root":
                if element not in self.getAllChildOfAnElement(verbeRoot) and element is not verbeRoot and str(verbeRoot.deprel) != "root" and element not in self.getAllBesideOfAnElement(verbeRoot,chunk):
                    tempChunkList.append(element)
                #if element.deprel=="suj" and (verbeRoot is not None and int(element.head)!=int(verbeRoot.id) and int(verbeRoot.head) !=0):
                #    print ("element:" + element.form)
                #    tempChunkList.append(element)
                #    childs = self.getChildsOfElementNonVerRoot(element,verbeRoot)
                #    for item in childs:
                #        if item not in tempChunkList and item not in chunkVerbRoot:
                #            tempChunkList.append(item)

            for item in tempChunkList:
                beforeVerbe.append(item)
                if item in filterChunkList:
                    filterChunkList.remove(item)

            #print("beforechunk: " + self.dTreeChunkRecursiveInText(beforeVerbe))
            #get the first head possible in verb chunk. i.e: ont, ne, plus, se,
            tempChunkList=[]
            for element in chunkList:
                condi = int(element.id) > int(verbeRoot.id) - 3 and int(element.id) < int(verbeRoot.id) + 3
                condi2 = re.match(r"ADV", element.xpostag) \
                        #or re.match(r"CLR", element.xpostag) \
                         #or re.match(r"V", element.xpostag) or re.match(r"VPP", element.xpostag) or\
                #re.match(r"VINF", element.xpostag) or re.match(r"VIMP", element.xpostag) or re.match(r"VPR", element.xpostag)
                # re.match(r"aff",element.deprel) or\
                if re.match(r"aux", element.deprel) or\
                (condi2 and condi):

                    tempChunkList.append(element)
                    childList = self.getChildOfElementInGroupVerb(element,self.sentence._elements)
                    if len(childList)>0:
                        for item in childList:
                            tempChunkList.append(item)
            for item in tempChunkList:
                    chunkVerbRoot.append(item)
                    if item in filterChunkList:
                        filterChunkList.remove(item)
            print("chunk: " + self.dTreeChunkRecursiveInText(chunk))
            print("beforechunk: " + self.dTreeChunkRecursiveInText(beforeVerbe))
            print("chunkVerbRoot: " + self.dTreeChunkRecursiveInText(chunkVerbRoot))
            print("filterChunkList: " + self.dTreeChunkRecursiveInText(filterChunkList))
            print("\nEnd of the Chunk\n")
            return self.sortedElement(beforeVerbe),self.sortedElement(chunkVerbRoot), self.sortedElement(filterChunkList)
        else:
            return None, None, None

    def getFirstElementOfChunk(self,chunk):
        element = None
        if len(chunk) > 0:
            if hasattr(chunk[0], "form"):
                element = chunk[0]
            else:
                element = self.getFirstElementOfChunk(chunk[0])
            return element
        else:
            return None

    def sortedChunk(self, chunk):
        if len(chunk) >1:
            for passnum in range(len(chunk)-1,0,-1):
                for i in range(passnum):
                    if (int(self.getFirstElementOfChunk(chunk[i]).id) > int(self.getFirstElementOfChunk(chunk[i+1]).id)):
                        tempChunk = chunk[i]
                        chunk[i] = chunk[i+1]
                        chunk[i+1] = tempChunk
        return chunk

    def sortedElement(self, elementList):
        for passnum in range(len(elementList)-1,0,-1):
            for i in range(passnum):
                if (int(elementList[i].id) > int(elementList[i+1].id)):
                    tempChunk = elementList[i]
                    elementList[i] = elementList[i+1]
                    elementList[i+1] = tempChunk
        return elementList

    def elementHeadOfChunkbyVerb(self,chunk):
        '''

        :param chunk
        :return: list of the element which are associated with principal verb in chunk
        '''
        chunkHead = []
        elementVerbe = self.findVerbInChunk(chunk)

        if elementVerbe:
            chunkHead.append(elementVerbe)
            for element in self.sentence._elements:
                if element.head == elementVerbe.id:
                    chunkHead.append(element)
            #head of verb is id of its parent

            parentOfElementVerb = self.getElementByID(elementVerbe.head)
            while parentOfElementVerb:
                if parentOfElementVerb in chunk:
                    remainElements = self.getChildsOfElement(parentOfElementVerb)
                    if len(remainElements)>1:
                        for element in remainElements:
                            if element not in chunkHead and int(element.id) > int(elementVerbe.id):
                                chunkHead.append(element)
                    parentOfElementVerb = self.getElementByID(parentOfElementVerb.head)
                else:
                    break

        #in case:     N1                    o
        #            / \                   / \
        #           V   N4          ===>  N1  o
        #         /   \                      / \
        #        N2    N3                   N2  o
        #                                      / \
        #                                     N3 N4
        #if parent of V has child
        #   add all child of of this parent
        return chunkHead

    def getElementByHead(self, head):
        for element in self.sentence._elements:
            if int(element.head) == int(head):
                return element
        return None

    def getElementByID(self, head):
        for element in self.sentence._elements:
            if int(element.id) == int(head):
                return element
        return None
    def getChildsOfElement(self, elementParent):
        elements = []
        for element in self.sentence._elements:
            if int(element.head) == int(elementParent.id):
                elements.append(element)
        return elements
    def getChildsOfElementNonVerRoot(self,el,verbRoot):
        elements=[]
        listElementofVerbRoot = self.getChildsOfElement(verbRoot)
        for element in self.sentence._elements:
            if int(element.head) == int(el.id) and el not in listElementofVerbRoot:
                elements.append(element)
        return elements

    def findVerbInChunk(self,chunk):
        for element in chunk:
            if str(element.upostag) == "V" and str(element.deprel) == "root":
                return element
        for element in chunk:
            if element.upostag == "V" and element is not chunk[len(chunk)-1]:
                return element
        return None

    def __str__(self):
        dotgraph = self.sentence.as_dotgraph()
        return repr(dotgraph)

    def __repr__(self):
        dotgraph = self.sentence.as_dotgraph()
        return dotgraph

    def dTreeChunkRecursiveInText(self,chunk):
        if len(chunk)>0:
            if hasattr(chunk[0], "form"):
                s = "["
                for element in chunk:
                    s += element.form + "("+str(element.id)+ "-" +str(element.deprel)+") "
                s += "]"
                return s
            else:
                s = "["
                for iChunk in chunk:
                    s += self.dTreeChunkRecursiveInText(iChunk)
                s += "]"
                return s
        elif hasattr(chunk, "form"):
            return "[" +chunk.form +"]"
        else: return "[]"
