import math
import numpy as np

class MatrixFactory(object):

    @staticmethod
    def makeIdentity():
        return np.array( [[1,0,0,0],
                          [0,1,0,0],
                          [0,0,1,0],
                          [0,0,0,1]] )

    @staticmethod
    def makeTranslation(x, y, z):
        return np.array([[1,0,0,x],
                         [0,1,0,y],
                         [0,0,1,z],
                         [0,0,0,1]])
    
    # rotation around x axis
    @staticmethod
    def makeRotationX(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return np.array([[1,0,0,0],
                         [0,c,-s,0],
                         [0,s,c,0],
                         [0,0,0,1]])
                     
    # rotation around y axis
    @staticmethod
    def makeRotationY(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return np.array([[c,0,s,0],
                          [0,1,0,0],
                          [-s,0,c,0],
                          [0,0,0,1]])
             
    # rotation around z axis
    @staticmethod
    def makeRotationZ(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return np.array([[c,-s,0,0],
                          [s,c,0,0],
                          [0,0,1,0],
                          [0,0,0,1]])

    # translation along a specified (normalized) axis
    @staticmethod
    def makeTranslationAxisDistance(axis, distance):
        displacement = np.array(axis) * distance
        return np.array( [[1, 0, 0, displacement[0]],
                           [0, 1, 0, displacement[1]],
                           [0, 0, 1, displacement[2]],
                           [0, 0, 0, 1]] )
                         
    
    # rotation around a specified (normalized) axis
    @staticmethod
    def makeRotationAxisAngle(axis, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        t = 1 - c
        x = axis[0]
        y = axis[1]
        z = axis[2]
        tx = t*x
        ty = t*y
        return np.array([[tx*x+c,   tx*y-s*z, tx*z+s*y, 0],
                          [tx*y+s*z, ty*y+c,   ty*z-s*x, 0],
                          [tx*z-s*y, ty*z+s*x, t*z*z+c,  0],
                          [0, 0, 0, 1]])
    
    # make scale
    @staticmethod
    def makeScaleUniform(s):
        return np.array([[s,0,0,0],
                         [0,s,0,0],
                         [0,0,s,0],
                         [0,0,0,1]])
    
    @staticmethod
    def makePerspective(fov=60, aspect=1, near=0.1, far=1000):
        D2R = 3.1415926 / 180.0
        yScale = 1.0 / math.tan(D2R * fov / 2)
        xScale = yScale / aspect
        c = (far + near) / (near - far)
        d = 2*far*near / (near - far)
        return np.array([[xScale,0,0,0], 
                         [0,yScale,0,0], 
                         [0, 0,  c, d],
                         [0, 0, -1, 0]])

    @staticmethod
    def makeOrthographic(left=-1, right=1, top=1, bottom=-1, far=1, near=-1):
        return np.array([[2/(right-left), 0, 0, -(right+left)/(right-left)], 
                         [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)], 
                         [0, 0,  -2/(far-near), -(far+near)/(far-near)],
                         [0, 0, 0, 1]])
                          
    @staticmethod
    def makeLookAt(position, target, up):
        
        forward = np.subtract(target, position)
        forward = np.divide( forward, np.linalg.norm(forward) )

        right = np.cross( forward, up )
        
        # if forward and up vectors are parallel, right vector is zero; 
        #   fix by perturbing up vector a bit
        if np.linalg.norm(right) < 0.001:
            epsilon = np.array( [0.001, 0, 0] )
            right = np.cross( forward, up + epsilon )
            
        right = np.divide( right, np.linalg.norm(right) )
        
        up = np.cross( right, forward )
        up = np.divide( up, np.linalg.norm(up) )
        
        return np.array([[right[0], up[0], -forward[0], position[0]], 
                         [right[1], up[1], -forward[1], position[1]], 
                         [right[2], up[2], -forward[2], position[2]],
                         [0, 0, 0, 1]])                  
        
