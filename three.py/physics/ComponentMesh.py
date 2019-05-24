import numpy as np

from core import Mesh
from components import *

class ComponentMesh(Mesh):
    def __init__(self,geometry,material):
        super().__init__(geometry,material)
        self.componentDict = {}

    #TODO: make some list of keys for checking instead of explicitly
    def addComponent(self,key,component):
        self.componentDict[key] = component

    
    def overlaps(self,other):
        if "Sphere" not in self.componentDict.keys():
            return False
        
        overlaps = (self.componentDict["Sphere"].intersectsSphere(other.componentDict["Sphere"]))
        return overlaps

    #TODO: prevent overlap with more types of components
    def preventOverlap(self,other):
        if not self.overlaps(other):
            return None

        minTransVec = self.componentDict["Sphere"].preventOverlap(
            other.componentDict["Sphere"])

        other.transform.translate(minTransVec[0],minTransVec[1],minTransVec[2])
        other.componentDict["Sphere"].setPosition(
            other.componentDict["Sphere"].center+minTransVec)

    def render(self, shaderProgramID=None):
        if "Sphere" in self.componentDict.keys():
            self.componentDict["Sphere"].setPosition(self.transform.getPosition())

        super().render(shaderProgramID)
        
