#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List, TYPE_CHECKING, Sequence

import datetime
import os
from logging import getLogger, DEBUG, NullHandler

from pokecontroller.core import (
    camera as lib_camera,
    image as lib_image,
)
from pokecontroller.utils import path

if TYPE_CHECKING:
    import numpy


def imwrite(filename: str, img: numpy.ndarray, params: Sequence[int] = None):
    _logger = getLogger(__name__)
    _logger.addHandler(NullHandler())
    _logger.setLevel(DEBUG)
    _logger.propagate = True

    try:
        return lib_image.write(img, filename, params)
    except Exception as e:
        print(e)
        _logger.error(f"Image Write Error: {e}")
        return False


CAPTURE_DIR = path.join("Captures")


def _get_save_filespec(filename: str) -> str:
    """
    画像ファイルの保存パスを取得する。

    入力が絶対パスの場合は、`CAPTURE_DIR`につなげずに返す。

    Args:
        filename (str): 保存名／保存パス

    Returns:
        str: _description_
    """
    if path.is_absolute(filename):
        return filename
    else:
        return path.to_absolute(path.join(CAPTURE_DIR, filename))


class Camera:
    def __init__(self, fps: int = 45):
        self.camera = lib_camera.Camera(fps=fps, frame_size=(1280, 720))
        self.image_bgr = None
        # self.capture_size = (1920, 1080)
        self.capture_dir = "Captures"

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

    @property
    def fps(self):
        return self.camera.fps

    @fps.setter
    def fps(self, fps: int):
        self.camera.fps = fps

    @property
    def capture_size(self):
        return self.camera.frame_size

    @capture_size.setter
    def capture_size(self, size: tuple[int, int]):
        self.camera.frame_size = size

    def openCamera(self, cameraId: int):
        if not self.camera.is_opened:
            self._logger.debug("Camera is already opened")
        if os.name == "nt":
            self._logger.debug("NT OS")
        else:
            self._logger.debug("Not NT OS")

        self.camera.open(camera_id=cameraId)

        if not self.isOpened():
            print("Camera ID " + str(cameraId) + " can't open.")
            self._logger.error(f"Camera ID {cameraId} cannot open.")
            return
        print("Camera ID " + str(cameraId) + " opened successfully")
        self._logger.debug(f"Camera ID {cameraId} opened successfully.")

    def isOpened(self):
        self._logger.debug("Camera is opened")
        return self.camera.is_opened

    def readFrame(self):
        self.camera.read()
        self.image_bgr = self.camera.frame
        return self.image_bgr

    def saveCapture(self, filename: str = None, crop: int = None, crop_ax: List[int] = None, img: numpy.ndarray = None):
        if crop_ax is None:
            crop_ax = [0, 0, self.capture_size[0], self.capture_size[1]]
        else:
            pass
            # print(crop_ax)

        dt_now = datetime.datetime.now()
        if filename is None or filename == "":
            filename = dt_now.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        else:
            filename = filename + ".png"

        crop_fmt = int(crop) if crop is not None else None
        if crop_fmt is None:
            image = self.image_bgr
        elif crop_fmt == 1:
            args = lib_image.ImageCropArgs(
                x=crop_ax[0],
                y=crop_ax[1],
                width=crop_ax[2] - crop_ax[0],
                height=crop_ax[3] - crop_ax[1],
            )
            image = lib_image.crop(self.image_bgr, args)
        elif crop_fmt == 2:
            args = lib_image.ImageCropArgs(
                x=crop_ax[0],
                y=crop_ax[1],
                width=crop_ax[2],
                height=crop_ax[3],
            )
            image = lib_image.crop(self.image_bgr, args)
        elif img is not None:
            image = img
        else:
            image = self.image_bgr

        save_path = _get_save_filespec(filename)

        if not os.path.exists(os.path.dirname(save_path)) or not os.path.isdir(os.path.dirname(save_path)):
            # 保存先ディレクトリが存在しないか、同名のファイルが存在する場合（existsはファイルとフォルダを区別しない）
            os.makedirs(os.path.dirname(save_path))
            self._logger.debug("Created Capture folder")

        try:
            lib_image.write(image, save_path)
            self._logger.debug(f"Capture succeeded: {save_path}")
            print("capture succeeded: " + save_path)
        except Exception as e:
            print("Capture Failed")
            self._logger.error(f"Capture Failed :{e}")

    def destroy(self):
        self.camera.close()
        self._logger.debug("Camera destroyed")
