import os
from geometry import Geometry
import numpy as np

# Note, may need to hand in absolute directory yourself here
#  or store the directory somewhere at the root
class OBJExtruder(Geometry):
    def __init__(self,objFileName="", smoothNormals=False):
        super().__init__()
        
        # open the file, and get the contents
        os.chdir(os.getcwd() + "..") # go up one directory
        # now in theory, we are in the root of the project,
        # assuming that the geometry package is at the root

        # open the file, get contents, close the file
        objFile = open(objFileName)
        objContentString = objFile.read()
        objFile.close()
        
        # initialize the three lists
        positionList = []
        UVList       = []
        normalList   = []

        # Turn the string into an array
        self.objContents = objContentString.splitlines()

        # initialize the final lists that will go to the buffers
        vertexPositionData = []
        vertexUVData       = []
        vertexNormalData   = []

        # used when smoothNormals=True
        
        # key=position, value=sum of normals at that position
        accumulatedNormals = {}
        # keep track of the order (by key) in which values were added to accumulatedNormals
        normalAddOrder = []

        #keep track of the order of the outside vertices(list of vertex indeces)
        self.outsideVertexIndexList = []
        self.outsideVertexIndexListLine = 0

        #key=index, value=vertex
        self.parallelFaceDict = {}

        
        for line in self.objContents:
        
            # remove whitespace
            if len(line.strip()) == 0:
                continue

            # split line into string tokens
            values = line.split()

            #do different things with the values
            if(values[0] == 'v'):
                positionList.append( [ float(values[1]), float(values[2]), float(values[3]) ] )
            elif(values[0] == 'vt'):
                UVList.append( [ float(values[1]), float(values[2]) ] )
            elif(values[0] == 'vn'):
                normalList.append( [ float(values[1]), float(values[2]), float(values[3]) ] )
            elif(values[0] == 'o'):
                #gets the number of the outside vertex index list
                self.outsideVertexIndexListLine = self.objContents.index(line)

                #adds the indeces to the list
                for x in range(1,len(values)):
                    self.outsideVertexIndexList.append(int(values[x]))
            elif(values[0] == 'f'):
                #keeps track of parallel vertices on this line
                parallelPositionList = []

                #keeps track of the original vertices on this line
                originalPositionList = []
                
                # represents the three points in a triangle
                for i in range(1,4):
                
                    # get data for vertex i (i=1,2,3)
                    trianglePointData = values[i]

                    # separate data (format: vertexIndex/uvIndex/normalIndex)
                    #  note: OBJ index numbering starts at 1
                    positionIndex, uvIndex, normalIndex = trianglePointData.split("/")

                    # add data to corresponding lists
                    position = positionList[int(positionIndex)-1]

                    #adds the vertex to the list
                    originalPositionList.append(position)       
                    
                    #generates a parallel vertex, then adds to list 
                    parallelFace = [position[0], position[1], position[2]-1]
                    parallelPositionList.append(parallelFace)

                    #adds parallel face to dictionary at the right index
                    self.parallelFaceDict[int(positionIndex)] = parallelFace
                    
                    
                    vertexPositionData += [ position[0], position[1], position[2] ] # TODO: extend?
                
                    UV = UVList[int(uvIndex)-1]
                    vertexUVData += [ UV[0], UV[1] ]
                    normal = normalList[int(normalIndex)-1]
                    
                    if smoothNormals:
                        # convert position to a string, because lists can not be used as dictionary keys
                        positionKey = "x" + str(position[0]) + "y" + str(position[1]) + "z" + str(position[2])
                        normalAddOrder.append( positionKey )
                        if positionKey not in accumulatedNormals:
                            accumulatedNormals[positionKey] = normal
                        else:
                            accumulatedNormals[positionKey][0] += normal[0]
                            accumulatedNormals[positionKey][1] += normal[1]
                            accumulatedNormals[positionKey][2] += normal[2]
                    else:
                        vertexNormalData += [ normal[0], normal[1], normal[2] ]

                #adds the parallel face to the vertex data
                for point in parallelPositionList:
                    vertexPositionData += [point[0], point[1], point[2]]

        
        #add the side faces
        print("outside vertex index list:", self.outsideVertexIndexList)
        print("parallel face list:", self.parallelFaceDict)
        #for each index in the outside vertex list
        for outsideVertexIndex in range(0 , len(self.outsideVertexIndexList)):
            print("index", outsideVertexIndex)

            #mod the index by the length of the list so it wraps back to 1
            outsideVertexIndexNext = ((outsideVertexIndex+1) % len(self.outsideVertexIndexList))
            print("next index",outsideVertexIndexNext)
            
            #get the indeces from the outside vertex list
            index=self.outsideVertexIndexList[outsideVertexIndex]
            index2=self.outsideVertexIndexList[outsideVertexIndexNext]
            
            
            #get points from original face
            position =  positionList[index-1]
            position2 = positionList[index2-1]

            #get points from parallel face
            parallelPos = self.parallelFaceDict[index]
            parallelPos2 = self.parallelFaceDict[index2]
            
            #make triangles from the points and add to the data
            vertexPositionData += [position[0],position[1],position[2],
                                   parallelPos[0],parallelPos[1],parallelPos[2],
                                   parallelPos2[0],parallelPos2[1],parallelPos2[2]]
            vertexPositionData += [position2[0],position2[1],position2[2],
                                   position[0],position[1],position[2],
                                   parallelPos2[0],parallelPos2[1],parallelPos2[2]]

                
                    
                        
        if smoothNormals:
            # normalize the accumulated normal vectors
            for positionKey, normal in accumulatedNormals.items():
                length = np.linalg.norm( normal )
                accumulatedNormals[positionKey][0] /= length
                accumulatedNormals[positionKey][1] /= length
                accumulatedNormals[positionKey][2] /= length
            # append new normal vectors into vertexNormalData list
            for positionKey in normalAddOrder:
                normal = accumulatedNormals[positionKey]
                vertexNormalData += [ normal[0], normal[1], normal[2] ]
            
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        self.vertexCount = len(vertexPositionData)
