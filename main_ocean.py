from functools import partial
from glob import glob
from typing import List

import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

from engine.drawing import Drawing
from engine.simplescanner import SimpleScanner
from ocean.drawingfish import DrawingFish, FISH_SHADER_CODE
from ocean.drawingseaweed import DrawingSeaweed, SEAWEED_SHADER_CODE
from ocean.drawingstatic import DrawingStatic
from engine.renderer import Renderer


def create_back_layer(filename: str, z: float, shader: int = 0) -> DrawingStatic:
    drawing_back = DrawingStatic(Renderer.create_texture_from_file(filename), shader=shader)
    drawing_back.position = np.array([0, 0., z])
    drawing_back.scale = np.array([3.6, 2.0, 1.0])
    return drawing_back


def draw_sails(drawings_list: List[Drawing], shader: int):
    drawing = DrawingSeaweed(Renderer.create_texture_from_file('ocean/images/sail_1.png'), shader=shader)
    drawing.position = np.array([1.2, -0.43, -0.77])
    drawing.scale = np.array([0.6, 0.4, 1.0])
    drawings_list.append(drawing)

    drawing = DrawingSeaweed(Renderer.create_texture_from_file('ocean/images/sail_2.png'), shader=shader)
    drawing.position = np.array([1.6, -0.34, -0.77])
    drawing.scale = np.array([0.3, 0.5, 1.0])
    drawings_list.append(drawing)

    drawing = DrawingSeaweed(Renderer.create_texture_from_file('ocean/images/sail_3.png'), shader=shader)
    drawing.position = np.array([1.7, -0.71, -0.77])
    drawing.scale = np.array([0.2, 0.3, 1.0])
    drawings_list.append(drawing)


def draw_ocean(drawings_list: List[Drawing]):
    seaweed_shader_program = Renderer.create_shader(GL_VERTEX_SHADER, SEAWEED_SHADER_CODE)

    drawings_list.append(create_back_layer('ocean/images/back_down.png', -0.8))
    drawings_list.append(create_back_layer('ocean/images/back_middle.png', -0.78))
    drawings_list.append(create_back_layer('ocean/images/back_reef.png', 0.8))

    draw_sails(drawings_list, seaweed_shader_program)

    seaweed_texture = Renderer.create_texture_from_file('ocean/images/seaweed_2.png')
    # Draw seaweed under the ship
    drawing = DrawingSeaweed(seaweed_texture, shader=seaweed_shader_program)
    drawing.position = np.array([1.2, 0.4, -0.75])
    drawing.scale = np.array([0.8, 0.4, 1.0])
    drawings_list.append(drawing)

    seaweed_texture = Renderer.create_texture_from_file('ocean/images/seaweed_1.png')
    # Draw seaweed in the right corner
    drawing = DrawingSeaweed(seaweed_texture, shader=seaweed_shader_program)
    drawing.position = np.array([1.2, 1.0, 0.9])
    drawing.scale = np.array([0.8, 1.4, 1.0])
    # drawing.color = np.array([0.5, 0.5, 1.0])
    drawings_list.append(drawing)

    # Draw seaweed in the front of the rock
    drawing = DrawingSeaweed(seaweed_texture, shader=seaweed_shader_program)
    drawing.position = np.array([0.2, 0.15, -0.7])
    drawing.scale = np.array([0.4, 0.4, 1.0])
    # drawing.color = np.array([0.6, 0.6, 1.0])
    drawings_list.append(drawing)

    seaweed_texture = Renderer.create_texture_from_file('ocean/images/seaweed_3.png')
    # Draw seaweed in the left corner
    drawing = DrawingSeaweed(seaweed_texture, shader=seaweed_shader_program)
    drawing.position = np.array([-1.2, 0.6, 0.9])
    drawing.scale = np.array([0.3, 1.0, 1.0])
    # drawing.color = np.array([0.5, 0.5, 1.0])
    drawings_list.append(drawing)

    # Draw seaweed on the background
    drawing = DrawingSeaweed(seaweed_texture, shader=seaweed_shader_program)
    drawing.position = np.array([-0.8, -0.5, -0.795])
    drawing.scale = np.array([0.3, 1.0, 1.0])
    drawing.color = np.array([0.3, 0.3, 0.8])
    drawings_list.append(drawing)

    drawing = DrawingSeaweed(seaweed_texture, shader=seaweed_shader_program)
    drawing.position = np.array([0.0, -0.2, -0.795])
    drawing.scale = np.array([-0.3, 1.0, 1.0])
    drawing.color = np.array([0.3, 0.3, 0.8])
    drawings_list.append(drawing)

    drawing = DrawingSeaweed(seaweed_texture, shader=seaweed_shader_program)
    drawing.position = np.array([-0.4, -0.2, -0.795])
    drawing.scale = np.array([0.1, 0.3, 1.0])
    drawing.color = np.array([0.1, 0.1, 0.4])
    drawings_list.append(drawing)


def main():
    scanner = SimpleScanner()

    glClearColor(0.1, 0.1, 0.2, 1.0)
    renderer = Renderer()
    drawings_list = []
    draw_ocean(drawings_list)

    fish_shader_program = Renderer.create_shader(GL_VERTEX_SHADER, FISH_SHADER_CODE)

    files = glob('./photos/*.jpg')
    for filename in files:
        frame = cv2.imread(filename)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            processed_frame = scanner.scan(frame)
        except ValueError as e:
            print(e)
            continue
        processed_frame = scanner.remove_background(processed_frame)
        drawing = DrawingFish(Renderer.create_texture(processed_frame),
                              shader=fish_shader_program)
        drawings_list.append(drawing)

    glutDisplayFunc(partial(renderer.render, drawings_list))

    def keys_processor(key, x, y):
        if key == b'\x1b':  # esc
            sys.exit(0)

    glutKeyboardFunc(keys_processor)

    timer_msec = int(1000 / 60)

    def animate(value):
        renderer.animate(drawings_list)
        glutTimerFunc(timer_msec, animate, 0)

    glutTimerFunc(timer_msec, animate, 0)

    glutMainLoop()


if __name__ == '__main__':
    main()
