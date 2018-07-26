import sys,os
from CONLL.CoNLLXHandle import CoNLLXHandle
from CONLL.FormatError import FormatError
def corpus_info(inputdir):
    conllx = CoNLLXHandle()
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
        except FormatError as e:
            print ('Error processing %s: %s' % (f, str(e)))
    print ("Total Sentence: %d"%(totalsentence))

def createTree(path, output,format="pdf"):
    conllx = CoNLLXHandle()
    list = []
    i = 0
    for name in os.listdir(path):
        f = os.path.join(path, name)
        try:
            sent_count, word_count = 0, 0
            for sentence in conllx.read_conllx(f):
                sent_count += 1
                word_count += len(sentence.words())

                print(sentence.to_normal_sentence())
                print("\n")

                dotgraph = sentence.as_dotgraph()
                print(dotgraph)
                name = str(i) + '_'+ sentence.words()[0].lemma
                #print name
                dotgraph.render(filename=name, directory=output, cleanup=True)
                i=i+1

                #for element in sentence.words():
                 #   print element.form

            print ('%s: %d sentences, %d words' % (f, sent_count, word_count))

        except FormatError as e:
            print (sys.stderr, 'Error processing %s: %s' % (f, str(e)))

    # process document at a time
    for name in os.listdir(path):
        f = os.path.join(path, name)
        try:
            sent_count, word_count = 0, 0
            for document in conllx.read_documents(f):
                sent_count += len(document.sentences())
                word_count += len(document.words())
            print ('%s: %d sentences, %d words' % (f, sent_count, word_count))
        except FormatError as e:
            print (sys.stderr, 'Error processing %s: %s' % (f, str(e)))


#conll_dir = "/home/lengocluyen/corpus/sequoia-corpus-v6.0/conll"
#conll_dir_tree_output= "/home/lengocluyen/corpus/sequoia-corpus-v6.0/treeoutput/"
conll_dir = "/home/lengocluyen/corpus/frenchTreebank/t"
conll_dir_tree_output= "/home/lengocluyen/corpus/frenchTreebank/output/"
#corpus_info(conll_dir)
createTree(conll_dir,conll_dir_tree_output)
