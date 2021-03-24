import math

import numpy as np

from engine.drawing import Drawing


class DrawingBubble(Drawing):
    """
    Sprite for drawing of bubble
    """

    def __init__(self, texid: int, start_x: float = 0., start_y: float = 0.):
        """
        Set starting position for the bubble
        :param texid: ID of texture
        :param start_x: Start X position of the bubble
        :param start_y: Start Y position of the bubble
        """
        super(DrawingBubble, self).__init__(texid, 1, 1, shader=0)

        self.scale = np.array([0.1, 0.1, 1.0])
        self.position = np.array([start_x, start_y, 0.])
        self._start_x = start_x
        self._start_y = start_y

        self._speed_y = -0.005
        self._frequency_x = 10
        self._deviation_x = 0.1


    def animation(self):
        """
        Logic of movement of the bubble
        :return:
        """
        self.position[0] = self._start_x + self._deviation_x * math.sin(self.position[1] * self._frequency_x)
        self.position[1] += self._speed_y
