from __future__ import annotations
from typing import List

import OpenGL.arrays.vbo as glvbo
import numpy as np
from OpenGL.GL import *


class Drawing:
    """
    Draw and animate 3D sprite
    """

    def __init__(self, texid: int, grid_x: int = 5, grid_y: int = 5, shader: int = 0):
        """
        Setup default position for sprite. Initialize mesh of selected size.
        :param texid: ID of texture
        :param grid_x: Mesh elements along axis X
        :param grid_y: Mesh elements along axis Y
        :param shader: ID of shader. Select 0 if you need no shader
        """

        # Setup default positions of sprite
        self.position = np.array([0, 0., 0.])
        self.rotate = np.array([0., 0., 0.])
        self.scale = np.array([1.0, 1.0, 1.0])
        self.color = np.array([1.0, 1.0, 1.0])

        # Setup default animation settings
        self.max_animation_timer = 1
        self.step_animation_timer = 0.001

        # Setup default vectors for image transformation
        self.vector = np.array([0.0, 0.0, 0.0])
        self.rotation_vector = np.array([0.0, 0.0, 0.0])

        self._texid = texid
        self._shader = shader
        self._time_counter = 0.0

        # Create vertices array for the sprite
        vertices = self._mesh_create(grid_size_x=grid_x, grid_size_y=grid_y)
        self._vertices_count = len(vertices)
        self._vbo_vertices = glvbo.VBO(np.array(vertices, 'f'))
        self._vbo_texcoords = glvbo.VBO(np.array(vertices, 'f') + 0.5)

        self._vao = glGenVertexArrays(1)
        glBindVertexArray(self._vao)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        self._vbo_vertices.bind()
        glVertexPointer(3, GL_FLOAT, 0, None)
        self._vbo_texcoords.bind()
        glTexCoordPointer(3, GL_FLOAT, 0, None)

        glBindVertexArray(0)

    def _apply_transforms(self):
        """
        Apply translation, rotation and scaling to the sprite
        :return:
        """
        glTranslatef(*self.position)
        glRotatef(self.rotate[0], 1, 0, 0)
        glRotatef(self.rotate[1], 0, 1, 0)
        glRotatef(self.rotate[2], 0, 0, 1)
        glScalef(*self.scale)

    def _draw_mesh(self):
        """
        Render sprite's mesh
        :return:
        """
        glPushMatrix()
        self._apply_transforms()
        glBindVertexArray(self._vao)
        glDrawArrays(GL_TRIANGLES, 0, self._vertices_count)
        glBindVertexArray(0)
        glPopMatrix()

    def render(self):
        """
        Render sprite with attached texture and shader
        :return:
        """
        glColor3f(*self.color)
        glBindTexture(GL_TEXTURE_2D, self._texid)
        glUseProgram(self._shader)
        if self._shader != 0:
            # Send timer value to the shader
            location = glGetUniformLocation(self._shader, "timer")
            glUniform1f(location, self._time_counter)
            self._time_counter += self.step_animation_timer
            # If timer came to border - go back
            if self._time_counter >= self.max_animation_timer or self._time_counter <= 0:
                self.step_animation_timer = -self.step_animation_timer
        self._draw_mesh()
        glUseProgram(0)

    def animation(self):
        """
        Override this method to apply animation
        :return:
        """
        pass

    def get_child_sprites(self) -> List[Drawing]:
        """
        Override this method to return all Drawings that child for the current one
        :return: List of child drawings
        """
        return []

    @staticmethod
    def _mesh_create(grid_size_x=5, grid_size_y=5) -> List[float]:
        """
        Create mesh of selected size
        :param grid_size_x: Mesh elements along axis X
        :param grid_size_y: Mesh elements along axis Y
        :return: List of vertices coordinates
        """
        vertices = []
        step_x = 1 / grid_size_x
        step_y = 1 / grid_size_y

        for y in np.arange(-0.5, 0.5, step_y):
            for x in np.arange(-0.5, 0.5, step_x):
                vertices += [x, y, 0.0,
                             x + step_x, y, 0.0,
                             x, y + step_y, 0.0,
                             x + step_x, y, 0.0,
                             x, y + step_y, 0.0,
                             x + step_x, y + step_y, 0.0,
                             ]
        return vertices
