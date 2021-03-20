import numpy as np

from engine.drawing import Drawing

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

    def __init__(self, texid: int, grid_x: int = 5, grid_y: int = 5, shader: int = 0):
        """
        Set default position of fish and select default vector of moving
        :param texid: ID of texture
        :param grid_x: Mesh elements along axis X
        :param grid_y: Mesh elements along axis Y
        :param shader: ID of shader. Select 0 if you need no shader
        """
        super(DrawingFish, self).__init__(texid, grid_x, grid_y, shader)

        self.scale = np.array([0.4, 0.3, 0.3])
        self.vector = np.array([np.random.uniform(0.002, 0.003),
                                np.random.uniform(-0.0006, 0.0006), 0.0])

        self.left = -1.5
        self.right = 1.5
        self.top = -0.7
        self.bottom = 0.3
        self.position = np.array([np.random.uniform(self.left, self.right),
                                  np.random.uniform(self.top, self.bottom), 0.])
        if np.random.randint(2) == 0:
            self.vector[0] = -self.vector[0]
            self.scale[0] = -self.scale[0]

    def animation(self):
        """
        Logic of movement of the fish
        :return:
        """
        self.position += self.vector

        # If we near border go to the other direction
        if self.position[0] > self.right or self.position[0] < self.left:
            self.vector[0] = -self.vector[0]
            self.rotation_vector[1] = 5.0

        if self.position[1] > self.top or self.position[1] < self.bottom:
            self.vector[1] = -self.vector[1]

        self.rotate[1] = (self.rotate[1] + self.rotation_vector[1]) % 360

        if self.rotate[1] % 180 == 0:
            self.rotation_vector[1] = 0.0
