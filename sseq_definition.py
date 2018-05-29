import sys
import os
from collections import deque
#sys.path.append("..\\resolution\\resolution.jar")
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
style_dict = { 'Z' : { 'shape' : 'Z' }, 'Z/2' : { 'shape' : 'Z/2' } }

infinity = 10000

def addToDictionaryOfLists(dictionary, key,value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)



class Sseq(SpectralSequence):
   def __init__(self):
        self.update_viewer = lambda _ : True
        # class_degree_dictionary is a dictionary that indexes a bidegree into a list of classes
        self.total_gens = 0;
        self.class_degree_dictionary = { }
        self.class_stem_dictionary = { }
        self.class_list = []
        self.structlines = []
        self.differentials = []
        self.xshift = 0
        self.yshift = 0
        self.last_classes = deque([],4)
        self.page_list = [0,infinity]
   
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
        self.total_gens = self.total_gens + 1
        addToDictionaryOfLists(self.class_degree_dictionary, (x,y), the_sseq_class)
        addToDictionaryOfLists(self.class_stem_dictionary,       x, the_sseq_class)
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
        if page <= 0:
            print("No page <= 0 differentials allowed.")
            return
        differential = PyDifferential(sourceClass,targetClass,page)
        self.differentials.append(differential)
        sourceClass.addOutgoingDifferential(differential)
        targetClass.addIncomingDifferential(differential)
        if page not in self.page_list:
            self.addPageToPageList(page)
        return differential
        
   def addPageToPageList(self,page):
        for i in range(0, len(self.page_list)):
            if(self.page_list[i] > page):
                self.page_list.insert(i, page)
                break


   def getClasses(self, p=None, page=None):
       if p == None:
           return self.class_list
       else:
           q = (p[1] - p[0], p[0])
           if q in self.class_degree_dictionary:
                return filter(lambda c: c.visible, self.class_degree_dictionary[q])
           else:
                return []
            

   # Java interface methods below here.
   def getPageList(self):
        return self.page_list
   
   def num_gradings(self):
        return 2

   def totalGens(self):
        return total_gens

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
