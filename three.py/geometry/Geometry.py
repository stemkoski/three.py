from OpenGL.GL import *
import numpy as np

class Geometry(object):

    def __init__(self, name="Geometry"):
        self.attributeData = {}
        self.vertexCount = None # must be set by extending class
        self.name = name
        
        # store vertex data bindings automatically;
        #   index by shaderProgramID
        self.vaoData = {} 

        
    # TODO: class Attribute, to parallel class Uniform?
    
    # TODO: rename as "initializeAttributeData"?
    # name: name of attribute variable in shader
    # value: array of values
    # type: float, vec2, vec3, vec4
    def setAttribute(self, type, name, value):
        data = { "type": type, "name": name, "value": value, "bufferID": None }
        self.attributeData[name] = data
        self.processAttribute(name)

    # send attribute data to a GPU buffer
    def processAttribute(self, name):
        data = self.attributeData[name]
        # if necessary, obtain an available buffer reference
        if data["bufferID"] is None:
            # return an available (unused) reference value
            data["bufferID"] = glGenBuffers(1)

        # make current bufferID active
        glBindBuffer(GL_ARRAY_BUFFER, data["bufferID"])
        # convert to a numpy array
        array = np.array( data["value"] ).astype( np.float32 )
        # create empty buffer object if necessary,
        # and send data to the active buffer
        glBufferData(GL_ARRAY_BUFFER, array.ravel(), GL_STATIC_DRAW)

    # useful for changing vertex data after initial process
    def updateAttribute(self, name, value):
        self.attributeData[name]["value"] = value
        self.processAttribute(name)
        
    # setup vertex bindings and store in VAO
    # will be called automatically the first time getVAO is called
    def setupVAO(self, shaderProgramID):
    
        vao = glGenVertexArrays(1)
        
        # DEBUG
        # print("Initializing VAO #", vao, "for geometry:", self.name)
        
        # all the following vertex bindings will be stored in this VAO
        glBindVertexArray(vao)
        
        # set up attribute pointers
        for name, data in self.attributeData.items():
        
            # make current bufferID active
            glBindBuffer(GL_ARRAY_BUFFER, data["bufferID"])

            attributeVarID = glGetAttribLocation(shaderProgramID, data["name"])
            # check if this variable exists in shader program; if so, point it to currently bound bufferID.
            if (attributeVarID != -1):
                glEnableVertexAttribArray(attributeVarID)
                if data["type"] == "float":
                    glVertexAttribPointer(attributeVarID, 1, GL_FLOAT, False, 0, None)
                elif data["type"] == "vec2":
                    glVertexAttribPointer(attributeVarID, 2, GL_FLOAT, False, 0, None)
                elif data["type"] == "vec3":
                    glVertexAttribPointer(attributeVarID, 3, GL_FLOAT, False, 0, None)
                elif data["type"] == "vec4":
                    glVertexAttribPointer(attributeVarID, 4, GL_FLOAT, False, 0, None)
                else:
                    raise Exception("Attribute " + data['name'] + " has unknown type " + data['type'])
    
        self.vaoData[shaderProgramID] = vao
        
        # all done; unbind this VAO
        glBindVertexArray(0)
        
    # get the VAO that stores vertex attribute bindings for this object
    def getVAO(self, shaderProgramID):
    
        if not shaderProgramID in self.vaoData:
            self.setupVAO(shaderProgramID)
            
        return self.vaoData[shaderProgramID]
    
    
    
    
    
    
    
    