import os

import cv2

from ..image import RawImage


class Camera:
    def __init__(self, *, frame_size: tuple[int, int] = (1280, 720), fps: int = 45):
        self._video_capture: cv2.VideoCapture | None = None
        self._frame: RawImage | None = None
        self._frame_size = frame_size
        self._fps = fps

    @property
    def is_opened(self) -> bool:
        if self._video_capture is None:
            return False
        return self._video_capture.isOpened()

    @property
    def frame_size(self) -> tuple[int, int]:
        return self._frame_size

    @frame_size.setter
    def frame_size(self, size: tuple[int, int]) -> None:
        self._frame_size = size
        if (vc := self._video_capture) is None:
            return
        if vc.isOpened():
            width, height = size
            vc.set(cv2.CAP_PROP_FRAME_WIDTH, float(width))
            vc.set(cv2.CAP_PROP_FRAME_HEIGHT, float(height))

    @property
    def fps(self) -> int:
        return self._fps

    @fps.setter
    def fps(self, fps: int) -> None:
        self._fps = fps
        if (vc := self._video_capture) is None:
            return
        if vc.isOpened():
            vc.set(cv2.CAP_PROP_FPS, float(fps))

    @property
    def frame(self) -> RawImage | None:
        return self._frame

    def open(self, camera_id: int) -> None:
        self.close()

        match os.name:
            case "nt":  # Windows
                self._video_capture = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
            case _:
                self._video_capture = cv2.VideoCapture(camera_id)

        if not self.is_opened:
            return

        self.frame_size = self._frame_size
        self.fps = self._fps

    def close(self) -> None:
        if (vc := self._video_capture) is None:
            return
        if vc.isOpened():
            vc.release()
        self._video_capture = None

    def read(self) -> bool:
        if (vc := self._video_capture) is None:
            return False

        if vc.isOpened():
            success, self._frame = vc.read()
            return success
        return False
