import sys
import os
from collections import deque
sys.path.append(os.path.join('resolution', 'resolution.jar'))


#from res.Main import * 
from res.frontend import *
from res.spectralsequencediagram import *
from res.spectralsequencediagram import DisplaySettings
from com.google.gson import *

from java.awt import Color, Shape
from java.awt.geom import Ellipse2D, Rectangle2D

color_dict = {'black' : Color.BLACK, 'blue' : Color.BLUE, 'green' : Color.GREEN, 'red' : Color.RED }
shape_dict = { 'Z' : Rectangle2D.Double( 0, 0, 12, 12) }

infinity = 10000

class PySseqClass(SseqClass):

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.class_structlines = []
        self.outgoing_differentials = []
        self.incoming_differentials = []
        self.class_name = ""
        self.extra_info = ""
        self.color = Color.BLACK
        self.class_page_list = [infinity]
        self.shape = Ellipse2D.Double( 0, 0, 6, 6)
        self.visible = True

    def getPage(self):
        return self.class_page_list[-1]

    def setPage(self,page):
        self.class_page_list[-1] = page
        return self
    
    def appendPage(self,page): 
        self.class_page_list.append(page)
        return self

    def getDegree(self):
        return [self.x,self.y]

    def getStructlines(self):
        return self.class_structlines

    def addStructline(self,sl):
        self.class_structlines.append(sl)
        return self

    def getOutgoingDifferentials(self):
        return self.outgoing_differentials

    def addOutgoingDifferential(self,differential):
        if self.getPage() < differential.page:
            self.setColor('red')
            if len(self.outgoing_differentials)>0:
                message = "Warning: class %r already %s, receiving another %s" %  \
                    (self, self.outgoing_differentials[-1].supportedMessage(), differential.supportedMessage())
            else: 
                message = "Warning: class %r already %s, receiving another %s" %  \
                    (self, self.incoming_differentials[-1].hitMessage(), differential.supportedMessage())
            self.extra_info += "\n" + message
            self.appendPage(infinity)
        self.setPage(differential.page)
        self.outgoing_differentials.append(differential)

    def addIncomingDifferential(self,differential):
        if self.getPage() < differential.page:
            self.setColor('red')
            if len(self.outgoing_differentials)>0:
                message = "Warning: class %r already %s, receiving another %s" %  \
                    (self, self.outgoing_differentials[-1].supportedMessage(), differential.hitMessage())
            else: 
                message = "Warning: class %r already %s, receiving another %s" %  \
                    (self, self.incoming_differentials[-1].hitMessage(), differential.hitMessage())   
            self.extra_info += "\n" + message
        self.setPage(differential.page)
        self.incoming_differentials.append(differential)
        
    def setShape(self,shape):
        if type(shape) is str:
            shape = shape_dict[shape]
        self.shape = shape
        return self

    def getShape(self,page):
        return self.shape

    def setExtraInfo(self,extra_info):
        self.extra_info = extra_info
        return self

    def extraInfo(self):
        return self.extra_info

    def setName(self,name):
        self.class_name = name
        return self

    def getName(self):
        return self.class_name

    def setColor(self,color):
        if type(color) is str:
            color = color_dict[color.lower().strip()]
        self.color = color
        return self

    def getColor(self,page):
        return self.color

    def toString(self):
        return self.getName()
        
    def drawOnPageQ(self,page):
        return self.page >= page

class PySseqStructline(Structline):
    def __init__(self,sourceClass,targetClass):
        self.sourceClass = sourceClass
        self.targetClass = targetClass
        self.thepage = 0

    def getSource(self):
        return self.sourceClass

    def getTarget(self):
        return self.targetClass

    def setPage(self,newPage):
        self.thepage = newPage
        return self

    def getPage(self):
        return self.thepage

    def getShape(self,page):
        return

    def getColor(self,page):
        return Color.BLACK

class PyDifferential(Differential):
    def __init__(self,sourceClass,targetClass,page):
        self.sourceClass = sourceClass
        self.targetClass = targetClass
        self.thepage = page
        self.color = Color.BLUE

    def getSource(self):
        return self.sourceClass

    def getTarget(self):
        return self.targetClass

    def getPage(self):
        return self.thepage

    def getColor(self,page):
        return self.color
        
    def hitMessage(self):
        return "hit on page %d by class %r" % (self.page, self.sourceClass)

    def supportedMessage(self):
        return "supported a differential on page %d hitting class %r" % (self.page, self.targetClass)
        
    def toString(self):
        return "d_{%d}( %s ) = %s" % (self.thepage,self.sourceClass,self.targetClass)


class Sseq(SpectralSequence):
   def __init__(self):
        self.update_viewer = lambda _ : True
        # class_degree_dictionary is a dictionary that indexes a bidegree into a list of classes
        self.class_degree_dictionary = { }
        self.class_stem_dictionary = { }
        self.class_list = []
        self.structlines = []
        self.differentials = []
        self.xshift = 0
        self.yshift = 0
        self.last_classes = deque([],4)

   def num_gradings(self):
        return 2

   def totalGens(self):
        return 0
   
   def set_shift(self,x,y):
        self.xshift = x
        self.yshift = y
        return self
   
   def add_to_shift(self,x,y):
        self.xshift += x
        self.yshift += y
        return self

   def addClass(self,x,y):
        x = x + self.xshift
        y = y + self.yshift
        the_sseq_class = PySseqClass(x,y)
        self.last_classes.appendleft(the_sseq_class)
        if (x,y) not in self.class_degree_dictionary:
            self.class_degree_dictionary[(x,y)] = []
        self.class_degree_dictionary[(x,y)].append(the_sseq_class)
        if x not in self.class_stem_dictionary:
            self.class_stem_dictionary[x] = []
        self.class_stem_dictionary[x].append(the_sseq_class)
        self.class_list.append(the_sseq_class)
        return the_sseq_class

   def addStructline(self, sourceClass = None, targetClass = None):
        if(sourceClass == None):
            sourceClass = self.last_classes[0]
            targetClass = self.last_classes[1]
        elif(targetClass == None):
            targetClass = self.last_classes[0]
        struct = PySseqStructline(sourceClass,targetClass)
        self.structlines.append(struct)
        sourceClass.addStructline(struct)
        return self
   
   def addStructlineSquare(self):
        self.addStructline(self.last_classes[0],self.last_classes[1])
        self.addStructline(self.last_classes[2],self.last_classes[3])
        self.addStructline(self.last_classes[0],self.last_classes[2])
        self.addStructline(self.last_classes[1],self.last_classes[3])


   def addDifferential(self,sourceClass,targetClass,page):
        differential = PyDifferential(sourceClass,targetClass,page)
        self.differentials.append(differential)
        sourceClass.addOutgoingDifferential(differential)
        targetClass.addIncomingDifferential(differential)
        return differential

   def getClasses(self, p=None, page=None):
       if p == None:
           return self.class_list
       else:
           q = (p[1] - p[0], p[0])
           if q in self.class_degree_dictionary:
                return filter(lambda c: c.visible, self.class_degree_dictionary[q])
           else:
                return []
            

   def getStructlines(self, page):
        return self.structlines

   def getDifferentials(self, page):
        return self.differentials

   def getTMax(self):
        return 50

   def getState(self,*args):
        return 4

   def addListener(self,l):
        self.update_viewer = l.ping

   def removeListener(self,l):
        return
