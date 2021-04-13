from engine.drawing import Drawing

SEAWEED_SHADER_CODE = """
uniform float timer;
vec4 sine_wave(vec4 p) {
    float pi = 3.14159;
    float A_x = 0.02;
    float A_y = 0.02;
    float w = 10.0 * pi;
    float t = 30.0*pi/180.0;
    float y = sin( w*timer*p.y + t) * A_y;
    float x = sin( w*timer*p.y + t) * A_x;
    return vec4(p.x+x, p.y+y, p.z, p.w);
}
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * sine_wave(gl_Vertex);
    gl_FrontColor = gl_Color;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
}
"""


class DrawingSeaweed(Drawing):
    """
    Sprite for seaweed
    """

    def __init__(
            self,
            texid: int,
            grid_x: int = 5,
            grid_y: int = 5,
            shader: int = 0,
    ):
        """
        Initialize seaweed as default sprite. All the magic happens in the shader
        :param texid: ID of texture
        :param grid_x: Mesh elements along axis X
        :param grid_y: Mesh elements along axis Y
        :param shader: ID of shader. Select 0 if you need no shader
        """
        super(DrawingSeaweed, self).__init__(texid, grid_x, grid_y, shader)
