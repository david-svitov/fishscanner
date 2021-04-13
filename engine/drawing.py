from __future__ import annotations

from typing import List

import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
import numpy as np


class Drawing:
    """
    Draw and animate 3D sprite
    """

    def __init__(
            self,
            texid: int,
            grid_x: int = 5,
            grid_y: int = 5,
            shader: int = 0,
    ):
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

        self._vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self._vao)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)

        self._vbo_vertices.bind()
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
        self._vbo_texcoords.bind()
        gl.glTexCoordPointer(3, gl.GL_FLOAT, 0, None)

        gl.glBindVertexArray(0)

    def _apply_transforms(self) -> None:
        """
        Apply translation, rotation and scaling to the sprite
        :return:
        """
        gl.glTranslatef(*self.position)
        gl.glRotatef(self.rotate[0], 1, 0, 0)
        gl.glRotatef(self.rotate[1], 0, 1, 0)
        gl.glRotatef(self.rotate[2], 0, 0, 1)
        gl.glScalef(*self.scale)

    def _draw_mesh(self) -> None:
        """
        Render sprite's mesh
        :return:
        """
        gl.glPushMatrix()
        self._apply_transforms()
        gl.glBindVertexArray(self._vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self._vertices_count)
        gl.glBindVertexArray(0)
        gl.glPopMatrix()

    def render(self) -> None:
        """
        Render sprite with attached texture and shader
        :return:
        """
        gl.glColor3f(*self.color)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._texid)
        gl.glUseProgram(self._shader)
        if self._shader != 0:
            # Send timer value to the shader
            location = gl.glGetUniformLocation(self._shader, "timer")
            gl.glUniform1f(location, self._time_counter)
            self._time_counter += self.step_animation_timer
            # If timer came to border - go back
            if self._time_counter >= self.max_animation_timer or self._time_counter <= 0:
                self.step_animation_timer = -self.step_animation_timer
        self._draw_mesh()
        gl.glUseProgram(0)

    def animation(self) -> None:
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
    def _mesh_create(
            grid_size_x: int = 5,
            grid_size_y: int = 5,
    ) -> List[float]:
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
