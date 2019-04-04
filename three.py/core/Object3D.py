import numpy as np
from OpenGL.GL import *

from mathutils import Matrix
from core import *

class Object3D(object):

    def __init__(self):
        self.transform = Matrix()
        self.parent = None
        self.children = []
        self.name = ""
    
    def add(self, child):
        self.children.append(child)
        child.parent = self
        
    def remove(self, child):
        self.children.remove(child)
        child.parent = None
        
    def getWorldMatrix(self):
        if self.parent == None:
            return self.transform.matrix
        else:
            return self.parent.getWorldMatrix() @ self.transform.matrix
    
    # return a list of descendants in depth-first order
    def getDepthFirstList(self):
        # elements added to list as a stack for depth-first traversal
        unvisitedList = [self]
        visitedList = []
        while len( unvisitedList ) > 0:
            item = unvisitedList.pop(0)
            visitedList.append(item)
            unvisitedList = item.children + unvisitedList
        return visitedList
        
    # return a list of descendants x with filterFunction(x) = True
    def getObjectsByFilter(self, filterFunction=None):
        return list( filter( filterFunction, self.getDepthFirstList() ) )
        
    def getObjectByName(self, name):
        return self.getObjectsByFilter( lambda x : x.name == name )[0]
        
