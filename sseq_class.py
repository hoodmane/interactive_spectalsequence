from res.spectralsequencediagram import *
from java.awt import Color, Shape
from java.awt.geom import Ellipse2D, Rectangle2D
from style import *

import copy

infinity = 10000

class PySseqClass(SseqClass):
    def __init__(self, sseq, x, y):
        self.sseq = sseq
        self.x = x
        self.y = y
        self.class_structlines = []
        self.outgoing_differentials = []
        self.incoming_differentials = []
        self.class_name = ""
        self.extra_info = ""
        self.color = Color.BLACK
        self.page_list = [infinity]
        self.node_list = [self.sseq.default_node.copy()]
        self.visible = True


    def appendPage(self, page):
        self.page_list.append(page)
        self.node_list.append(self.sseq.default_node)
        return self

    def replace(self, node):
        self.appendPage(infinity)
        if type(node) is str:
            node = node_dict[node].copy()
        self.node_list[-1] = node
        return self

    def addStructline(self, sl):
        self.class_structlines.append(sl)
        return self

    def getOutgoingDifferentials(self):
        return self.outgoing_differentials

    def addOutgoingDifferential(self, differential):
        if self.getPage() < differential.page:
            self.handleDoubledDifferential("supporting another" + differential.supportedMessage())
        self.setPage(differential.page)
        self.outgoing_differentials.append(differential)

    def addIncomingDifferential(self, differential):
        if self.getPage() < differential.page:
            self.handleDoubledDifferential("receiving another" + differential.hitMessage())
        self.setPage(differential.page)
        self.incoming_differentials.append(differential)

    def handleDoubledDifferential(self, d_message):
        self.setColor('red')
        if len(self.outgoing_differentials)>0:
            message = "Warning: class %r already %s, %s" %  \
                (self, self.outgoing_differentials[-1].supportedMessage(), d_message)
        else:
            message = "Warning: class %r already %s, %s" %  \
                (self, self.incoming_differentials[-1].hitMessage(), d_message)
        self.extra_info += "\n" + message
        self.appendPage(infinity)

    def setExtraInfo(self, extra_info):
        self.extra_info = extra_info
        return self
        
    def addExtraInfo(self, str):
        self.extra_info += str + "\n"
        return self

    def getPageIndex(self, page):
        for idx, cur_page in enumerate(self.page_list):
            if(cur_page >= page):
                return idx
        # Assumption failure
        return len(self.page_list)

    # Java methods:
    def getDegree(self):
        return [self.x, self.y]

    def getStructlines(self):
        return self.class_structlines

    def getPage(self):
        return self.page_list[-1]

    def setPage(self, page):
        self.page_list[-1] = page
        return self

    def extraInfo(self):
        return self.extra_info

    def getName(self):
        return self.class_name

    def setName(self, name):
        self.class_name = name
        return self

    def getNode(self, page = 1000):
        idx = self.getPageIndex(page)
        if idx < len(self.node_list):
            return self.node_list[idx]
        # Assumption failure?
        return self.node_list[-1]

    def setNode(self, node, page = 1000):
        if type(node) is str:
            node = node_dict[node].copy()
        idx = self.getPageIndex(page)        
        if idx < len(self.node_list):
            self.node_list[idx] = node.copy()
        else:
            self.node_list[-1] = node.copy()
        return self

    def getColor(self, page=1000):
        return self.getNode(page).getColor()

    def setColor(self, c, page=1000):
        if type(c) is str:
            if c not in color_dict:
                print("Invalid color %s, ignoring it." % c)
                return self
            c = color_dict[c]
        self.getNode(page).setColor(c)
        return self

    def toString(self):
        return self.getName()

    def drawOnPageQ(self, page):
        return self.page_list[-1] >= page
