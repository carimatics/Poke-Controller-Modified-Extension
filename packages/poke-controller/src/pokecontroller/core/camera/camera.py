import logging

import cv2

from ..image import RawImage
from ..platform import is_windows

logger = logging.getLogger(__name__)


class Camera:
    def __init__(
        self,
        *,
        frame_size: tuple[int, int] = (1280, 720),
        fps: int = 45,
    ) -> None:
        self._video_capture: cv2.VideoCapture | None = None
        self._frame: RawImage | None = None
        self._frame_size = frame_size
        self._fps = fps

    @property
    def is_opened(self) -> bool:
        if self._video_capture is None:
            logger.debug("Camera is not opened")
            return False
        is_opened = self._video_capture.isOpened()
        logger.debug(f"Camera is_opened: {is_opened}")
        return is_opened

    @property
    def frame_size(self) -> tuple[int, int]:
        return self._frame_size

    @frame_size.setter
    def frame_size(self, size: tuple[int, int]) -> None:
        self._frame_size = size
        self._set_video_capture_frame_size(size)

    @property
    def fps(self) -> int:
        return self._fps

    @fps.setter
    def fps(self, fps: int) -> None:
        self._fps = fps
        self._set_video_capture_fps(fps)

    @property
    def frame(self) -> RawImage | None:
        return self._frame

    def open(self, camera_id: int) -> None:
        self.close()

        if is_windows():
            logger.debug("NT OS")
            self._video_capture = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        else:
            logger.debug("Not NT OS")
            self._video_capture = cv2.VideoCapture(camera_id)

        if not self.is_opened:
            logger.error(f"Camera ID {camera_id} cannot open.")
            return

        logger.debug(f"Camera ID {camera_id} opened successfully.")
        self._set_video_capture_frame_size(self._frame_size)
        self._set_video_capture_fps(self._fps)

    def close(self) -> None:
        if (vc := self._video_capture) is None:
            logger.debug("Camera is not opened")
            return
        if vc.isOpened():
            logger.debug("Closing camera")
            vc.release()
        self._video_capture = None
        logging.debug("Camera closed")

    def read(self) -> tuple[bool, RawImage | None]:
        if (vc := self._video_capture) is None:
            return False, None

        if vc.isOpened():
            success, self._frame = vc.read()
            return success, self._frame
        return False, None

    def _set_video_capture_frame_size(self, size: tuple[int, int]) -> None:
        logger.debug(f"Setting frame size to {size}")
        if (vc := self._video_capture) is None:
            logger.debug("Camera is not opened")
            return
        if vc.isOpened():
            width, height = size
            vc.set(cv2.CAP_PROP_FRAME_WIDTH, float(width))
            vc.set(cv2.CAP_PROP_FRAME_HEIGHT, float(height))
        logger.debug("Frame size set successfully")

    def _set_video_capture_fps(self, fps: int) -> None:
        logger.debug(f"Setting fps to {fps}")
        if (vc := self._video_capture) is None:
            logger.debug("Camera is not opened")
            return
        if vc.isOpened():
            vc.set(cv2.CAP_PROP_FPS, float(fps))
        logger.debug("FPS set successfully")
