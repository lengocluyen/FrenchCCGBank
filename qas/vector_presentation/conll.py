from SemanticExtraction.src.ATR.CoNLLX.Document import Document
from SemanticExtraction.src.ATR.CoNLLX.Element import Element
from SemanticExtraction.src.ATR.CoNLLX.Sentence import Sentence
from SemanticExtraction.src.ATR.FormatError import FormatError
import codecs
import sys
import os

class CoNLLProcessing():
    def read_conll(self,conll_file_folder):
        conllx = CoNLLXHandle()
      #  dir = "../data/question/")
      #  inputdir = "../data/question/outmalt/"
        i = 0
        totalsentence = 0
        documents = []
        for name in os.listdir(conll_file_folder):
            f = os.path.join(conll_file_folder, name)
            conllx = CoNLLXHandle()
            sentences = conllx.read_conllx(f)
            document = []
            for sentence in sentences:
                document.append(sentence)
            documents.append(document)
        return documents


class CoNLLXHandle(object):

    metadata=[]

    def _file_name(self, file_like, default='document'):
        """return name of named file or file-like object, or default if not available"""
        # If given a string, assume that it's the name
        if isinstance(file_like, basestring):
            return file_like
        try:
            return file_like.name
        except AttributeError:
            return default

    def read_documents(self, source, filename=None):
        """Read CoNLL-X format, yielding Document Objects."""
        if filename is None:
            filename = self._file_name(source)
        current = Document(filename)
        for sentence in self.read_conllx(source, filename):
            #TODO: recognize and respect document boundaries in source data
            current.append(sentence)
        yield current



    def set_metadata(self,metadata):
        self.metadata = metadata

    def read_conllx(self,source, filename=None):
        """Read CoNLL-X format, yielding Sentence objects.
        Note: incomplte implementation, lacks validation.
        """
        #if given a string, assume it's a file name, open and recurse
        if isinstance(source, basestring):
            with codecs.open(source, encoding='utf-8') as i:
                for s in self.read_conllx(i, filename=source):
                    yield s
            return

        if filename is None:
            filename = self._file_name(source)

        sent_num, offset =1, 0
        current = Sentence(sent_num, filename, offset,self.metadata)
        for ln, line in enumerate(source):
            line = line.rstrip('\n')
            if not line:
                if not current.empty():
                    #Assume single character sentence separator
                    offset+=current.length()+1
                    yield current
                else:
                    raise FormatError('empty sentence', line, ln+1)
                sent_num+=1
                current = Sentence(sent_num, filename,offset,self.metadata)
            elif line[0] == '#':
                current.comments.append(line)
            else:
                try:
                    current.append(Element.from_string(line))

                except FormatError, e:
                    e.linenum = ln+1
                    raise e
        assert current.empty(), 'missing terminating whitespace'



cp = CoNLLProcessing()
documents = cp.read_conll("../data/question/outmalt/")
for document in documents:
    for sentence in document:
        print sentence.to_normal_sentence()