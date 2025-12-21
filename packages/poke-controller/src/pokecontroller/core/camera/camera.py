import logging
from typing import overload

import cv2

from pokecontroller.core.image import RawImage
from pokecontroller.utils.platform import is_windows

logger = logging.getLogger(__name__)


class PokeControllerCameraException(Exception):
    pass


class Camera:
    def __init__(
        self,
        *,
        frame_size: tuple[int, int] = (1280, 720),
    ) -> None:
        self._video_capture: cv2.VideoCapture | None = None
        self._frame: RawImage | None = None
        self._frame_size = frame_size

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

    @property
    def frame(self) -> RawImage | None:
        return self._frame

    @overload
    def open(self, *, camera_id: int) -> None: ...

    @overload
    def open(self, *, camera_path: str) -> None: ...

    def open(
        self,
        *,
        camera_id: int | None = None,
        camera_path: str | None = None,
    ) -> None:
        self.close()

        if is_windows():
            logger.debug("Windows OS")
            if camera_id is not None:
                self._video_capture = cv2.VideoCapture(
                    index=camera_id, apiPreference=cv2.CAP_DSHOW
                )
            elif camera_path is not None:
                self._video_capture = cv2.VideoCapture(
                    filename=camera_path, apiPreference=cv2.CAP_DSHOW
                )
            else:
                raise PokeControllerCameraException(
                    "Camera ID or Name is not specified."
                )
        else:
            logger.debug("Not Windows OS")
            if camera_id is not None:
                self._video_capture = cv2.VideoCapture(index=camera_id)
            elif camera_path is not None:
                self._video_capture = cv2.VideoCapture(filename=camera_path)
            else:
                raise PokeControllerCameraException(
                    "Camera ID or Name is not specified."
                )

        if not self.is_opened:
            logger.error(f"Camera ID {camera_id} cannot open.")
            return

        logger.debug(f"Camera ID {camera_id} opened successfully.")
        vc = self._video_capture
        vc.set(cv2.CAP_PROP_FRAME_WIDTH, float(self._frame_size[0]))
        vc.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self._frame_size[1]))

    def close(self) -> None:
        if (vc := self._video_capture) is None:
            logger.debug("Camera is not opened")
            return
        if vc.isOpened():
            logger.debug("Closing camera")
            vc.release()
            logging.debug("Camera closed")
        self._video_capture = None

    def read(self) -> tuple[bool, RawImage | None]:
        if (vc := self._video_capture) is None:
            return False, None

        if vc.isOpened():
            success, self._frame = vc.read()
            return success, self._frame
        return False, None
