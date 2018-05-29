#!./jython
import sys
import os
#sys.path.append("..\\resolution\\resolution.jar")
sys.path.append(os.path.join('resolution', 'resolution.jar'))

from sseq_class_defs import *
import code



def monomialString(vars, exponents):
    out = [None] * len(vars)
    for i in range(0,len(vars)):
        if(exponents[i]==0):
            out[i] = ""
        elif(exponents[i]==1):
            out[i] = vars[i]
        else:
            out[i] = vars[i] + "^" + str(exponents[i])
    return " ".join(filter(lambda s: s != "",out))

def initialize(settings):
    global sseq 
    global startDisplay 
    sseq = Sseq()
    startDisplay = SpectralSequenceDisplay.constructFrontend(sseq,settings).start
    return sseq
    
def getSettingsObject():
    settings = DisplaySettings()
    settings.windowName = "Interactive Spectral Sequences"
    return settings

if(len(sys.argv) > 1):
    exec(open(sys.argv[1],"r").read())
else:
    settings = getSettingsObject()
    settings.prime = 2
    settings.xscale = 1
    settings.yscale = 2
    settings.xmin = -50
    settings.xmax = 50
    settings.ymin = 0
    settings.ymax = 30
    settings.xgridstep = 5
    settings.ygridstep = 5
    settings.T_max = 100
    settings.x_full_range = True
    settings.page_list = [0,5,9,17,33,65]
    sseq = initialize(settings)


startDisplay()

def run_repl():
    code.interact(local=globals()) 
    sys.exit()

run_repl()
