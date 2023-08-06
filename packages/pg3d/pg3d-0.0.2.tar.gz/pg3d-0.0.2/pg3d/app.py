import pygame as pg
import math as m
from pygame.colordict import THECOLORS
from typing import Optional, Tuple, Sequence
import pg3d.MatrixMath.matrix as mm
from pg3d.camera import Camera
from pg3d.triangle import Triangle


class App:
    def __init__(
        self,
        dimensions=(1000, 700),
        cam_pos=[0, 0, 0],
        BG_COLOR=(0, 0, 0),
        LINE_COLOR=(255, 255, 255),
        VERTEX_SIZE=2,
        stats=False,
        fullscreen=False,
        mouse_look=False,
    ):
        pg.init()

        if fullscreen:
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN, vsync=1)
            self.dimensions = (
                self.width,
                self.height,
            ) = pg.display.get_surface().get_size()
        else:
            self.dimensions = self.width, self.height = dimensions
            self.screen = pg.display.set_mode(self.dimensions, pg.RESIZABLE, vsync=1)

        self.half_width, self.half_height = self.width / 2, self.height / 2
        self.FPS: int = 60
        self.screen = pg.display.set_mode(self.dimensions, pg.RESIZABLE, vsync=1)
        self.clock = pg.time.Clock()
        self.stats = stats

        if mouse_look:
            pg.mouse.set_visible(0)
        self.mouse_look = mouse_look

        self.BG_COLOR = BG_COLOR
        self.LINE_COLOR = LINE_COLOR
        self.VERTEX_SIZE = VERTEX_SIZE

        self.camera = Camera(self, cam_pos)

        self.mesh = []

        self.fov = 90
        self.zf = 1000
        self.zn = 0.1

        m00 = (self.height / self.width) * (1 / m.tan(m.radians(self.fov / 2)))
        m11 = 1 / m.tan(m.radians(self.fov / 2))
        m22 = self.zf / (self.zf - self.zn)
        m32 = -self.zn * (self.zf / (self.zf - self.zn))

        self.projection_matrix = mm.Matrix(
            [[m00, 0, 0, 0], [0, m11, 0, 0], [0, 0, m22, 1], [0, 0, m32, 0]]
        )

    def create_projection_matrix(self):
        m00 = (self.height / self.width) * (1 / m.tan(m.radians(self.fov / 2)))
        m11 = 1 / m.tan(m.radians(self.fov / 2))
        m22 = self.zf / (self.zf - self.zn)
        m32 = -self.zn * (self.zf / (self.zf - self.zn))

        self.projection_matrix = mm.Matrix(
            [[m00, 0, 0, 0], [0, m11, 0, 0], [0, 0, m22, 1], [0, 0, m32, 0]]
        )

    def add_point(self, point: Sequence[float]):
        self.mesh.append([point])

    def add_triangle(self, triangle):
        self.mesh.append(triangle)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        for shape in self.mesh:
            if type(shape) == Triangle:
                shape.project()
            else:
                for point in shape:
                    projected = point.project(
                        self.projection_matrix, self.camera.cam_mat()
                    )
                    if projected is not None:
                        x, y, z = projected
                        if point.vertex == True:
                            pg.draw.circle(
                                self.screen, self.LINE_COLOR, (x, y), self.VERTEX_SIZE
                            )

    def display_stats(self):
        font = pg.font.Font("freesansbold.ttf", 10)
        fov = font.render(f"fov = {self.fov}", True, (0, 255, 0))
        fps = font.render(f"fps = {round(self.clock.get_fps())}", True, (0, 255, 0))
        dimensions = font.render(f"dimensions = {self.dimensions}", True, (0, 255, 0))
        self.screen.blit(fov, (5, 5))
        self.screen.blit(fps, (5, 15))
        self.screen.blit(dimensions, (5, 25))

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                exit()

            elif event.type == pg.MOUSEWHEEL:
                if event.y == 1:
                    self.fov -= 1
                else:
                    self.fov += 1
                self.create_projection_matrix()

            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                self.dimensions = self.width, self.height = (event.w, event.h)
                self.half_width, self.half_height = self.width / 2, self.height / 2
                self.create_projection_matrix()

            elif (event.type == pg.MOUSEMOTION) and (self.mouse_look == True):
                self.camera.mouse_look(event.rel)

    def run(self):
        while True:
            self.draw()
            self.camera.movement()
            self.check_events()
            if self.stats:
                self.display_stats()

            if self.mouse_look == True:
                pg.mouse.set_pos((self.half_width, self.half_height))

            pg.display.set_caption(f"{round(self.clock.get_fps())} FPS")
            pg.display.update()
            self.clock.tick(self.FPS)
