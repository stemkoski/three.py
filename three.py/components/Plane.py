import numpy as np
from mathutils import Matrix
import math
from components import *

#Plane component, can be used for several things, including collisions
#represented by the planes normal and its offset from the center
class Plane(Shape):
    def __init__(self,normal = (0,1,0), offset = 0):
        super().__init__()
        self.normal = np.asarray(normal)
        self.offset = offset

    def setOffset(self, newOffset):
        self.offset = newOffset

    def setNormal(self, newNormal):
        self.normal = np.asarray(newNormal)

    #NOTE: the point taken in must be a numpy array
    def distanceToPoint(self, point):
        return np.dot(self.normal, point) + self.offset

    def intersectsSphere(self, sphere):
        return sphere.intersectsPlane(self)
