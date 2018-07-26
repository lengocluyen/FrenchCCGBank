from __future__ import division
from qas.common.common import Utils
import string
import math
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk.corpus.reader import WordListCorpusReader
from sklearn.feature_extraction.text import TfidfVectorizer
#billchambers.me/tutorials/2014/12/21/tf-idf-explained-in-python.html
class Transform():

    def __init__(self,csvFile):
        self.csvFile = csvFile
        #csvfile = "../data/MAILS_MON_CONSEILLER_CONS.csv"
        self.all_documents = Utils().read_csv_and_output_in_a_list(csvFile, ";")
        #self.all_documents = ["France is a countre of pain", "The pain is the most food in the world", "There were manry foreigner student who didn't speakk french"]

    def tokenzie(self,doc):
        return doc.lower().split(" ")

    def stopword_list(self,from_file=None):
        results = []
        stopword_collections = stopwords.words("french")
        for item in stopword_collections:
            results.append(item)
        with open(from_file,"r") as f:
            data = f.readlines()
            for line in data:
                results.append(line.lower().replace("\t"," ").replace("\r","").replace("\n","").rstrip())

        return results

    def jaccard_similarity(self,query,document):
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        return len(intersection)/len(union)

    def term_frequency(self,term,tokenized_document):
        return tokenized_document.count(term)

    def sublinear_term_frequency(self,term,tokenized_document):
        count = tokenized_document.count(term)
        if count ==0:
            return 0
        return 1+ math.log(count)

    def augmented_term_frequency(self,term, tokenized_document):
        max_count = max([self.term_frequency(t,tokenized_document) for t in tokenized_document])
        return (0.5 + ((0.5 * self.term_frequency(term,tokenized_document))/max_count))

    def inverse_document_frequencies(self,tokenized_documents):
        idf_values = {}
        all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
        for tkn in all_tokens_set:
            contains_token = map(lambda doc:tkn in doc, tokenized_documents)
            idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
        return idf_values

    def tfidf(self, documents):
        tokenized_documents = [self.tokenzie(d) for d in documents]
        idf = self.inverse_document_frequencies(tokenized_documents)
        tfidf_documents = []
        for document in tokenized_documents:
            doc_tfidf = []
            for term in idf.keys():
                tf = self.sublinear_term_frequency(term,document)
                doc_tfidf.append(tf*idf[term])
            tfidf_documents.append(doc_tfidf)
        return tfidf_documents

    def sklearn_tfidfvectorizer(self,input = None,encoding='utf-8',decode_error='strict',strip_accents=None,lowercase=True,preprocessor=None,tokenizer=None,
                                analyzer="word",stop_words=None,token_pattern='(?u)\b\w\w+\b', ngram_range=(1,1),max_df=1.0,min_df=1,max_features=None,
                                vocabulary=None,binary=False,norm='l2',use_idf=True,smooth_idf=True,sublinear_tf = False
                                ):
        tokenize = lambda doc: doc.lower().split(" ",)
        min_df=1
        smooth_idf = False
        sublinear_tf = True
        #stop_words = self.stopword_list("../data/stopwords_fr.txt")
        print self.all_documents
        sklearn_tfidf = TfidfVectorizer(input = input,encoding=encoding,decode_error=decode_error,strip_accents=strip_accents,lowercase=lowercase,preprocessor=preprocessor,tokenizer=tokenizer,
                                analyzer=analyzer,stop_words=stop_words,token_pattern=token_pattern, ngram_range=ngram_range,max_df=max_df,min_df=min_df,max_features=max_features,
                                vocabulary=vocabulary,binary=binary,norm=norm,use_idf=use_idf,smooth_idf=smooth_idf,sublinear_tf = sublinear_tf)
        sklearn_representation = sklearn_tfidf.fit_transform(self.all_documents)
        return sklearn_representation

    def sklearn_tfidfvectorizer2(self, ):
        tokenize = lambda doc: doc.lower().split(" ",)

        stop_words = self.stopword_list("../data/stopwords_fr.txt")
        print self.all_documents
        sklearn_tfidf = TfidfVectorizer(norm = 'l2',min_df = 0, use_idf=True, smooth_idf=False, sublinear_tf=True,tokenizer=tokenize,stop_words=stop_words)
        sklearn_representation = sklearn_tfidf.fit_transform(self.all_documents)
        return sklearn_representation

    def consine_similarity(self,vector1, vector2):
        dot_product = sum(p *q for p,q in zip(vector1, vector2))
        sum1 = sum([val**2 for val in vector1])
        sum2 = sum([val**2 for val in vector2])
        magnitude = math.sqrt(sum1) * math.sqrt(sum2)
        if not magnitude:
            return 0
        return dot_product/magnitude

#all documents
#all_documents = Utils().read_csv_and_output_in_a_list("../data/MAILS_MON_CONSEILLER_CONS.csv", ";")
all_documents =["France is a countre of pain", "The pain is the most food in the world", "There were manry foreigner student who didn't speakk french"]
#from sklean
##tokenize = lambda doc: doc.lower().split(" ")
##sklearn_tfidf = TfidfVectorizer(norm = 'l2',min_df = 0, use_idf=True, smooth_idf=False, sublinear_tf=True,tokenizer=tokenize)
##sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

#sklearn_representation = sklearn_representation.toarray()
#print sklearn_representation

#our tfidf
transform = Transform("../data/MAILS_MON_CONSEILLER_CONS.csv")
tfidf_representation = transform.tfidf(all_documents)
#print tfidf_representation
our_tfidf_comparisons = []


sklearn_representation = transform.sklearn_tfidfvectorizer2()
#stop_words = transform.stopword_list("../data/stopwords_fr.txt")



print tfidf_representation[0]
print sklearn_representation.toarray()[0].tolist()
print all_documents[0]

for count_0, doc_0 in enumerate(tfidf_representation):
    for count_1,doc_1 in enumerate(sklearn_representation.toarray()):
        our_tfidf_comparisons.append((Transform("../data/MAILS_MON_CONSEILLER_CONS.csv").consine_similarity(doc_0,doc_1),count_0,count_1))

skl_tfidf_comparisons=[]
for count_0, doc_0 in enumerate(sklearn_representation.toarray()):
    for count_1,doc_1 in enumerate(sklearn_representation.toarray()):
        skl_tfidf_comparisons.append((Transform("../data/MAILS_MON_CONSEILLER_CONS.csv").consine_similarity(doc_0,doc_1),count_0,count_1))

for x in zip(sorted(our_tfidf_comparisons, reverse=True), sorted(skl_tfidf_comparisons,reverse=True)):
    print x

