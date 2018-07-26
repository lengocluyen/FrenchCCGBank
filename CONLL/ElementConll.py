import re
from CONLL.FormatError import FormatError
from CONLL.Annotation import TextBound, Attribute, Comment

from itertools import groupby

#feature name-value sperator

FSEP = '='
#dependency head-rel separator
DSEP = ':'

#Free-form text annotation type in brat
COMMENT_TYPE = 'AnnotatorNotes'

UPOSTAG_RE = re.compile(r'^[a-zA-Z]+$')
XPOSTAG_RE = re.compile(r'^[\x20-\xff]+$')

class ElementConllQ(object):
    """Prepresents CoNN-X word or multi-word token."""

    def __init__(self,id_, form, lemma, upostag, xpostag, feats, cluster, head, deprel, deps, misc, offset=0):
        self.id = id_
        self.form = form
        self.lemma = lemma
        self.upostag = upostag
        self.xpostag = xpostag
        self._feats = feats
        self.cluster = cluster
        self.head = head
        self.deprel = deprel
        self.deps = deps
        self.misc = misc

        self.offset = offset
        self.sentence = None

        self._fmap = None
        self._dlist = None

    def validate(self):
        #minimal format validation (incomplete)
        if not self.is_word():
            #TODO: check multi-word tokens
            return

        #some character set constraints
        if not UPOSTAG_RE.match(self.upostag):
            raise FormatError('invalid UPOSTAG: %s' % self.upostag)
        if not XPOSTAG_RE.match(self.xpostag):
            raise FormatError('invalid XPOSTAG: %s' % self.xpostag)

        #no feature is empty
        if any(True for s in self._feats if len(s)==0):
            raise FormatError('empty feature: %s' % str(self._feats))

        #feature names and values separated by feature separator:
        if any(s for s in self._feats if len(s.split(FSEP))<2):
            raise FormatError('invalid features: %s' % str(self._feats))

        #no feate name repeats
        if any(n for n, g in groupby(sorted(s.split(FSEP)[0] for s in self._feats)) if len(list(g))>1):
            raise FormatError('duplicate features: %s' % str(self._feats))

        #head is integer
        try:
            int (self.head)
        except ValueError:
            raise FormatError('non-int head: %s' % self.head)

    def is_word(self):
        try:
            val = int(self.id)
            if val and self.form.strip() is not ".":
                return True
            return False
        except ValueError:
            return False

    def has_feat(self, name):
        return name in self.feat_map()

    def add_feats(self,feats):
        #name-value pairs
        assert not any (nv for nv in feats if len(nv) != 2)
        self._feats.extend(FSEP.join(nv) for nv in feats)
        self._fmap = None

    def set_feats(self, feats):
        self._feats=[]
        self.add_feats(feats)
        self._fmap = None

    def remove_feat(self, name, value):
        nv = FSEP.join((name,value))
        self._feats.remove(nv)
        self._fmap = None

    def feat_names(self):
        return [f.split(FSEP)[0] for f in self._feats]

    def feat_map(self):
        if self._fmap is None:
            try:
                self._fmap = dict([f.split(FSEP,1) for f in self._feats])
            except ValueError:
                raise ValueError('failed to convert ' + str(self._feats))
        return self._fmap

    def feats(self):
        return self.feat_map().items()

    def has_deprel(self, deprel, check_deps=True):
        if self.deprel == deprel:
            return True
        elif not check_deps:
            return False
        elif any (d for d in self.deps() if d[1] == deprel):
            return True
        else:
            return False

    def wipe_annotation(self):
        self.lemma = '_'
        self.upostag = '_'
        self.xpostag = '_'
        self._feats='_'
        self.head='_'
        self.deprel='_'
        self.deps='_'
        self.misc = '_'

    def to_brat_standoff(self, element_by_id):
        """Return list of brat standoff annotations for the element."""
        #base ID, unique within the document
        bid = '%s.%s' %(self.sentence.id, self.id)
        if self.is_word():
            #Word, maps to: Textbound with the coarse POS tag as type, freeform text comment with LEMMA, UPOSTAG and ????
            span = [[self.offset, self.offset + len(self.form)]]
            textbounds = [
                TextBound('T'+bid, self.xpostag, span, self.form),
            ]
            # comments
            freeform = [
                ('LEMMA', self.lemma),
                ('UPOSTAG', self.upostag),
            ]
            # attributes
            attribs = []
            for name, value in self.feats():
                aid = 'A' + bid + '-%d' % (len(attribs) + 1)
                attribs.append(Attribute(aid, name, 'T' + bid, value))
            return textbounds + attribs # + relations + comments
        else:
            # Multi-word token, maps to: Textbound with a special type,
            # and free-text comment containing the form.
            # Span corresponds to maximum span over covered tokens.
            start, end = self.id.split('-')
            first, last = element_by_id[start], element_by_id[end]
            spans = [[first.offset, last.offset + len(last.form)]]
            text = ' '.join(str(element_by_id[str(t)].form)
                            for t in range(int(start), int(end) + 1))
            return [
                TextBound('T' + bid, 'Multiword-token', spans, text),
                Comment('#' + bid, COMMENT_TYPE, 'T' + bid, 'FORM=' + self.form)
            ]

    def __unicode__(self):
        fields = [self.id, self.form, self.lemma, self.upostag, self.xpostag, self._feats, self.head, self.deprel, self.deps, self.misc]
        fields[5] = '_' if fields[5] == [] else '|'.join(sorted(fields[5], key=lambda s: s.lower())) # feats
        return '\t'.join(fields)



    @classmethod
    def from_string(cls, s):
        fields = s.split('\t')
        #for question corpus len(fields)=11, for FTB len(fields)=10
        if len(fields)!=11:
            raise FormatError('got %s/10 field(s) for Data format CoNLL-X' % len(fields), s)
        fields[5] = [] if fields[5] == '_' else fields[5].split('|') # feats
        return cls(*fields)

#class ElementConllFTB(object):
class ElementConll(object):
    """Prepresents CoNN-X word or multi-word token."""

    def __init__(self,id_, form, lemma, upostag, xpostag, feats, head, deprel, deps, misc, offset=0):
        self.id = id_
        self.form = form
        self.lemma = lemma
        self.upostag = upostag
        self.xpostag = xpostag
        self._feats = feats
        self.head = head
        self.deprel = deprel
        self.deps = deps
        self.misc = misc

        self.offset = offset
        self.sentence = None

        self._fmap = None
        self._dlist = None

    def validate(self):
        #minimal format validation (incomplete)
        if not self.is_word():
            #TODO: check multi-word tokens
            return

        #some character set constraints
        if not UPOSTAG_RE.match(self.upostag):
            raise FormatError('invalid UPOSTAG: %s' % self.upostag)
        if not XPOSTAG_RE.match(self.xpostag):
            raise FormatError('invalid XPOSTAG: %s' % self.xpostag)

        #no feature is empty
        if any(True for s in self._feats if len(s)==0):
            raise FormatError('empty feature: %s' % str(self._feats))

        #feature names and values separated by feature separator:
        if any(s for s in self._feats if len(s.split(FSEP))<2):
            raise FormatError('invalid features: %s' % str(self._feats))

        #no feate name repeats
        if any(n for n, g in groupby(sorted(s.split(FSEP)[0] for s in self._feats)) if len(list(g))>1):
            raise FormatError('duplicate features: %s' % str(self._feats))

        #head is integer
        try:
            int (self.head)
        except ValueError:
            raise FormatError('non-int head: %s' % self.head)

    def is_word(self):
        try:
            val = int(self.id)
            if val and self.form.strip() is not ".":
                return True
            return False
        except ValueError:
            return False

    def has_feat(self, name):
        return name in self.feat_map()

    def add_feats(self,feats):
        #name-value pairs
        assert not any (nv for nv in feats if len(nv) != 2)
        self._feats.extend(FSEP.join(nv) for nv in feats)
        self._fmap = None

    def set_feats(self, feats):
        self._feats=[]
        self.add_feats(feats)
        self._fmap = None

    def remove_feat(self, name, value):
        nv = FSEP.join((name,value))
        self._feats.remove(nv)
        self._fmap = None

    def feat_names(self):
        return [f.split(FSEP)[0] for f in self._feats]

    def feat_map(self):
        if self._fmap is None:
            try:
                self._fmap = dict([f.split(FSEP,1) for f in self._feats])
            except ValueError:
                raise ValueError('failed to convert ' + str(self._feats))
        return self._fmap

    def feats(self):
        return self.feat_map().items()

    def has_deprel(self, deprel, check_deps=True):
        if self.deprel == deprel:
            return True
        elif not check_deps:
            return False
        elif any (d for d in self.deps() if d[1] == deprel):
            return True
        else:
            return False

    def wipe_annotation(self):
        self.lemma = '_'
        self.upostag = '_'
        self.xpostag = '_'
        self._feats='_'
        self.head='_'
        self.deprel='_'
        self.deps='_'
        self.misc = '_'

    def to_brat_standoff(self, element_by_id):
        """Return list of brat standoff annotations for the element."""
        #base ID, unique within the document
        bid = '%s.%s' %(self.sentence.id, self.id)
        if self.is_word():
            #Word, maps to: Textbound with the coarse POS tag as type, freeform text comment with LEMMA, UPOSTAG and ????
            span = [[self.offset, self.offset + len(self.form)]]
            textbounds = [
                TextBound('T'+bid, self.xpostag, span, self.form),
            ]
            # comments
            freeform = [
                ('LEMMA', self.lemma),
                ('UPOSTAG', self.upostag),
            ]
            # attributes
            attribs = []
            for name, value in self.feats():
                aid = 'A' + bid + '-%d' % (len(attribs) + 1)
                attribs.append(Attribute(aid, name, 'T' + bid, value))
            return textbounds + attribs # + relations + comments
        else:
            # Multi-word token, maps to: Textbound with a special type,
            # and free-text comment containing the form.
            # Span corresponds to maximum span over covered tokens.
            start, end = self.id.split('-')
            first, last = element_by_id[start], element_by_id[end]
            spans = [[first.offset, last.offset + len(last.form)]]
            text = ' '.join(str(element_by_id[str(t)].form)
                            for t in range(int(start), int(end) + 1))
            return [
                TextBound('T' + bid, 'Multiword-token', spans, text),
                Comment('#' + bid, COMMENT_TYPE, 'T' + bid, 'FORM=' + self.form)
            ]

    def __unicode__(self):
        fields = [self.id, self.form, self.lemma, self.upostag, self.xpostag, self._feats, self.head, self.deprel, self.deps, self.misc]
        fields[5] = '_' if fields[5] == [] else '|'.join(sorted(fields[5], key=lambda s: s.lower())) # feats
        return '\t'.join(fields)



    @classmethod
    def from_string(cls, s):
        fields = s.split('\t')
        if len(fields)!=10:
            raise FormatError('got %s/10 field(s) for Data format CoNLL-X' % len(fields), s)
        fields[5] = [] if fields[5] == '_' else fields[5].split('|') # feats
        return cls(*fields)





