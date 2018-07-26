from __future__ import print_function
import os,sys
from qas.common.CoNLLXHandle import CoNLLXHandle
from qas.common.FormatError import FormatError


def corpus_info():
    conllx = CoNLLXHandle()

    dir =  "../data/question/output/"
    inputdir = "../data/question/outmalt/"
    i=0
    totalsentence =0;
    for name in os.listdir(inputdir):
        f = os.path.join(inputdir, name)
        try:
            sent_count, word_count = 0, 0
            for document in conllx.read_documents(f):
                sent_count += len(document.sentences())
                word_count += len(document.words())
                i+=1
            totalsentence+=sent_count
            print ('%d - %s: %d sentences, %d words' % (i,f, sent_count, word_count))
        except FormatError, e:
            print >> sys.stderr, 'Error processing %s: %s' % (f, str(e))
    print ("Total Sentence: %d"%(totalsentence))

def createTree():
    # process sentence at a time

    conllx = CoNLLXHandle()
    dir = "../data/question/output/"
    inputdir = "../data/question/outmalt/"

    list = []
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for name in os.listdir(inputdir):
        f = os.path.join(inputdir, name)
        try:
            sent_count, word_count = 0, 0
            i=0
            for sentence in conllx.read_conllx(f):
                sent_count += 1
                word_count += len(sentence.words())

                print (sentence.to_normal_sentence())
                print ("\n")

                dotgraph = sentence.as_dotgraph()
                print (dotgraph)
                name = str(dir) + str(i) + '_'+ sentence.words()[0].lemma
                #print name
                dotgraph.render(name)
                i=i+1

                #for element in sentence.words():
                 #   print element.form

            print ('%s: %d sentences, %d words' % (f, sent_count, word_count))

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
            print ('%s: %d sentences, %d words' % (f, sent_count, word_count))
        except FormatError, e:
            print >> sys.stderr, 'Error processing %s: %s' % (f, str(e))


#createTree()
corpus_info()