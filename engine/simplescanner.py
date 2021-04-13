import cv2
import numpy as np


class SimpleScanner:
    """
    Scanner of objects on white surface
    """

    def __init__(self):
        """
        Initialize AR markers detector
        """
        self._aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self._aruco_params = cv2.aruco.DetectorParameters_create()

        self._marker_top_left_id = 3
        self._marker_top_right_id = 1
        self._marker_bottom_left_id = 4
        self._marker_bottom_right_id = 2

        # Target size of scanned image in pixels
        self.target_w = 800
        self.target_h = 600

    def scan(
            self,
            frame: np.ndarray,
    ) -> np.ndarray:
        """
        Scan fish from image represented by ndarray
        :param frame: Photo of a fish from an opencv image
        :return: Aligned image of a fish
        """
        corners, ids, rejected = cv2.aruco.detectMarkers(frame, self._aruco_dict,
                                                         parameters=self._aruco_params)

        top_left, top_right, bottom_right, bottom_left = None, None, None, None

        if len(corners) > 0:
            ids = ids.flatten()
            for (marker_corner, marker_id) in zip(corners, ids):
                corners = marker_corner.reshape((4, 2))
                if marker_id == self._marker_top_left_id:
                    top_left, _, _, _ = corners
                elif marker_id == self._marker_top_right_id:
                    _, top_right, _, _ = corners
                elif marker_id == self._marker_bottom_right_id:
                    _, _, bottom_right, _ = corners
                elif marker_id == self._marker_bottom_left_id:
                    _, _, _, bottom_left = corners

        if (top_left is None) or (top_right is None) or (bottom_right is None) or (bottom_left is None):
            raise ValueError("Markers in the image are not found")
        else:
            tr = (int(top_right[0]), int(top_right[1]))
            br = (int(bottom_right[0]), int(bottom_right[1]))
            bl = (int(bottom_left[0]), int(bottom_left[1]))
            tl = (int(top_left[0]), int(top_left[1]))

            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))

            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))

            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")

            rect = np.array((tl, tr, br, bl)).astype("float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))

            return warped

    def remove_background(
            self,
            frame: np.ndarray,
    ) -> np.ndarray:
        """
        Remove background from the fish image
        :param frame: Aligned image of a fish
        :return: OpenCV image with alpha channel
        """
        frame = cv2.resize(frame, (self.target_w, self.target_h))

        # TODO: remove this fix for final version
        frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        ret, mask = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Remove markers
        marker_size = 130
        mask = cv2.rectangle(mask, (0, 0), (marker_size, marker_size), 255, -1)
        mask = cv2.rectangle(mask, (self.target_w - marker_size, 0), (self.target_w, marker_size), 255, -1)
        mask = cv2.rectangle(mask, (self.target_w - marker_size, self.target_h - marker_size),
                             (self.target_w, self.target_h), 255, -1)
        mask = cv2.rectangle(mask, (0, self.target_h - marker_size), (marker_size, self.target_h), 255, -1)

        mask_filled = mask.copy()
        cv2.floodFill(mask_filled, np.zeros((self.target_h + 2, self.target_w + 2), np.uint8), (0, 0), 0)
        mask_filled += 255 - mask

        filtered_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
        filtered_frame[..., 3] = mask_filled

        return filtered_frame


'''
if __name__ == '__main__':
    scanner = SimpleScanner()
    files = glob('/home/david/PycharmProjects/FishScanner/photos/*.jpg')
    for filename in files:
        frame = cv2.imread(filename)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_frame = scanner.scan(frame)
        processed_frame = scanner.remove_background(processed_frame)

        cv2.imshow('fish', processed_frame)
        cv2.waitKey(0)
'''
