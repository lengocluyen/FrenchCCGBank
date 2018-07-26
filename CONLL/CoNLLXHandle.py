from CONLL.Document import Document
from CONLL.Sentence import Sentence
from CONLL.FormatError import FormatError
from CONLL.ElementConll import ElementConll
from six import string_types
import codecs

class CoNLLXHandle(object):

    metadata=[]

    def _file_name(self, file_like, default='document'):
        """return name of named file or file-like object, or default if not available"""
        # If given a string, assume that it's the name
        if isinstance(file_like, string_types):
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
        if isinstance(source, string_types):
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
                    current.append(ElementConll.from_string(line))

                except FormatError as e:
                    e.linenum = ln+1
                    raise e
        assert current.empty(), 'missing terminating whitespace'
