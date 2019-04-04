from geometry import Geometry, QuadGeometry
from mathutils import MatrixFactory
import numpy as np
from math import pi

class BoxGeometry(Geometry):

    def __init__(self, width=2, height=2, depth=2, widthResolution=1, heightResolution=1, depthResolution=1):
        super().__init__()

        # create from 6 quads.
        
        vertexPositionData = []
        vertexUVData = []
        vertexNormalData = []
        
        frontQuad = QuadGeometry(width, height, widthResolution, heightResolution)
        frontMatrix = MatrixFactory.makeTranslation(0,0,depth/2)
        vertexPositionData += self.applyMat4ToVec3List( frontMatrix, frontQuad.attributeData["vertexPosition"]["value"] )
        vertexUVData       += frontQuad.attributeData["vertexUV"]["value"]
        vertexNormalData   += self.applyMat4ToVec3List( frontMatrix, frontQuad.attributeData["vertexNormal"]["value"] )
        
        backQuad = QuadGeometry(width, height, widthResolution, heightResolution)
        backMatrix = MatrixFactory.makeTranslation(0,0,-depth/2) @ MatrixFactory.makeRotationY(pi) 
        vertexPositionData += self.applyMat4ToVec3List( backMatrix, backQuad.attributeData["vertexPosition"]["value"] )
        vertexUVData       += backQuad.attributeData["vertexUV"]["value"]
        vertexNormalData   += self.applyMat4ToVec3List( backMatrix, backQuad.attributeData["vertexNormal"]["value"] )
        
        leftQuad = QuadGeometry(depth, height, depthResolution, heightResolution)
        leftMatrix = MatrixFactory.makeTranslation(-width/2,0,0) @ MatrixFactory.makeRotationY(-pi/2)
        vertexPositionData += self.applyMat4ToVec3List( leftMatrix, leftQuad.attributeData["vertexPosition"]["value"] )
        vertexUVData       += leftQuad.attributeData["vertexUV"]["value"]
        vertexNormalData   += self.applyMat4ToVec3List( leftMatrix, leftQuad.attributeData["vertexNormal"]["value"] )
        
        rightQuad = QuadGeometry(depth, height, depthResolution, heightResolution)
        rightMatrix = MatrixFactory.makeTranslation(width/2,0,0) @ MatrixFactory.makeRotationY(pi/2)
        vertexPositionData += self.applyMat4ToVec3List( rightMatrix, rightQuad.attributeData["vertexPosition"]["value"] )
        vertexUVData       += rightQuad.attributeData["vertexUV"]["value"]
        vertexNormalData   += self.applyMat4ToVec3List( rightMatrix, rightQuad.attributeData["vertexNormal"]["value"] )
        
        topQuad = QuadGeometry(width, depth, widthResolution, depthResolution)
        topMatrix = MatrixFactory.makeTranslation(0,height/2,0) @ MatrixFactory.makeRotationX(-pi/2)
        vertexPositionData += self.applyMat4ToVec3List( topMatrix, topQuad.attributeData["vertexPosition"]["value"] )
        vertexUVData       += topQuad.attributeData["vertexUV"]["value"]
        vertexNormalData   += self.applyMat4ToVec3List( topMatrix, topQuad.attributeData["vertexNormal"]["value"] )
        
        bottomQuad = QuadGeometry(width, depth, widthResolution, depthResolution)
        bottomMatrix = MatrixFactory.makeTranslation(0,-height/2,0) @ MatrixFactory.makeRotationX(pi/2)
        vertexPositionData += self.applyMat4ToVec3List( bottomMatrix, bottomQuad.attributeData["vertexPosition"]["value"] )
        vertexUVData       += bottomQuad.attributeData["vertexUV"]["value"]
        vertexNormalData   += self.applyMat4ToVec3List( bottomMatrix, bottomQuad.attributeData["vertexNormal"]["value"] )
        
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV",       vertexUVData)
        self.setAttribute("vec3", "vertexNormal",   vertexNormalData)
        
        self.vertexCount = len(vertexPositionData)

    def applyMat4ToVec3List(self, matrix, originalVectorList):
        newVectorList = []
        count = len(originalVectorList)
        for index in range(count):
            v = originalVectorList[index]
            v.append(1) # convert to homogeneous coordinates
            v = list(matrix @ v)
            v.pop(3) # convert back to vec3
            newVectorList.append(v)
        return newVectorList

        
