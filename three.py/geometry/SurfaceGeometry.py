from mathutils import Surface
from geometry import Geometry

class SurfaceGeometry(Geometry):
    def __init__(self, uStart, uEnd, uResolution, vStart, vEnd, vResolution, surfaceFunction):
        super().__init__()

        surface = Surface(surfaceFunction)

        positions = surface.getPoints(uStart, uEnd, uResolution, vStart, vEnd, vResolution)
        uvs       = surface.getUVs(uResolution, vResolution)
        normals   = surface.getNormals(uStart, uEnd, uResolution, vStart, vEnd, vResolution)
                
        vertexPositionData = []
        vertexUVData       = []
        vertexNormalData   = []
        
        # group vertex data into triangles
        # note: .copy() is necessary to avoid storing references
        for xIndex in range(uResolution):
            for yIndex in range(vResolution):

                # position coordinates
                pA = positions[xIndex+0][yIndex+0]
                pB = positions[xIndex+1][yIndex+0]
                pD = positions[xIndex+0][yIndex+1]
                pC = positions[xIndex+1][yIndex+1]

                vertexPositionData += [pA.copy(),pB.copy(),pC.copy(), pA.copy(),pC.copy(),pD.copy()]

                # uv coordinates
                uvA = uvs[xIndex+0][yIndex+0]
                uvB = uvs[xIndex+1][yIndex+0]
                uvD = uvs[xIndex+0][yIndex+1]
                uvC = uvs[xIndex+1][yIndex+1]
                
                vertexUVData += [uvA,uvB,uvC, uvA,uvC,uvD]
                
                # normal coordinates
                nA = normals[xIndex+0][yIndex+0]
                nB = normals[xIndex+1][yIndex+0]
                nD = normals[xIndex+0][yIndex+1]
                nC = normals[xIndex+1][yIndex+1]
                
                vertexNormalData += [nA.copy(),nB.copy(),nC.copy(), nA.copy(),nC.copy(),nD.copy()]

        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        
        self.vertexCount = len(vertexPositionData)
       