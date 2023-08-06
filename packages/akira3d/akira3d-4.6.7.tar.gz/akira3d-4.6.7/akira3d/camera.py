import glm
import pygame as pg


class Camera:
    def __init__(self, app, position=(0,0,4), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = app.size[0] / app.size[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        self.FOV = 80
        self.NEAR = 0.3
        self.FAR = 100
        self.px, self.pn = 90, -90

        self.gvm()
        self.gpm()

    def rotate(self, angle):
        if angle != None:
            self.yaw +=  angle[0]
            self.pitch -=  angle[1]
            self.pitch = max(self.pn, min(self.px, self.pitch))

    def ucv(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0,1,0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self, pos=None, angle=None):
        self.move(pos)
        self.rotate(angle)
        self.ucv()
        self.gvm()

    def move(self, pos):
        if pos != None: self.position = pos

    def gvm(self): self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)
    def gpm(self): self.m_proj = glm.perspective(glm.radians(self.FOV), self.aspect_ratio, self.NEAR, self.FAR)
