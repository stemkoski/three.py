import numpy as np
from mathutils import Matrix
import math
from components import *

#Sphere component, can be used for a lot of things, including
#detecting collisions
class Sphere(Shape):
    def __init__(self, radius = 1, center = (0,0,0)):
        super().__init__()
        self.radius = radius
        self.center = np.asarray(center)

    def setPosition(self, newPos):
        self.center = np.asarray(newPos)

    def align(self,matrix):
        self.center = np.asarray(matrix.getPosition())

    def intersectSphere(self,other):
        distance = abs(np.linalg.norm(self.center - other.center))
        addedRadius = self.radius + other.radius
        return (addedRadius >= distance)

    def intersectsPlane(self, plane):
        return (abs(plane.distanceToPoint(self.center)) <= self.radius)

    #returns the minimum translation vector needed to prevent an overlap
    #will move other
    #TODO: check other shapes?
    def preventOverlap(self,other):
        if not self.intersectSphere(other):
            return None

        distanceVec = other.center - self.center
        distanceLen = math.sqrt(distanceVec[0]**2+distanceVec[1]**2+distanceVec[2]**2)

        minTransLen = distanceLen - self.radius - other.radius

        distanceNorm = (distanceVec[0]/distanceLen,distanceVec[1]/distanceLen,distanceVec[2]/distanceLen)

        minimumTranslationVector = (-distanceNorm[0]*minTransLen,-distanceNorm[1]*minTransLen,-distanceNorm[2]*minTransLen)
        
        return minimumTranslationVector
