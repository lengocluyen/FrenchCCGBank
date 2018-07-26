import re
from CONLL import ElementConll
import codecs
from itertools import groupby
import graphviz
import asciitree
from collections import defaultdict


class Sentence(object):

    metadata=[]
    def __init__(self, id_=0, filename=None, base_offset=0,metadata=None):
        """Initialize a new, empty Sentence."""
        self.metadata = metadata
        self.comments = []
        self._elements = []
        self.id = id_
        self.filename = filename
        self.base_offset = base_offset
        self.next_offset = base_offset
        # mapping from IDs to elements
        self._element_by_id = None


    def set_metadata(self,metadata):
        self.metadata = metadata

    def append(self, element):
        """Append word or multi-word token to sentence."""
        self._elements.append(element)
        assert element.sentence is None, 'element in multiple sentences?'
        element.sentence = self
        element.offset = self.next_offset
        if element.is_word():
            self.next_offset += len(element.form) + 1
        else:
            # multi-word token; don't shift position of next token
            pass
        # reset cache (TODO: extend instead)
        self._element_by_id = None

    def empty(self):
        return self._elements == []

    def words(self):
        """Return a list of the words in the sentence."""
        return [e for e in self._elements if e.is_word()]

    def text(self, use_tokens=False, separator=' '):
        """Return the text of the sentence."""
        if use_tokens:
            raise NotImplementedError('multi-word token text not supported.')
        else:
            return separator.join(w.form for w in self.words())

    def length(self, use_tokens=False):
        """Return the length of the sentence text."""
        return len(self.text(use_tokens))

    def element_by_id(self):
        """Return mapping from id to element."""
        if self._element_by_id is None:
            self._element_by_id = {e.id: e for e in self._elements}
        return self._element_by_id

    def get_element(self, id_):
        """Return element by id."""
        return self.element_by_id()[id_]

    def wipe_annotation(self):
        for e in self._elements:
            if e.is_word():
                e.wipe_annotation()

    def remove_element(self, id_):
        # TODO: implement for cases where multi-word tokens span the
        # element to remove.
        assert len(self.words()) == len(self._elements), 'not implemented'

        # there must not be references to the element to remove
        for w in self.words():
            assert not any(h for h, d in w.deps(True) if h == id_), \
                'cannot remove %s, references remain' % id_

        # drop element
        element = self.get_element(id_)
        self._elements.remove(element)
        self._element_by_id = None

        # update IDs
        id_map = {u'0': u'0'}
        for i, w in enumerate(self.words()):
            new_id = str(i + 1, 'utf-8')
            id_map[w.id] = new_id
            w.id = new_id
        for w in self.words():
            w.head = id_map[w.head]
            w.set_deps([(id_map[h], d) for h, d in w.deps()])

    def dependents(self, head, include_secondary=True):
        if isinstance(head, ElementConll):
            head_id = head.id

        deps = []
        for w in self.words():
            if not include_secondary:
                wdeps = [(w.head, w.deprel)]
            else:
                wdeps = w.deps(include_primary=True)
            for head, deprel in wdeps:
                if head == head_id:
                    deps.append((w.id, deprel))
        return deps

    def assign_offsets(self, base_offset=None, use_tokens=False):
        """Assign offsets to sentence elements."""
        if base_offset is not None:
            self.base_offset = base_offset
        offset = self.base_offset
        if use_tokens:
            raise NotImplementedError('multi-word token text not supported.')
        else:
            # Words are separated by a single character and multi-word
            # tokens appear at the start of the position of their
            # initial words with zero-width spans.
            for e in self._elements:
                e.offset = offset
                if e.is_word():
                    offset += len(e.form) + 1

    def to_brat_standoff(self):
        """Return list of brat standoff annotations for the sentence."""
        # Create mapping from ID to element.
        annotations = []
        for element in self._elements:
            annotations.extend(element.to_brat_standoff(self.element_by_id()))
        return annotations

    def find_root_node(self):
        root ='root'
        for mot in self.words():
            if mot.deprel is root:
                return mot.form
        return root


    def as_dotgraph(self, digraph_kwargs=None, id_prefix=None, node_formatter=None, edge_formatter=None):
        digraph_kwargs = digraph_kwargs or {}
        id_prefix = id_prefix or ''

        node_formatter = node_formatter or (lambda element: {})
        edge_formatter = edge_formatter or (lambda element: {})

        graph = graphviz.Digraph(**digraph_kwargs)
        #add root node
       # graph.node(id_prefix + '0', 'root',**node_formatter(None))
        #add remaining nodes and edges
        already_added = set()
        for element in self._elements:
            element_id = id_prefix + str(element.id)
            parent_id = id_prefix + str(element.head)
            if element_id not in already_added:
                graph.node(element_id, element.form + "\n ["+element.upostag+"]"+ "\n [ id : "+element.id+"]"+ "\n [ head : "+element.head+"]", **node_formatter(element))
            if parent_id is not '0':
                graph.edge(parent_id, element_id, label=element.deprel, **edge_formatter(element))
            already_added.add(element_id)
        return graph

    

    def to_normal_sentence(self):
        str=""
        for word in self._elements:
            lemma = word.form
            str+=lemma + " "
        return str

    def to_normal_sentence_form(self):
        str=""
        for word in self._elements:
            form = word.form
            str+=form + " "
        return str

    def to_normal_sentence_form_with_postag(self):
        str=""
        for word in self._elements:
            form = word.form
            str+=form + " "
        str +="\n"
        for word in self._elements:
            form = word.upostag
            str += form + "_"
        for word in self._elements:
            form = word.xpostag
            str += form + "_"
        return str

    def __unicode__(self):
        element_unicode = [str(e, 'utf-8') for e in self._elements]
        return '\n'.join(self.comments + element_unicode) + '\n'