import glm
import pygame as pg
import moderngl as mgl
from array import array
import time, math
from . import model
from .camera import Camera
from .light import Light
from .mesh import Mesh
from .model import *
import pyautogui
size = pyautogui.size()
w, h = size[0], size[1]


def cos(a):
    return math.cos(math.radians(a))


def sin(a):
    return math.sin(math.radians(a))


def tg(a):
    return math.tan(math.radians(a))


def li(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def l(x, y):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5


class GraphicsEngine:
    def __init__(self, size=None):
        self.full = bool(size)
        self.size = (size if self.full else (w, h))
        print(self.full, size, self.size)
        self.init()
        self.defDr = lambda surf: 0
        self.defEv = lambda: 0
        self.time = 0
        self.delta_time = 0
        self.fps = 1
        self.mesh = Mesh(self)
        self.light = Light()
        self.scene = self.Scene(self)
        self.validate = False
        self.clock = pg.time.Clock()

    class Scene:
        def __init__(self, app):
            self.scene = {"objects":{}, "render":[], "shadow":[]}
            self.scs = {}
            self.app = app
            self.ctx = app.ctx
            self.mesh = app.mesh
            self.sky = model.AdvancedSkyBox(self.app, 'default')
            self.name = None
            self.depth_texture = self.mesh.texture.textures['dt']
            self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

        def d1(self, _):
            _.render()

        def d2(self, _):
            _.render_shadow()

        def add(self, scene, name, obj, render, shadow):
            self.scs[scene]['objects'][name] = obj
            if render: self.scs[scene]['render'].append(name)
            if shadow: self.scs[scene]['shadow'].append(name)

        def render(self):
            if self.name:
                if self.sky: self.sky.render()
                self.depth_fbo.clear()
                self.depth_fbo.use()

                # list(self.d2(_) for _ in self.scs[self.name].values())
                [self.scs[self.name]['objects'][_].render_shadow() for _ in self.scs[self.name]['shadow']]
                # list(map(self.d2, self.scs[self.name].values()))

                self.app.ctx.screen.use()

                # list(self.d1(_) for _ in self.scs[self.name].values())
                [self.scs[self.name]['objects'][_].render() for _ in self.scs[self.name]['render']]
                # list(map(self.d1, self.scs[self.name].values()))


        def destroy(self): self.depth_fbo.release()

    class Pointer():
        def __init__(self, cam, pos):
            self.cam = cam
            self.pos = pos
            self.fov = cam.FOV
            self.nfov = self.fov//cam.aspect_ratio
            self.angle = [0, 0]
            self.fa = 0

        def behind(self):
            toOther = self.pos - self.cam.position
            return glm.dot(self.cam.forward, toOther) < 0

        def update(self):
            pos = self.cam.position
            self.fa = math.degrees(math.atan2(self.pos.y - pos.y, self.pos.x - pos.x))
            self.fa += self.cam.yaw
            self.fb = math.degrees(math.atan2(self.pos.y - pos.y, self.pos.z - pos.z))
            self.fb += self.cam.pitch
            posn = [li(((cos(-self.fov), sin(-self.fov)), (cos(0), sin(0))), ((0, 0), (cos(-self.fa), sin(-self.fa)))), li(((cos(-self.nfov), sin(-self.nfov)), (cos(0), sin(0))), ((0, 0), (cos(-self.fb), sin(-self.fb))))]
            m = l((cos(-self.fov), sin(-self.fov)), posn[0]) / l((cos(-self.fov), sin(-self.fov)), (cos(0), sin(0)))
            m1 = l((cos(-self.nfov), sin(-self.nfov)), posn[1]) / l((cos(-self.nfov), sin(-self.nfov)), (cos(0), sin(0)))
            self.angle = [m, m1]

    def quit(self):
        self.mesh.destroy()
        self.scene.destroy()
        pg.quit()
        exit()

    def init(self):
        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(self.size, flags=pg.OPENGL | pg.DOUBLEBUF) if self.full else pg.display.set_mode(self.size, flags=pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN)
        self.ctx = mgl.create_context()
        #self.ctx.front_face = 'cw' | mgl.CULL_FACE
        self.ctx.enable(flags=mgl.DEPTH_TEST)

        self.clock = pg.time.Clock()
        self.camera = Camera(self)

        self.surf = pg.Surface(self.size, flags=pg.SRCALPHA)
        self.pg_texture = self.ctx.texture(self.size, 4)
        self.pg_texture.filter = mgl.NEAREST, mgl.NEAREST
        self.pg_texture.swizzle = 'BGRA'
        self.texture_program = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec2 in_vert;
                in vec2 in_texcoord;
                out vec2 uv;
                void main() {
                    uv = in_texcoord;
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                uniform sampler2D surface;
                out vec4 f_color;
                in vec2 uv;
                void main() {
                    f_color = texture(surface, uv);
                }
            """)
        self.texture_program['surface'] = 0
        buffer = self.ctx.buffer(
            data=array('f', [
                -1.0, 1.0, 0.0, 1.0,
                -1.0, -1.0, 0.0, 0.0,
                1.0, 1.0, 1.0, 1.0,
                1.0, -1.0, 1.0, 0.0]))
        self.quad_fs = self.ctx.vertex_array(self.texture_program, [(buffer, "2f 2f", "in_vert", "in_texcoord")])

    def render(self):
        self.ctx.clear(0,255,0)
        self.scene.render()
        self.ctx.disable(mgl.BLEND)
        self.defDr(self.surf)
        self.surf = pg.transform.flip(self.surf, flip_x=False, flip_y=True)
        texture_data = self.surf.get_view('1')
        self.pg_texture.write(texture_data)
        self.ctx.enable(mgl.BLEND)
        self.pg_texture.use(location=0)
        self.quad_fs.render(mode=mgl.TRIANGLE_STRIP)
        pg.display.flip()

    def update(self):
        nTime = time.time()
        self.defEv()
        self.render()
        self.fps = 1 / (time.time()-nTime) if (time.time()-nTime) != 0 else 0.00001
