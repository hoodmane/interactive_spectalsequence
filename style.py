from java.awt import Color, Shape

from res.spectralsequencediagram import *
from res.spectralsequencediagram.nodes import *

infinity = 10000

color_dict = {'black' : Color.BLACK, 'blue' : Color.BLUE, 'green' : Color.GREEN, 'red' : Color.RED }
node_dict = {
    'Z' : RectangleNode(8),
    '2Z' : RectangleNode(8,8,RectangleNode.NO_FILL),    
    'pZ' : RectangleNode(8,8,RectangleNode.NO_FILL),    
    'Zq' : RectangleNode(8),
    'qZq' : RectangleNode(8,8,RectangleNode.NO_FILL),    
    'Z/q' : CircleNode(),
    'Fp' : CircleNode(),
    
}

    
    
    
    
