import math
import numpy as np
from mathutils import MatrixFactory


# a curve consists of a function, a domain [min,max], and a resolution (divisions).
# getPoints() returns equally spaced points along the curve
# getFrames() returns { "tangents" : list, "normals" : list, "binormals" : list } at same set of points

class Curve(object):

    # divisions = number of line segments. len(points) = divisions+1.
    def __init__(self, curveFunction, tMin=0, tMax=1, divisions=4, arcLengthDivisions=256):
        self.f = curveFunction
        self.tMin = tMin
        self.tMax = tMax
        self.divisions = divisions
        
        # reparameterize curve by arclength
        self.arcLengthDivisions = arcLengthDivisions
        # list of length of curve from tMin to t
        # approximate using # of points from arcLengthDivisions
        # TODO: clean this up
        self.arcLengths = None
        self.totalArcLength = None
        self.calculateArcLengths()

        # for dashed lines:
        
        # normalize for hue shading
        
    def calculateArcLengths(self):
        # note: points stored as numpy arrays for simpler calculation syntax
        arcLengthPoints = []
        deltaT = (self.tMax - self.tMin) / (self.arcLengthDivisions-1) 
        
        for index in range(self.arcLengthDivisions):
            t = self.tMin + index * deltaT
            point = self.getPointAt(t)
            arcLengthPoints.append( np.array(point) )
            
        self.arcLengths = [0]
        for index in range(1, self.arcLengthDivisions):
            arcLength = np.linalg.norm( arcLengthPoints[index] - arcLengthPoints[index-1] )
            self.arcLengths.append( self.arcLengths[index-1] + arcLength )
        
        self.totalArcLength = self.arcLengths[self.arcLengthDivisions-1]
        
    # u - percentage of total curve distance traversed, in [0,1]
    # t - corresponding value of variable from original parameterization
    def convert_u_to_t(self, u):
        arcLength = u * self.totalArcLength
        # index = np.searchsorted(list, value) means that list[index-1] < value <= list[index]
        index = np.searchsorted(self.arcLengths, arcLength)
        # arcLengthA < arcLength < arcLengthB
        arcLengthA = self.arcLengths[index-1]
        arcLengthB = self.arcLengths[index]
        segmentLength = arcLengthB - arcLengthA
        # determine how far along the segment this arclength would be
        percent = (arcLength - arcLengthA) / segmentLength
        # 
        deltaT = (self.tMax - self.tMin) / (self.arcLengthDivisions-1)
        tA = self.tMin + (index-1) * deltaT
        t = tA + percent * deltaT
        return t

    # calculates a point according to original parameterization
    def getPointAt(self, t):
        return self.f(t)
                
    # calculates a point according to arclength parameterization
    # u - percentage of total curve distance traversed, in [0,1]
    def getPoint(self, u):
        t = self.convert_u_to_t(u)
        return self.getPointAt(t)
        
    # calculates a list of equally spaced points along the curve
    def getPoints(self):
        points = []
        deltaU = 1 / (self.divisions - 1)
        for index in range(self.divisions):
            u = index * deltaU
            point = self.getPoint(u)
            points.append( point )        
        return points

    # calculates a tangent vector according to original parameterization
    def getTangentAt(self, t):
        h = 0.00001
        tangent = np.divide( np.subtract(self.getPointAt(t+h), self.getPointAt(t)), h )
        tangent = np.divide( tangent, np.linalg.norm(tangent) )
        return tangent
    
    # calculates a tangent vector according to arclength parameterization
    # u - percentage of total curve distance traversed, in [0,1]
    def getTangent(self, u):
        t = self.convert_u_to_t(u)
        return self.getTangentAt(t)
    
    
    # returns { "tangents" : list, "normals" : list, "binormals" : list }
    #  length of each list = divisions
    def getFrames(self):
        tangents  = []
        normals   = []
        binormals = []
        
        # calculate tangents ------------------------
        deltaU = 1 / (self.divisions - 1)
        for index in range( self.divisions ):
            u = index * deltaU
            tangent = self.getTangent(u)
            tangents.append( tangent )

        # calculate normals ------------------------
        # reference: https://cs.indiana.edu/ftp/techreports/TR425.pdf
        
        # calculate initial normal vector
        arbitraryVector = [1,1,1] # if tangents[0] != c*[1,1,1] else [1,1,-1]
        normal = np.cross(tangents[0], arbitraryVector)
        normals.append(normal)
        
        # calculate the remaining normal vectors
        for n in range(1, self.divisions):
        
            # default normal vector equals the previous normal vector
            # (will be used if the tangent vector has not changed direction)
            normal =  normals[n-1]
            
            # if two vectors are parallel, 
            #  then their cross product is the zero vector (which has magnitude zero)
            crossProduct = np.cross(tangents[n-1], tangents[n])
            # therefore, if this magnitude is nonzero, 
            #  the tangent vectors have changed direction
            #  and we need to apply the same change to the normal vector.
            magnitude = np.linalg.norm(crossProduct)
            if (magnitude > 0.0001):
                # normalize the cross product vector
                crossProduct = np.divide(crossProduct, magnitude)
                
                # calculate the angle between the previous and current tangent vector
                theta = math.acos( np.dot(tangents[n-1], tangents[n]) )

                # calculate the transformation the rotates previous tangent vector
                #  into the current tangent vector
                rotationMatrix = MatrixFactory.makeRotationAxisAngle(crossProduct,theta)
                
                # apply this transformation to the normal vector
                normal = self.applyMatrix4(normal, rotationMatrix)

            # assign next normal vector
            normals.append(normal)
        
        # calculate binormals ------------------------
        for index in range( self.divisions ):
            binormal = np.cross( tangents[index], normals[index] )
            binormals.append( binormal )

        # calculations complete ------------------------
        return { "tangents" : tangents, "normals" : normals, "binormals" : binormals }

    
    @staticmethod
    def applyMatrix4(vec, mat):
        vec = list( vec )       # convert back to list
        vec.append(1)           # convert vec3 to homogeneous vec4
        vec = list( mat @ vec ) # apply transformation
        vec.pop(3)              # convert vec4 back to vec3
        return vec
        
    # TODO: getLengths (of intervals), getLengthAt (requires all lengths & interpolation on correct segment...
    
    """
    getLengths(divisions) (cumulative segment lengths at each point)  [0, 0.1, 0.35, 0.4, 0.8, 1.2, 1.9]
    getTotalLength(tRes) = arcLength approximation, last value of getLengths' array
    use these to get parameterization by arc length? nice/accurate tex coords?
    
    
    """
