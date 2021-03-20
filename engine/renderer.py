from typing import List

import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

from engine.drawing import Drawing


class Renderer:
    """
    Core of the Engine
    """

    def __init__(self):
        """
        Initialize and create GLUT window
        """
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
        glutCreateWindow("OpenGL")
        glutFullScreen()

        glEnable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnableClientState(GL_VERTEX_ARRAY)

        # Modify matrices for screen size
        width = glutGet(GLUT_SCREEN_WIDTH)
        height = glutGet(GLUT_SCREEN_HEIGHT)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        aspect = width / height
        glOrtho(-aspect, aspect, 1, -1, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    @staticmethod
    def render(drawings_list: List[Drawing]):
        """
        Draw all sprites
        :param drawings_list: List of sprites to draw
        :return:
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        sorted_drawings_list = sorted(drawings_list, key=lambda x: x.position[2])
        for drawing in sorted_drawings_list:
            drawing.render()

        glFlush()
        glutSwapBuffers()

    def animate(self, drawings_list: List[Drawing]):
        """
        Perform one step of animation
        :param drawings_list: List of sprites to animate
        :return:
        """
        for drawing in drawings_list:
            drawing.animation()

        glutPostRedisplay()

    @staticmethod
    def create_texture(image: np.ndarray) -> int:
        """
        Create a texture from image represented by ndarray
        :param image: Image to build texture
        :return: Texture ID
        """
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D,
                     0,
                     GL_RGBA,
                     image.shape[1], image.shape[0],
                     0,
                     GL_RGBA,
                     GL_UNSIGNED_BYTE,
                     image)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)
        return texid

    @staticmethod
    def create_texture_from_file(filename: str) -> int:
        """
        Create a texture from image loaded by the filename
        :param filename: Path to image with the texture
        :return: Texture ID
        """
        image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
        return Renderer.create_texture(image)

    @staticmethod
    def create_shader(shader_type, source: str):
        """
        Compile shader from string
        :param shader_type:  Type of shader
        :param source: Code of the shader represented by the string
        :return: Shader ID
        """
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        result = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if not result:
            raise RuntimeError(glGetShaderInfoLog(shader))

        shader_program = glCreateProgram()
        glAttachShader(shader_program, shader)
        glLinkProgram(shader_program)
        return shader_program
