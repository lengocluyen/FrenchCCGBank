class NodeInfo:
    def __init__(self, label, ccgtag=None, element=None, dependency=None, cluster=None):
        self.label = label
        self.ccgTag = ccgtag
        self.element = element
        self.dependency = dependency
        self.cluster = cluster