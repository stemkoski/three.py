import numpy as np

# NOTE: Three.js automatically scales parameter domain to [0,1] (based on 200 subdivisions). 
# is this useful? could more easily get equally spaced points along the curve. check 3js' code.

class Surface(object):
        
    def __init__(self, surfaceFunction):
        self.f = surfaceFunction
        
    def getPoints(self, uStart, uEnd, uResolution, vStart, vEnd, vResolution):
        deltaU = (uEnd - uStart) / uResolution 
        deltaV = (vEnd - vStart) / vResolution 
        points = []
        
        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                u = uStart + uIndex * deltaU
                v = vStart + vIndex * deltaV
                vArray.append( self.f(u,v) )
            points.append(vArray)

        return points
        
    def getUVs(self, uResolution, vResolution):
        UVs = []
        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                # u = uStart + uIndex * deltaU
                # v = vStart + vIndex * deltaV
                vArray.append( [uIndex/uResolution, vIndex/vResolution] )
            UVs.append(vArray)
            
        return UVs

    def getNormalAt(self, u, v):
        h = 0.0001
        uDeriv = ( np.array(self.f(u+h, v)) - np.array(self.f(u, v)) ) / h
        vDeriv = ( np.array(self.f(u, v+h)) - np.array(self.f(u, v)) ) / h
        # calculate the normal at this point
        normalVector = np.cross(uDeriv,vDeriv)
        # normalize normal vectors
        normalVector = normalVector / np.linalg.norm(normalVector)
        return list(normalVector)
        
    def getNormals(self, uStart, uEnd, uResolution, vStart, vEnd, vResolution):
        deltaU = (uEnd - uStart) / uResolution 
        deltaV = (vEnd - vStart) / vResolution 
        normals = []

        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                u = uStart + uIndex * deltaU
                v = vStart + vIndex * deltaV
                vArray.append( self.getNormalAt(u,v) )
            normals.append(vArray)
            
        return normals


    # TODO: getPoint, getTangent
    """
    getLengths(tResolution) (cumulative segment lengths at each point)  [0, 0.1, 0.35, 0.4, 0.8, 1.2, 1.9]
    getTotalLength(tRes) = arcLength approximation, last value of getLengths' array
    use these to get parameterization by arc length? nice/accurate tex coords?
    
    
    """
