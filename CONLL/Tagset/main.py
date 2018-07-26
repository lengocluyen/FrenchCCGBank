import os,re
import sys,os
from CONLL.CoNLLXHandle import CoNLLXHandle
from CONLL.FormatError import FormatError

homepath = "/home/lengocluyen/PyWorkspace/FrenchCCGBank/CONLL/data"
savepath = "/home/lengocluyen/PyWorkspace/FrenchCCGBank/CONLL/Tagset"
def readConllFile(pathFile):
    conllx = CoNLLXHandle()
    return conllx.read_documents(pathFile)

def saveFile(content,savefile):
    with open(savefile, "w") as text_file:
        for item in content:
            text_file.write(str(item)+"\n")

def elemenetStatistics1(element,xpostagCollections):

    exist=False
    for item in xpostagCollections:
        if item[0] == element.xpostag:
            item[1] +=1
            item[2].append(element.form)
            exist=True
            break
    if exist==False:
        xpostagCollections.append([element.xpostag,0,[element.form]])
    return xpostagCollections

def readConllFolder(folderPath,savefolder):
    xpostagCollections = []
    upostagCollections = []
    deprelCollections =  []
    for name in os.listdir(folderPath):
        print ("start: " + str(name))
        f = os.path.join(folderPath, name)
        try:
            #elementConlls = readConllFile(f).words()
            for sentence in readConllFile(f):
                for element in sentence.words():
                    xpostagCollections = elemenetStatistics1(element,xpostagCollections)
                    #if element.xpostag not in xpostagCollections:
                    #    xpostagCollections.append(element.xpostag)
                    if element.upostag not in upostagCollections:
                        upostagCollections.append(element.upostag)
                    if element.deprel not in deprelCollections:
                        deprelCollections.append(element.deprel)
            print("end: " + str(name))
        except FormatError as e:
            print ("Error: " + str(e))
    print ("Saving into file ...")
    xpostagFile = os.path.join(savefolder,"xpostagset.txt")
    xpostgString =[]
    for item in xpostagCollections:
        s=""
        for i in range(0,20):
            s += item[2][i] + " "
        xpostgString.append(item[0] + "\t" + str(item[1]) +"\t" + s +"\n")
    saveFile(xpostgString,xpostagFile)
    upostagFile = os.path.join(savefolder, "upostagset.txt")
    saveFile(upostagCollections, upostagFile)
    deprelFile = os.path.join(savefolder, "deprel.txt")
    saveFile(deprelCollections, deprelFile)
    print("All finish")

readConllFolder(homepath,savepath)