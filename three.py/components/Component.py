#Right now, the component class does not have any special functions associated
#but in the future I plan on adding more components, so having this and the potential
#for common methods should make things easier
class Component(object):
    IDCounter = 0 
    def __init__(self):
        self.ID = Component.IDCounter
        Component.IDCounter+=1
