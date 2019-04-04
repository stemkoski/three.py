import numpy as np
from mathutils.MatrixFactory import *

# this class uses a numpy matrix to store data
# and contains methods to transform the matrix
class Matrix(object):

    LOCAL = 1
    GLOBAL = 2
        
    def __init__(self):
        self.matrix = MatrixFactory.makeIdentity().astype(float) # set type, otherwise set values cast to ints

    def translate(self, x=0, y=0, z=0, type=GLOBAL):
        if type == Matrix.LOCAL:
            self.matrix = self.matrix @ MatrixFactory.makeTranslation(x,y,z)
        if type == Matrix.GLOBAL:
            self.matrix = MatrixFactory.makeTranslation(x,y,z) @ self.matrix

    def rotateZ(self, angle=0, type=GLOBAL):
        if type == Matrix.LOCAL:
            self.matrix = self.matrix @ MatrixFactory.makeRotationZ(angle)
        if type == Matrix.GLOBAL:
            self.matrix = MatrixFactory.makeRotationZ(angle) @ self.matrix

    def rotateX(self, angle=0, type=GLOBAL):
        if type == Matrix.LOCAL:
            self.matrix = self.matrix @ MatrixFactory.makeRotationX(angle)
        if type == Matrix.GLOBAL:
            self.matrix = MatrixFactory.makeRotationX(angle) @ self.matrix

    def rotateY(self, angle=0, type=GLOBAL):
        if type == Matrix.LOCAL:
            self.matrix = self.matrix @ MatrixFactory.makeRotationY(angle)
        if type == Matrix.GLOBAL:
            self.matrix = MatrixFactory.makeRotationY(angle) @ self.matrix
    
    def translateAxisDistance(self, axis=[1,0,0], distance=0, type=GLOBAL):
        if type == Matrix.LOCAL:
            self.matrix = self.matrix @ MatrixFactory.makeTranslationAxisDistance(axis, distance)
        if type == Matrix.GLOBAL:
            self.matrix = MatrixFactory.makeTranslationAxisDistance(axis, distance) @ self.matrix
            
    def rotateAxisAngle(self, axis=[1,0,0], angle=0, type=GLOBAL):
        if type == Matrix.LOCAL:
            self.matrix = self.matrix @ MatrixFactory.makeRotationAxisAngle(axis, angle)
        if type == Matrix.GLOBAL:
            self.matrix = MatrixFactory.makeRotationAxisAngle(axis, angle) @ self.matrix
        
    def scaleUniform(self, s=1, type=GLOBAL):
        self.matrix = self.matrix @ MatrixFactory.makeScaleUniform(s)

    # positions are global with respect to parent object
    def getPosition(self):
        return [ self.matrix.item((0,3)), 
                 self.matrix.item((1,3)),
                 self.matrix.item((2,3)) ]
                 
    def setPosition(self, x=0, y=0, z=0, type=LOCAL):
        self.matrix.itemset((0,3), x)
        self.matrix.itemset((1,3), y)
        self.matrix.itemset((2,3), z)
        
    # returns 3x3 submatrix with rotation data (assumes no scale)
    def getRotationMatrix(self):
        return np.array( [ self.matrix[0][0:3], 
                              self.matrix[1][0:3], 
                              self.matrix[2][0:3] ] )
                              
    # rotate matrix to look at target=[x,y,z]
    def lookAt(self, x, y, z):
        self.matrix = MatrixFactory.makeLookAt( self.getPosition(), [x,y,z], [0,1,0] )
        
        
        
                 