import re
from six import string_types


class Annotation(object):
    """Base class for annotation with ID and type."""

    def __init__(self,id_, type_):
        self.id = id_
        self.type=type_

    def verify_text(self,text):
        """Verify reference text for textbound annotations."""
        pass

    def __unicode__(self):
        raise NotImplementedError

    STANDOFF_RE = None

    @classmethod
    def from_standoff(cls, line):
        if cls.STANDOFF_RE is None:
            raise NotImplementedError
        m = cls.STANDOFF_RE.match(line)
        if not m:
            raise ValueError('Failed to parse "$s' % line)
        return cls(*m.groups())

class Attribute(Annotation):
    """Attribute with optional value associated with another annotation."""

    def __init__(self, id_, type_, arg, val):
        super(Attribute, self).__init__(id_, type_)
        self.arg = arg
        self.val = val

    def __unicode__(self):
        if not self.val:
            return '%s\t%s %s' % (self.id, self.type, self.arg)
        else:
            return '%s\t%s %s %s' % (self.id, self.type, self.arg, self.val)

    STANDOFF_RE = re.compile(r'^(\S+)\t(\S+) (\S+) ?(\S*)$')

class TextBound(Annotation):
    """Textbound annotation representing entity mention or event trigger."""

    def __init__(self, id_, type_, spans, text):
        super(TextBound, self).__init__(id_,type_)
        if isinstance(spans, string_types):
            self.spans = TextBound.parse_spans(spans)
        else:
            self.spans = spans
        self.text = text

    def verify_text(self,text):
        offset = 0
        for start, end in self.spans:
            endoff = offset + (end - start)
            assert text[start:end] == self.text[offset:endoff], \
                'Error: text mismatch: "%s" vs. "%s"' % \
                (text[start:end], self.text[offset:endoff])
            offset = endoff + 1

    def __unicode__(self):
        span_str = u';'.join(u'%d %d' % (s[0], s[1]) for s in self.spans)
        return u'%s\t%s %s\t%s' % (self.id, self.type, span_str, self.text)

    @staticmethod
    def parse_spans(span_string):
        """Return list of (start, end) pairs for given span string."""
        spans = []
        for span in span_string.split(';'):
            start, end = span.split(' ')
            spans.append((int(start), int(end)))
        return spans


class Comment(Annotation):
    """Typed free-form text comment associated with another annotation."""

    def __init__(self, id_, type_, arg, text):
        super(Comment, self).__init__(id_, type_)
        self.arg = arg
        self.text = text

    def __unicode__(self):
        return '%s\t%s %s\t%s' % (self.id, self.type, self.arg, self.text)

    STANDOFF_RE = re.compile(r'^(\S+)\t(\S+) (\S+)\t(.*)$')