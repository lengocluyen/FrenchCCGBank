#from common.directory import Directory
#from common.docConverter import DocumentConverter
#from common.commandLinux import CommandExecute
from SemanticExtraction.src.directory import Directory
from SemanticExtraction.src.docConverter import DocumentConverter
from SemanticExtraction.src.commandLinux import CommandExecute
import os

home="/home/lengocluyen/Data" # can take this from argv

#Convert folder of the word files to txt file
#dir=os.path.join(home,"/FICHIERS_WORD/")
#directory = Directory()
#list= directory.scan_dir(dir)


#for name in list:
#    os.rename(name,name.replace("(","").replace(")","").replace("-","").replace(" ","").replace("!","").replace("'",""))
#    print (name)

#add the environmental variables


#docConverter = DocConverter()
#docConverter.docx2text_fileInFolderConverter(list,dir + "txt/")

#Convert folder of the pdf files to txt file
#dir=os.path.join(home,"CommunicationSimplifiee/")
#print dir
#directory = Directory()
#list= directory.scan_dir(dir)


#for name in list:#
#    os.rename(name,name.replace("(","").replace(")","").replace("-","").replace(" ","").replace("!","").replace("'",""))
#    print (name)

#add the environmental variables

#docConverter = DocumentConverter()
#docConverter.pdf2text_fileInFolderConverter(list,os.path.join(home,"CommunicationSimplifiee_txt/"))

#Textes Analyseurs


commande=CommandExecute()
def addEnvironmentalVariables():
    commande.exucute("export MALT_DIR="+home+"/malt-1.3.1")
    commande.exucute("export PYTHONPATH="+home+"/melt-0.6/src/")
    commande.exucute("export BONSAI="+home+"/bonsai_v3.2")

def executeExtractText(filename):
    variablesCommand="export MALT_DIR="+home+"/malt-1.3.1 && export PYTHONPATH="+home+"/melt-0.6/src/ && export BONSAI="+home+"/bonsai_v3.2"
    mainCommande="$BONSAI/bin/bonsai_malt_parse_rawtext.sh"
    finalCommande =  variablesCommand +" && "+mainCommande +" '"+ filename+"'"
    print finalCommande
    result=commande.exucute(finalCommande)
    print (result)


#dataset="/home/lengocluyen/PyWorkspace/PyCharmProjects/qas/data/question/" # can take this from argv
dataset="/home/lengocluyen/PyWorkspace/PyCharmProjects/qas/data/" # can take this from argv
dirTxt=os.path.join(dataset, "bescherelle/")

#dirTxt=os.path.join(home,"txt/")
directoryTxt = Directory()
listTxt = directoryTxt.scan_dir(dirTxt)


for name in listTxt:
    executeExtractText(name)


