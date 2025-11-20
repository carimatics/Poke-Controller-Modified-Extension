from .image_processing import (
    ImageBinarizeHsvArgs,
    ImageCropArgs,
    ImageReadMode,
    binarize_by_hsv,
    binarize_by_interframe_diff,
    binarize_by_threshold,
    crop,
    grayscale,
    read,
    write,
)
from .raw_image import RawImage


class Image:
    def __init__(self, src: RawImage):
        self.src = src

    @property
    def src(self) -> RawImage:
        return self._src

    @src.setter
    def src(self, value: RawImage) -> None:
        self._src: RawImage = value
        self._width: int = self._src.shape[1]
        self._height: int = self._src.shape[0]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def crop(self, args: ImageCropArgs) -> "Image":
        return Image(crop(self._src, args))

    def grayscale(self) -> "Image":
        return Image(grayscale(self._src))

    def binarize_by_hsv(self, args: ImageBinarizeHsvArgs) -> "Image":
        return Image(binarize_by_hsv(self._src, args))

    def binarize_by_threshold(self, threshold: float) -> "Image":
        return Image(binarize_by_threshold(self._src, threshold))

    def binarize_by_interframe_diff(self, frame2: "Image", frame3: "Image", threshold: float) -> "Image":
        return Image(binarize_by_interframe_diff(self._src, frame2.src, frame3.src, threshold))

    def write(self, path: str) -> bool:
        return write(self._src, path)

    @staticmethod
    def read(
        path: str,
        mode: ImageReadMode = ImageReadMode.COLOR
    ) -> "Image | None":
        if (result := read(path, mode)) is None:
            return None
        return Image(result)
