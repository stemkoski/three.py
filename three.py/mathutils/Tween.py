# Tween objects linearly interpolate (lerp)
#   between a set of values that occur at a given set of times

class Tween(object):

    # assume timeList is sorted in increasing order
    def __init__(self, timeList=[0], valueType="float", valueList=[1], loop=False):
        self.timeList  = timeList
        self.valueType = valueType
        self.valueList = valueList
        self.listSize  = len(timeList)
        self.loop = loop
        
    @staticmethod
    def lerpFloat(minFloat, maxFloat, percent):
        return minFloat + (maxFloat - minFloat) * percent
        
    @staticmethod
    def lerpVec2(minVec, maxVec, percent):
        return [ Tween.lerpFloat( minVec[0], maxVec[0], percent ),
                 Tween.lerpFloat( minVec[1], maxVec[1], percent ) ]
    
    @staticmethod
    def lerpVec3(minVec, maxVec, percent):
        return [ Tween.lerpFloat( minVec[0], maxVec[0], percent ),
                 Tween.lerpFloat( minVec[1], maxVec[1], percent ),
                 Tween.lerpFloat( minVec[2], maxVec[2], percent ) ]
        
    @staticmethod
    def percentFloat(minFloat, maxFloat, value):
        return (value - minFloat) / (maxFloat - minFloat)
        
    def evaluate(self, time):
    
        if self.loop:
            time = time % self.timeList[self.listSize-1]
            
        # if time is outside the range specified by timeList,
        #    return the first/last element of valueList, as appropriate
        if time < self.timeList[0]:
            return self.valueList[0]
            
        if time > self.timeList[self.listSize-1]:
            return self.valueList[self.listSize-1]

        # determine index, so that timeList[index-1] < time < timeList[index]
        index = 0
        while index < self.listSize and time > self.timeList[index]:
            index += 1
           
        # find relative location of time within this interval
        percent = Tween.percentFloat(self.timeList[index-1], self.timeList[index], time)
        
        # return interpolated value, according to value type
        if self.valueType == "float":
            return Tween.lerpFloat(self.valueList[index-1], self.valueList[index], percent)
        elif self.valueType == "vec2":
            return Tween.lerpVec2(self.valueList[index-1], self.valueList[index], percent)
        elif self.valueType == "vec3":
            return Tween.lerpVec3(self.valueList[index-1], self.valueList[index], percent)
        else:
            raise Exception("Tween.evaluate() - unknown value type: " + self.valueType)
        
        
        