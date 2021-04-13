from typing import List

import numpy as np

from engine.drawing import Drawing
from ocean.drawingbubble import DrawingBubble

FISH_SHADER_CODE = """
uniform float timer;
vec4 sine_wave(vec4 p) {
    float pi = 3.14159;
    float A_x = 0.001;
    float A_y = 0.01;
    float w = 10.0 * pi;
    float t = 30.0*pi/180.0;
    float y = sin( w*p.x + t) * A_y;
    float x = sin( w*p.x + t) * A_x;
    return vec4(p.x+x, p.y+y, p.z, p.w);
}
void main() {
    gl_Position = sine_wave(gl_ModelViewProjectionMatrix * gl_Vertex);
    gl_FrontColor = gl_Color;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
}
"""


class DrawingFish(Drawing):
    """
    Sprite for drawing of fish
    """

    def __init__(
            self,
            texid: int,
            grid_x: int = 5,
            grid_y: int = 5,
            shader: int = 0,
            bubble_texture_id: int = 0,
    ):
        """
        Set default position of fish and select default vector of moving
        :param texid: ID of texture
        :param grid_x: Mesh elements along axis X
        :param grid_y: Mesh elements along axis Y
        :param shader: ID of shader. Select 0 if you need no shader
        :param bubble_texture_id: ID of a bubble texture
        """
        super(DrawingFish, self).__init__(texid, grid_x, grid_y, shader)

        self.scale = np.array([0.4, 0.3, 0.3])
        self.vector = np.array([0, 0.02, 0.0])
        self.is_alive = True # The fish will be deleted from the drawing list when it False

        self._left = -1.5
        self._right = 1.5
        self._top = -0.7
        self._bottom = 0.3
        self.position = np.array([np.random.uniform(self._left, self._right), -1, 0.])
        if np.random.randint(2) == 0:
            self.scale[0] = -self.scale[0]

        # Parameters for animations
        self._animation_stage = 'init'
        self._init_animation_step = 120
        self._water_resistance = np.random.uniform(0.95, 0.98)

        # To animate bubbles
        self._bubble_texture_id = bubble_texture_id
        self._bubble_random_frequency = 2
        self._bubble_deviation_x = 0
        self._bubble_speed_y = -0.01
        self._bubbles = []

    def _init_fish_velocity(self) -> None:
        """
        Setup initial values for velocity vector
        :return:
        """
        self.vector = np.array([np.random.uniform(0.002, 0.003),
                                np.random.uniform(0.001, 0.002), 0.0])
        if self.scale[0] < 0:
            self.vector[0] = -self.vector[0]
        if np.random.randint(2) == 0:
            self.vector[1] = -self.vector[1]

        self._bubble_random_frequency = 500
        self._bubble_deviation_x = 0.1
        self._bubble_speed_y = -0.005

    def _process_bubbles(self) -> None:
        # randomly create bubble
        if np.random.randint(int(self._bubble_random_frequency)) == 0:
            bubble_x = np.random.uniform(self.position[0], self.position[0] + self.scale[0]/2)
            bubble = DrawingBubble(self._bubble_texture_id,
                                   start_x=bubble_x, start_y=self.position[1])
            bubble.deviation_x = self._bubble_deviation_x
            bubble.speed_y = self._bubble_speed_y
            self._bubbles.append(bubble)

        # delete bubbles when they left the screen
        for bubble in self._bubbles:
            if bubble.position[1] < -1:
                self._bubbles.remove(bubble)

    def animation(self) -> None:
        """
        Logic of movement of the fish
        :return:
        """
        self.position += self.vector
        self._process_bubbles()

        if self._animation_stage == 'init':
            self._init_animation_step -= 1
            self._bubble_random_frequency += 0.1
            self.vector[1] *= self._water_resistance
            # Finis init animation
            if self._init_animation_step == 0:
                self._init_fish_velocity()
                self._animation_stage = 'swim'

        elif self._animation_stage == 'swim':
            # If we near border go to the other direction
            if self.position[0] > self._right or self.position[0] < self._left:
                self.vector[0] = -self.vector[0]
                self.rotation_vector[1] = 5.0

            if self.position[1] < self._top or self.position[1] > self._bottom:
                self.vector[1] = -self.vector[1]

            self.rotate[1] = (self.rotate[1] + self.rotation_vector[1]) % 360

            if self.rotate[1] % 180 == 0:
                self.rotation_vector[1] = 0.0

        elif self._animation_stage == 'finish':
            if self.position[0] > self._right + 1.0 or self.position[0] < self._left - 1.0:
                self.is_alive = False

    def get_child_sprites(self) -> List[Drawing]:
        """
        Return list of bubbles
        :return: List of bubbles
        """
        return self._bubbles

    def go_away(self) -> None:
        """
        Start animation of fish swimming away
        :return:
        """
        self.vector[1] = 0.0
        self.vector[0] *= 2
        self._animation_stage = 'finish'
