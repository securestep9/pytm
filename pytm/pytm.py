from pytm.threats import Threats

def uniq_name(s):
    ''' transform name in a unique(?) string '''
    return s.replace(' ', '_')


class Threat():
    BagOfThreats = []

    ''' Represents a possible threat '''
    def __init__(self):
        for t in Threats.keys():
            self.id = t
            self.description = Threats[t]["description"]
        self.cvss = Threats[t]["cvss"]
        self.condition = Threats[t]["condition"]
        self.target = Threats[t]["target"]

    def apply(self, target):
        if type(target) != self.target:
            return None
        return eval(self.condition)
        

class Finding():
    BagOfFindings = []

    def __init__(self, element, description, cvss):
        self.target = element
        self.description = description
        self.cvss = cvss


class Mitigation():

    def __init__(self, mitigatesWhat, mitigatesWhere, description):
        self.mitigatesWhat = mitigatesWhat
        self.mitigatesWhere = mitigatesWhere
        self.description = description


class TM():
    
    ''' Describes the threat model '''

    BagOfFlows = []
    BagOfElements = []
    BagOfThreats = Threat.BagOfThreats
    BagOfFindings = Finding.BagOfFindings

    def __init__(self, name, descr=""):
        self.name = name
        self.description = descr

    def set_description(self, descr):
        self.description = descr

    def resolve(self):
        for e in TM.BagOfElements + TM.BagOfFlows:
            for t in TM.BagOfThreats:
                if t.apply(e):
                    TM.BagOfFindings.append(Finding(e.name, t.description, t.cvss))
                        
    def dataflow(self):
        pass

    def report(self, *args, **kwargs):
        for f in TM.BagOfFindings:
            print("Finding: {} on {} with score {}".format(f.description, f.target, f.cvss))


class Element():
    counter = 0

    def __init__(self, name):
        Element.counter += 1
        self.name = name
        TM.BagOfElements.append(self)

    def set_description(self, descr):
        self.descr = descr

    def verify(self):
        ''' makes sure it is good to go '''
        # all minimum annotations are in place
        # then add itself to BagOfElements
        pass


class Server(Element):
    OS = ""
    hardened = False
    onAWS = False

    def __init__(self, name):
        super().__init__(name)
    pass


class Database(Element):
    onRDS = False
    pass


class Actor(Element):
    pass


class Process(Element):
    pass


class SetOfProcesses(Element):
    pass


class Dataflow():
    counter = 0

    def __init__(self, source, sink, name):
        Dataflow.counter += 1
        self.source = source
        self.sink = sink
        self.name = name
        self.protocol = ""
        self.dstPort = None
        self.authenticatedWith = None
        TM.BagOfFlows.append(self)

    def set_source(self, source):
        self.source = source

    def set_sink(self, sink, dstPort=None):
        self.sink = sink
        self.dstPort = dstPort

    def verify(self):
        ''' makes sure it is good to go '''
        # all minimum annotations are in place
        # then add itself to BagOfFlows
        pass
            
    @classmethod
    def count(cls):
        return len(TM.BagOfFlows)

