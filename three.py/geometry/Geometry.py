class Geometry(object):

    def __init__(self):
        self.attributeData = {}
        self.vertexCount = None # must be set by extending class

    # name: name of attribute variable in shader
    # value: array of values
    # type: float, vec2, vec3, vec4
    def setAttribute(self, type, name, value):
        data = { "type": type, "name": name, "value": value, 
                 "needsUpdate": True, "bufferID": None }
        self.attributeData[name] = data
        