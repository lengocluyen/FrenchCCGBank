
class FormatError(Exception):
    def __init__(self, msg, line=None, linenum=None):
        self.msg = msg
        self.line = line
        self.linenum = linenum

    def __str__(self):
        msg = self.msg
        if self.line is not None:
            msg += ': "' + self.line.encode('ascii','replace') + '"'
        if self.linenum is not None:
            msg += ' (line %d)' % self.linenum
        return msg