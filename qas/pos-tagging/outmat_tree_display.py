import json
import os
import sys
import re
from cycler import concat
import codecs
import xmltodict
from os.path import basename

from SemanticExtraction.src.ATR.CandidateTermExtraction import CandidateTermExtraction
from SemanticExtraction.src.ATR.CandidateTermExtraction import CandidateTerm
from SemanticExtraction.src.ATR.CoNLLXHandle import CoNLLXHandle
from SemanticExtraction.src.ATR.FormatError import FormatError
from SemanticExtraction.src.ATR.TripleExtraction import  TripleExtraction
from SemanticExtraction.src.ATR.GraphExtraction.SubGraphControl import SubGraphControl
from SemanticExtraction.src.ATR.WordNetMongoDB import ConnectionMongoDB
from SemanticExtraction.src.Graphics.sentencegraph import SentenceGraph
from SemanticExtraction.src.directory import Directory

#dirhome="/home/lengocluyen/"

#dir = os.path.join(dirhome, "corpus/output/")
#inputdir = os.path.join(dirhome, "corpus/outmalt/")

dirhome="/home/lengocluyen/PyWorkspace/PyCharmProjects/qas/data/"

dir = os.path.join(dirhome, "output/bescherelle_pdf/")
inputdir = os.path.join(dirhome, "output/bescherelle_out")

def createTree():
    # process sentence at a time

    conllx = CoNLLXHandle()
    #dir = "/home/lengocluyen/Data/output/"
    #inputdir = "/home/lengocluyen/Data/txt/"


    list = []
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for name in os.listdir(inputdir):
        f = os.path.join(inputdir, name)
        try:
            sent_count, word_count = 0, 0
            i=0
            pdf_name = name.replace(".txt.outmalt","")
            for sentence in conllx.read_conllx(f):
                sent_count += 1
                word_count += len(sentence.words())

                print sentence.to_normal_sentence()
                print "\n"

                dotgraph = sentence.as_dotgraph()
                print dotgraph
                name = str(dir) + pdf_name +"_"+ str(i)
                #print name
                dotgraph.format = "jpg"
                dotgraph.render(name)
                i=i+1

                #for element in sentence.words():
                 #   print element.form

            print '%s: %d sentences, %d words' % (f, sent_count, word_count)

        except FormatError, e:
            print >> sys.stderr, 'Error processing %s: %s' % (f, str(e))

    # process document at a time
    for name in os.listdir(inputdir):
        f = os.path.join(inputdir, name)
        try:
            sent_count, word_count = 0, 0
            for document in conllx.read_documents(f):
                sent_count += len(document.sentences())
                word_count += len(document.words())
            print '%s: %d sentences, %d words' % (f, sent_count, word_count)
        except FormatError, e:
            print >> sys.stderr, 'Error processing %s: %s' % (f, str(e))


def delete_file_not_pdf(path):
    for name in os.listdir(path):
        dirhome = "/home/lengocluyen/PyWorkspace/PyCharmProjects/qas/data/"

        dir = os.path.join(dirhome, "output/bescherelle_pdf/")
        fullpath = os.path.join(dir,name)
        extension = os.path.splitext(fullpath)[1][1:]
        if extension != "pdf" and extension !="jpg":
            print fullpath
            if os.path.isfile(fullpath):
                os.remove(fullpath)



#execution
createTree()
delete_file_not_pdf(dir)

