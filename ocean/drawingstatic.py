from engine.drawing import Drawing


class DrawingStatic(Drawing):
    """
    Sprite for static objects
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
        super(DrawingStatic, self).__init__(texid, grid_x, grid_y, shader)
