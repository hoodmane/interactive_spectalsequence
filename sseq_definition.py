import sys
import os
from collections import deque
sys.path.append("..\\resolution\\resolution.jar")
sys.path.append(os.path.join('resolution', 'resolution.jar'))

from sseq_class import *
from sseq_edges import *

from res.frontend import *
from res.spectralsequencediagram import *
from res.spectralsequencediagram.nodes import *

from java.awt import Color, Shape
from java.awt.geom import Ellipse2D, Rectangle2D

from contextlib import contextmanager
# The important thing about cStringIO is that it "doesn't handle Unicode". Turns out StringIO doesn't handle normal strings...
import cStringIO 
from itertools import product

@contextmanager
def redirect_stdout(new_target):
    old_target, sys.stdout = sys.stdout, new_target # replace sys.stdout
    try:
        yield new_target # run some code with the replaced stdout
    finally:
        sys.stdout = old_target # restore to the previous value

infinity = 10000

def addToDictionaryOfLists(dictionary, key,value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)
    
def monomialString(vars, exponents):
    out = [None] * len(vars)
    for i in range(0,len(vars)):
        if(exponents[i]==0):
            out[i] = ""
        elif(exponents[i]==1):
            out[i] = vars[i]
        else:
            out[i] = vars[i] + "^" + str(exponents[i])
    outStr = " ".join(filter(lambda s: s != "",out))
    if outStr == "":
        outStr = "1"
    return outStr

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
        self.default_node = CircleNode()
   
   def setInterpreter(self, interpreter):
        self.interpreter = interpreter
   
   def setDefaultStyle(self, node):
        if type(node) is str:
            if node not in node_dict:
                print("Unknown node type %s, ignoring it")
            node = node_dict[node]
        self.default_node  = node
        return self
   
   def set_shift(self, x, y):
        self.xshift = x
        self.yshift = y
        return self
   
   def add_to_shift(self, x, y):
        self.xshift += x
        self.yshift += y
        return self

   def addClass(self, x, y):
        x = x + self.xshift
        y = y + self.yshift
        the_sseq_class = PySseqClass(self, x, y)
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


   def addDifferential(self, sourceClass, targetClass, page):
        if page <= 0:
            print("No page <= 0 differentials allowed.")
            return
        differential = PyDifferential(sourceClass, targetClass, page)
        self.differentials.append(differential)
        if page not in self.page_list:
            self.addPageToPageList(page)
        return differential
        
   def addPageToPageList(self, page):
        for i in range(0, len(self.page_list)):
            if(self.page_list[i] > page):
                self.page_list.insert(i, page)
                break


   def getClasses(self, *args):
       if len(args) == 0:
            return self.class_list
       elif len(args) == 1:
            p = args[0]
            page = 1000
       elif len(args) == 2:
            p = args[0]
            page = args[1]
       elif len(args) == 3:
            p = (args[0], args[1])
            page = args[2]
       else:
            print("Too many arguments")
            return
       if p in self.class_degree_dictionary:
            return filter(lambda c: c.visible, self.class_degree_dictionary[p])
       else:
            return []
            
   def getCycles(self, p=None, page=1000):
        return filter(lambda c: c.getPage()>page,self.getClasses(p) )
        
   # Input:
   #    var_degree_dict: a dictionary of the form varname : (stem_degree, filtration)
   #    var_spec_list: a list of lists or tuples [varname, min, max, step].
   # If step is missing, it defaults to 1, if min is missing it defaults to 0.
   # Like python, max is max + 1.
   def addPolynomialClasses(self,var_degree_dict,var_spec_list):
        var_name_list = []
        stem_list = []
        filtration_list = []
        range_list = [] 
        class_dict = monomial_basis(self)
        
        for var_spec in var_spec_list:
            var_name = var_spec[0]
            var_name_list.append(var_name)
            stem_list.append(var_degree_dict[var_name][0])
            filtration_list.append(var_degree_dict[var_name][1])
            range_list.append(range(*var_spec[1:]))
            
        for monomial_exponents in product(*range_list):
            stem = sum(p*q for p,q in zip(monomial_exponents, stem_list))
            filtration = sum(p*q for p,q in zip(monomial_exponents, filtration_list))
            name = monomialString(var_name_list,monomial_exponents)
            class_dict._add_class(monomial_exponents, name, self.addClass(stem,filtration).setName(name))
        return class_dict
        
   # 

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

   def getState(self, *args):
        return 4

   def addListener(self, l):
        self.update_viewer = l.ping

   def removeListener(self, l):
        return

   # See https://stackoverflow.com/questions/22425453/redirect-output-from-stdin-using-code-module-in-python
   # Ugh Python docs suck.
   # So at some point they changed io.StringIO so that it will ONLY accept unicode strings.
   # Unfortunately, the interpreter writes ascii to stdout, and then StringIO gets mad because it's not unicode.
   # This is retarded. Anyways cStringIO accepts ascii.
   def executeJython(self, command, callback):
        f = cStringIO.StringIO()
        with redirect_stdout(f):    
            if(not self.interpreter.push(command)):
                callback.run(f.getvalue())


# tuples but + means add elementwise and * means multiply by scalar.
# Note: multiplying on the left by an integer does the wrong thing...
class vector_tuple(tuple):
    def __new__(cls, *args):
        return tuple.__new__(cls, args)
    
    def __add__(self, other):
        return vector_tuple(*([sum(x) for x in zip(self, other)]))
    
    def __sub__(self, other):
        return self.__add__(-i for i in other)
    
    def __mul__(self, n):
        return vector_tuple(*[n*x for x in self])
                
   
class monomial_basis:
    
    def __init__(self,sseq):
        self.sseq = sseq
        self._tuples_to_classes = {}
        self._strings_to_classes = {}
        self._tuples_to_strings = {}
        
    def _add_class(self, tuple, name, the_class):
        tuple = vector_tuple(*tuple)
        self._tuples_to_classes[tuple] = the_class
        self._strings_to_classes[name] = the_class
        self._tuples_to_strings[tuple] = name
    
    def addStructline(self, *vect):
        vect = vector_tuple(*vect)
        for k in self.keys():
            if k + vect in self:
                self.sseq.addStructline(self[k], self[k + vect])
                
    def addDifferential(self, page, target_vect, cond, callback = None):
        target_vect = vector_tuple(*target_vect)
        for k in self.keys():
            if cond(k):
                if k + target_vect in self:
                    d = self.sseq.addDifferential(self[k], self[k + target_vect], page)
                    if callback:
                        callback(d)
                else:
                    if self[k].getPage()> page:
                        self[k].setPage(page)
    
    # standard immutable dictionary methods:        
    def __getitem__(self, key): 
        if key in self._tuples_to_classes:
            return self._tuples_to_classes[key]
        if key in self._strings_to_classes:
            return self._strings_to_classes[key]        
        raise KeyError()
        
    def __len__(self):
        return len(_tuples_to_classes)
    
    def __iter__(self):
        return iter(self._tuples_to_classes)
    
    def __contains__(self, item):
        return (item in self._tuples_to_classes) or (item in self._strings_to_classes)
    
    def keys(self): 
        return self._tuples_to_classes.keys()
        
    def values(self):
        return self._tuples_to_classes.values()
        
    def items(self):
        return [(tup, self._tuples_to_strings[tup], self._tuples_to_classes[tup]) for tup in self._tuples_to_classes.keys()]
    
    def get(self, key, default_value = None):
        if key in self._tuples_to_classes:
            return self._tuples_to_classes[key]
        if key in self._strings_to_classes:
            return self._strings_to_classes[key]        
        return default_value         
    
    
            
