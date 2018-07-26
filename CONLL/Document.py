
class Document(object):
    def __init__(self, filename=None):
        self._sentences = []
        self.filename = filename

    def append(self, sentence):
        """Append sentence to document"""
        self._sentences.append(sentence)

    def empty(self):
        return self._sentences==[]

    def words(self):
        """Return a list of the words in the document."""
        return [w for s in self.sentences() for w in s.words()]

    def sentences(self):
        """Return a list of sentence in the document"""
        return self._sentences

    def text(self, use_tokens=False, element_separator=' ', sentence_separator='\n'):
        return sentence_separator.join(s.text(use_tokens, element_separator) for s in self.sentences())

    def to_brat_standoff(self):
        """Return list of brat standoff annotations for the document."""
        annotations = []
        for sentence in self._sentences:
            annotations.extend(sentence.to_brat_standoff())
        return annotations



