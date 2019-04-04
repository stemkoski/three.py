from core import *
from geometry import *
from material import *
from mathutils import *

from random import random, uniform
from math import sin, cos, pi, sqrt

# =============================================================================

class ParticleGeometry(Geometry):

    def __init__(self, particlePositionData, particleColorData, particleOpacityData, particleSizeData, particleAliveData):
        super().__init__()
        self.setAttribute("vec3",  "particlePosition", particlePositionData)
        self.setAttribute("vec3",  "particleColor",    particleColorData)
        self.setAttribute("float", "particleOpacity",  particleOpacityData)
        self.setAttribute("float", "particleSize",     particleSizeData)
        self.setAttribute("float", "particleAlive",    particleAliveData)
        self.vertexCount = len(particlePositionData)

# =============================================================================

class ParticleMaterial(Material):

    def __init__(self, texture=None, additiveBlending=False, alphaTest=0.5):

        # vertex shader code
        vsCode = """
        in vec3  particlePosition;        
        in vec3  particleColor;
        in float particleOpacity;
        in float particleSize;
        in float particleAlive;

        out vec4  rgbaColor;
        out float alive;
        
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;

        // all components are in the range [0...1]
        vec3 hsv_to_rgb(vec3 hsv)
        {
            vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
            vec3 p = abs(fract(hsv.xxx + K.xyz) * 6.0 - K.www);
            return hsv.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), hsv.y);
        }

        void main()
        {
            rgbaColor = vec4( hsv_to_rgb(particleColor), particleOpacity );
            alive = particleAlive;
            vec4 eyePosition = viewMatrix * modelMatrix * vec4(particlePosition, 1.0);
            gl_PointSize = 500 * particleSize / length(eyePosition);
            gl_Position = projectionMatrix * eyePosition;
        }
        """

        # fragment shader code
        fsCode = """
        in vec4 rgbaColor;
        in float alive;
        uniform sampler2D image;
        uniform float alphaTest;
        void main()
        {             
            if (alive < 0.5)
                discard;
            
            vec4 imageColor = texture(image, gl_PointCoord);
            if (imageColor.a < alphaTest)
                discard;
                
            gl_FragColor = rgbaColor * imageColor;
        }
        """

        # initialize shaders
        super().__init__(vsCode, fsCode)
        
        # set render values
        self.drawStyle = GL_POINTS
        self.additiveBlending = additiveBlending
        
        # set uniform values
        self.setUniform( "sampler2D", "image", texture )
        self.setUniform( "float", "alphaTest", alphaTest )
        
# =============================================================================

# Note: update is not defined as a Particle class method
#   because it depends on external data (gravity, tweens, deathAge, etc.)

class Particle(object):

    def __init__(self):
        super().__init__()
        self.position = [0,0,0]
        self.velocity = [0,1,0]
        self.color = [1,0,0]
        self.opacity = 1
        self.size = 1
        self.age = 0
        self.alive = 0
        self.index = -1
                
# =============================================================================
        
class ParticleEngine(Mesh):

    # style = "box"    -> 
    #   vec3 positionBase/Spread, velocityBase/Spread
    # style = "sphere" -> 
    #   vec3 positionBase = center of sphere
    #   float positionSpread = maximum distance from center 
    #   float velocityBase/Spread = speed in direction away from center 
    
    def __init__(self, style="sphere",
                       particlesPerSecond=100, particleDeathAge=3,
                       emitterDeathAge=10,
                       positionBase=[0,0,0], positionSpread=0,
                       velocityBase=1, velocitySpread=0,
                       gravity=[0,0,0],
                       colorBase=[1,0,0], colorSpread=[0,0,0], colorTween=None,
                       opacityBase=1, opacitySpread=0, opacityTween=None,
                       sizeBase=1, sizeSpread=0, sizeTween=None,
                       additiveBlending=False,
                       particleTexture=None):

        # store particle initialization parameters
        self.style = style
        self.positionBase   = positionBase
        self.positionSpread = positionSpread
        self.velocityBase   = velocityBase
        self.velocitySpread = velocitySpread
        self.gravity        = gravity
        self.colorBase      = colorBase
        self.colorSpread    = colorSpread
        self.colorTween     = colorTween
        self.opacityBase    = opacityBase
        self.opacitySpread  = opacitySpread
        self.opacityTween   = opacityTween
        self.sizeBase       = sizeBase
        self.sizeSpread     = sizeSpread
        self.sizeTween      = sizeTween
        
        self.particleList = []
        
        # global properties particle setting data something something
        self.particleDeathAge = particleDeathAge
        
        # emitter properties
        self.particlesPerSecond = particlesPerSecond
        self.emitterAge = 0
        self.emitterAlive = True
        self.emitterDeathAge = emitterDeathAge
        
        # maximum number of particles that could be active at any given time
        self.particleCount = self.particlesPerSecond * min(self.particleDeathAge, self.emitterDeathAge)         
        
        # initialize all the particles
        for index in range(self.particleCount):
            
            particle = Particle()
            self.initializeParticle(particle)
            particle.alive = 0
            particle.index = index
            self.particleList.append(particle)

        # initialize all attribute data
        particlePositionData = []
        particleColorData    = []
        particleOpacityData  = []
        particleSizeData     = []
        particleAliveData    = []

        for particle in self.particleList:
            particlePositionData.append( particle.position )
            particleColorData.append( particle.color )
            particleOpacityData.append( particle.opacity )
            particleSizeData.append( particle.size )
            particleAliveData.append( particle.alive )

        # initialize associated geometry, material, and mesh
        self.particleGeometry = ParticleGeometry(
            particlePositionData = particlePositionData,
            particleColorData    = particleColorData,
            particleOpacityData  = particleOpacityData,
            particleSizeData     = particleSizeData,
            particleAliveData    = particleAliveData )
            
        self.particleMaterial = ParticleMaterial(texture=particleTexture, additiveBlending=additiveBlending)
        
        super().__init__( self.particleGeometry, self.particleMaterial )
        
        
    def initializeParticle(self, particle):
        
        # initial position and velocity depend on emitter style
        if self.style == "box":
            particle.position = RandomUtils.randomBoxVec3(self.positionBase, self.positionSpread)
            particle.velocity = RandomUtils.randomBoxVec3(self.velocityBase, self.velocitySpread)
        elif self.style == "sphere":
            ux,uy,uz = RandomUtils.randomUnitSphereVec3()
            cx,cy,cz = self.positionBase
            r = uniform(0, self.positionSpread)
            particle.position = [cx+r*ux, cy+r*uy, cz+r*uz]               
            s = RandomUtils.randomFloat(self.velocityBase, self.velocitySpread)
            particle.velocity = [s*ux, s*uy, s*uz]
        else:
            raise Exception("unknown style set in particle engine")
         
        particle.color   = RandomUtils.randomBoxVec3(self.colorBase, self.colorSpread)
        particle.opacity = RandomUtils.randomFloat(self.opacityBase, self.opacitySpread)
        particle.size    = RandomUtils.randomFloat(self.sizeBase, self.sizeSpread)
        
        particle.age = 0
        
    def updateParticle(self, particle, dt):
    
        # update velocity based on gravity
        particle.velocity[0] += self.gravity[0] * dt
        particle.velocity[1] += self.gravity[1] * dt
        particle.velocity[2] += self.gravity[2] * dt
        
        # update position based on velocity
        particle.position[0] += particle.velocity[0] * dt
        particle.position[1] += particle.velocity[1] * dt
        particle.position[2] += particle.velocity[2] * dt
    
        # use tweens to update particle properties (if present)
        if self.colorTween is not None:
            particle.color = self.colorTween.evaluate(particle.age)
        if self.opacityTween is not None:
            particle.opacity = self.opacityTween.evaluate(particle.age)
        if self.sizeTween is not None:
            particle.size = self.sizeTween.evaluate(particle.age)
            
        # increase particle age
        particle.age += dt
        if particle.age > self.particleDeathAge:
            particle.alive = 0
        
    def update(self, dt):
    
        # store indices of particles that have died
        recycleIndexList = []
        
        # update particle data
        for particle in self.particleList:

            # only update alive particles
            if particle.alive == 1:
                self.updateParticle(particle, dt)
                
                # keep track of particles that just died
                if particle.alive == 0:
                    recycleIndexList.append( particle.index )
                
                # update attribute data
                self.particleGeometry.attributeData["particlePosition"]["value"][particle.index] = particle.position
                self.particleGeometry.attributeData["particleColor"]["value"][particle.index] = particle.color
                self.particleGeometry.attributeData["particleOpacity"]["value"][particle.index] = particle.opacity
                self.particleGeometry.attributeData["particleSize"]["value"][particle.index] = particle.size
                self.particleGeometry.attributeData["particleAlive"]["value"][particle.index] = particle.alive
        
        # flag geometry attributes so updated data is resent to buffers
        self.particleGeometry.attributeData["particlePosition"]["needsUpdate"] = True
        self.particleGeometry.attributeData["particleColor"]["needsUpdate"] = True
        self.particleGeometry.attributeData["particleOpacity"]["needsUpdate"] = True
        self.particleGeometry.attributeData["particleSize"]["needsUpdate"] = True
        self.particleGeometry.attributeData["particleAlive"]["needsUpdate"] = True
        

        # check if particle emitter is still running
        if not self.emitterAlive:
            return
            
        # debug
        # print("Emitter age: " + str(self.emitterAge))
        
        # if no particles have died yet, then there are still particles to activate
        if self.emitterAge < self.particleDeathAge:
            # determine indices of particles to activate
            startIndex = int( self.particlesPerSecond * self.emitterAge )
            endIndex = int( self.particlesPerSecond * (self.emitterAge + dt) )
            if endIndex > self.particleCount:
                endIndex = self.particleCount
            # debug
            # print("Initial activation of particles " + str(startIndex) + " to " + str(endIndex))
            # activate the particles
            for index in range(startIndex, endIndex):
                self.particleList[index].alive = 1
         
        # debug
        # if len(recycleIndexList) > 0:
        #    print("Recycling particles " + str(recycleIndexList))
            
        # since emitter is still running, immediately recycle any dead particles
        for index in recycleIndexList:
            particle = self.particleList[index]
            self.initializeParticle(particle)
            particle.alive = 1
            
        # increase emitter age
        self.emitterAge += dt
        self.emitterAlive = (self.emitterAge < self.emitterDeathAge)
        
    def stop(self):
        
        self.emitterAlive = False
        
        # age all the particles
        for particle in self.particleList:
            # all particles will die on the next frame; attribute data will be updated
            particle.age = self.particleDeathAge
        
    def reset(self):

        self.emitterAge = 0
        self.emitterAlive = True
        
        # re-initialize all the particles
        for particle in self.particleList:
            self.initializeParticle(particle)
            particle.age = self.particleDeathAge
            particle.alive = 0
        
        
# =============================================================================
