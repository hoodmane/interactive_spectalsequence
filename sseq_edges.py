from res.spectralsequencediagram import *

infinity = 10000
from java.awt import Color, Shape

class PySseqStructline(Structline):
    def __init__(self, source_class, target_class):
        self.source_class = source_class
        self.target_class = target_class
        self.the_page = 0

    # Java Methods:
    def getSource(self):
        return self.source_class

    def getTarget(self):
        return self.target_class

    def setPage(self, newPage):
        self.the_page = newPage
        return self

    def getPage(self):
        return self.the_page

    def getShape(self, page):
        return

    def getColor(self, page):
        return Color.BLACK
        
        
        
class PyDifferential(Differential):
    def __init__(self, source_class, target_class, page):
        self.source_class = source_class
        self.target_class = target_class
        self.the_page = page
        self.color = Color.BLUE
        source_class.addOutgoingDifferential(self)
        target_class.addIncomingDifferential(self)
        self.sourceName = str(self.source_class)
        self.targetName = str(self.target_class)

    def setKernel(self, nodeStyle):
        self.source_class.replace(nodeStyle)
        return self

    def setCokernel(self, nodeStyle):
        self.target_class.replace(nodeStyle)
        return self

    def replaceSource(self, nodeStyle):
        self.setKernel(nodeStyle)
        return self

    def replaceTarget(self, nodeStyle):
        self.setCokernel(nodeStyle)
        return self
        
    def setSourceName(self, name):
        self.source_name = name
        return self
    
    def setTargetName(self, name):
        self.target_name = name
        return self

    def hitMessage(self):
        return "hit on page %d by class %r" % (self.page, self.source_class)

    def supportedMessage(self):
        return "supported a differential on page %d hitting class %r" % (self.page, self.target_class)

    def addInfoToSourceAndTarget(self):
        self.source_class.addExtraInfo(str(self))
        self.target_class.addExtraInfo(str(self))
        return self

    # Java methods:
    def getSource(self):
        return self.source_class

    def getTarget(self):
        return self.target_class

    def getPage(self):
        return self.the_page

    def getColor(self, page):
        return self.color

    def toString(self):
        return "d_{%d}( %s ) = %s" % (self.the_page,self.source_class,self.target_class)



