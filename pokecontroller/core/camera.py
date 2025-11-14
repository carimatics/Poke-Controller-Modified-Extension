import os

import cv2

from pokecontroller.core.image import Image


class Camera:
    def __init__(self, frame_size: tuple[int, int] = (1280, 720), fps: int = 45):
        self.camera = None
        self.current_frame = None
        self.frame_size = frame_size
        self.fps = fps

    @property
    def is_opened(self) -> bool:
        if self.camera is None:
            return False
        return self.camera.isOpened()

    def set_frame_size(self, size: tuple[int, int]) -> None:
        self.frame_size = size
        if self.is_opened:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])

    def set_fps(self, fps: int) -> None:
        self.fps = fps
        if self.is_opened:
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)

    def open(self, camera_id: int) -> None:
        self.close()

        if os.name == "nt":
            self.camera = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        else:
            self.camera = cv2.VideoCapture(camera_id)

        if not self.is_opened:
            return

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])
        self.camera.set(cv2.CAP_PROP_FPS, self.fps)

    def close(self) -> None:
        if self.is_opened:
            self.camera.release()
        self.camera = None

    def read_current_frame(self) -> None:
        if self.is_opened:
            _, self.current_frame = self.camera.read()

    def get_current_frame(self) -> Image | None:
        if not self.current_frame:
            return None
        return Image(self.current_frame)
