import logging
from contextlib import contextmanager
from typing import Sequence, Generator
from pokecontroller.core import (
    image as imagelib,
    camera as cameralib,
    path as pathlib,
    datetime as datetimelib,
)
from pokecontroller.core.image import utils as imagelib_utils

logger = logging.getLogger(__name__)


def imwrite(
    filename: str,
    img: imagelib.RawImage,
    params: Sequence[int] = None) -> bool:
    """
    画像を書き込む
    """
    try:
        return imagelib.write(img, filename, params)
    except Exception as e:
        logger.error(f"Image Write Error: {e}")
        return False


CAPTURE_DIR = "Captures"


def _get_save_filespec(filename: str) -> str:
    """
    画像ファイルの保存パスを取得する。

    入力が絶対パスの場合は、`CAPTURE_DIR`につなげずに返す。

    Args:
        filename (str): 保存名／保存パス

    Returns:
        str: _description_
    """
    if pathlib.is_absolute(filename):
        return filename
    else:
        return pathlib.to_absolute(pathlib.join(CAPTURE_DIR, filename))


class Camera:
    def __init__(self, fps: int = 45):
        self.camera = cameralib.Camera(fps=fps, frame_size=(1280, 720))
        self.image_bgr = None
        # self.capture_size = (1920, 1080)
        self.capture_dir = "Captures"

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

    def openCamera(self, cameraId: int):  # noqa
        self.camera.open(camera_id=cameraId)

    def isOpened(self):  # noqa
        return self.camera.is_opened

    def readFrame(self) -> imagelib.RawImage | None:  # noqa
        _, self.image_bgr = self.camera.read()
        return self.image_bgr

    def saveCapture(  # noqa
        self,
        filename: str = None,
        crop: int = None,
        crop_ax: list[int] = None,
        img: imagelib.RawImage = None,
    ):
        if crop_ax is None:
            c = [0, 0, self.capture_size[0], self.capture_size[1]]
        else:
            c = crop_ax

        crop_fmt = int(crop) if crop is not None else None
        if crop_fmt is None:
            image = self.image_bgr
        elif crop_fmt:
            imagelib_utils.convert_to_default(c, crop_fmt)
            args = imagelib.ImageCropArgs(
                ys=c[0],
                ye=c[1],
                xs=c[2],
                xe=c[3],
            )
            image = imagelib.crop(self.image_bgr, args)
        elif img is not None:
            image = img
        else:
            image = self.image_bgr

        if not filename:
            fn = f"{datetimelib.format_datetime()}.png"
        else:
            fn = filename + ".png"
        save_path = _get_save_filespec(fn)

        if not pathlib.exists_directory((save_dir := pathlib.directory_name(save_path))):
            # 保存先ディレクトリが存在しないか、同名のファイルが存在する場合（existsはファイルとフォルダを区別しない）
            pathlib.make_directory(save_dir)
            logger.debug("Created Capture folder")

        try:
            imwrite(save_path, image)
            logger.debug(f"Capture succeeded: {save_path}")
        except Exception as e:
            logger.error(f"Capture Failed :{e}")

    def destroy(self):
        self.camera.close()


@contextmanager
def use_camera(
    fps: int = 45,
) -> Generator[Camera, None, None]:
    camera = Camera(fps=fps)
    try:
        yield camera
    finally:
        camera.destroy()
