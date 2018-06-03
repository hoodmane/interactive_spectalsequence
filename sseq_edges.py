from res.spectralsequencediagram import *

infinity = 10000
from java.awt import Color, Shape

class PySseqStructline(Structline):
    def __init__(self, sourceClass, targetClass):
        self.sourceClass = sourceClass
        self.targetClass = targetClass
        self.thepage = 0

    # Java Methods:
    def getSource(self):
        return self.sourceClass

    def getTarget(self):
        return self.targetClass

    def setPage(self, newPage):
        self.thepage = newPage
        return self

    def getPage(self):
        return self.thepage

    def getShape(self, page):
        return

    def getColor(self, page):
        return Color.BLACK
        
        
        
class PyDifferential(Differential):
    def __init__(self, sourceClass, targetClass, page):
        self.sourceClass = sourceClass
        self.targetClass = targetClass
        self.thepage = page
        self.color = Color.BLUE
        sourceClass.addOutgoingDifferential(self)
        targetClass.addIncomingDifferential(self)

    def setKernel(self, nodeStyle):
        self.sourceClass.replace(nodeStyle)
        return self

    def setCokernel(self, nodeStyle):
        self.targetClass.replace(nodeStyle)
        return self

    def replaceSource(self, nodeStyle):
        self.setKernel(nodeStyle)
        return self

    def replaceTarget(self, nodeStyle):
        self.setCokernel(nodeStyle)
        return self

    def hitMessage(self):
        return "hit on page %d by class %r" % (self.page, self.sourceClass)

    def supportedMessage(self):
        return "supported a differential on page %d hitting class %r" % (self.page, self.targetClass)

    def addInfoToSourceAndTarget(self):
        self.sourceClass.addExtraInfo(str(self))
        self.targetClass.addExtraInfo(str(self))
        return self

    # Java methods:
    def getSource(self):
        return self.sourceClass

    def getTarget(self):
        return self.targetClass

    def getPage(self):
        return self.thepage

    def getColor(self, page):
        return self.color

    def toString(self):
        return "d_{%d}( %s ) = %s" % (self.thepage,self.sourceClass,self.targetClass)



