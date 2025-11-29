import io
import os
from dataclasses import dataclass
from typing import Literal, Protocol, Sequence

import cv2
from PIL import Image

from .raw_image import RawImage

ImageReadMode = Literal["grayscale", "color"]


@dataclass(kw_only=True, frozen=True)
class ImageCropArgs:
    xs: int
    xe: int
    ys: int
    ye: int


@dataclass(kw_only=True, frozen=True)
class ImageBinarizeHsvArgs:
    lower: RawImage
    upper: RawImage


@dataclass(kw_only=True, frozen=True)
class TemplateMatchResult:
    contains: bool
    location_max: tuple[int, int]
    width: int
    height: int
    value_max: float


class RawImageDownloadable(Protocol):
    def download(self) -> RawImage: ...


class GpuTemplateMatchable(Protocol):
    def match(
        self,
        image: cv2.cuda.GpuMat,
        template: cv2.cuda.GpuMat,
    ) -> RawImageDownloadable: ...


def crop(src: RawImage, args: ImageCropArgs) -> RawImage:
    return src[args.ys: args.ye, args.xs: args.xs]


def grayscale(src: RawImage) -> RawImage:
    return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


def binarize_by_hsv(src: RawImage, args: ImageBinarizeHsvArgs) -> RawImage:
    return cv2.inRange(src, args.lower, args.upper)


def binarize_by_threshold(src: RawImage, threshold: float) -> RawImage:
    return cv2.threshold(src, threshold, 255, cv2.THRESH_BINARY)[1]


def binarize_by_interframe_diff(
    src1: RawImage,
    src2: RawImage,
    src3: RawImage,
    threshold: float,
) -> RawImage:
    diff1 = cv2.absdiff(src1, src2)
    diff2 = cv2.absdiff(src2, src3)
    diff = cv2.bitwise_and(diff1, diff2)
    th = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
    return cv2.medianBlur(th, 3)


def write(src: RawImage, path: str, *params: Sequence[int]) -> bool:
    ext = os.path.splitext(path)[1]
    success, encoded = cv2.imencode(ext, src, *params)

    if not success:
        return False

    with open(path, mode="w+b") as f:
        encoded.tofile(f)
    return True


def read(path: str, mode: ImageReadMode = "color") -> RawImage | None:
    if not path:
        return None

    match mode:
        case "grayscale":
            return cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        case "color":
            return cv2.imread(path, cv2.IMREAD_COLOR)


def to_bytes(src: RawImage, fmt: str | None = "png") -> bytes:
    rgb = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(rgb)
    bio = io.BytesIO()
    image.save(bio, format=fmt)
    return bio.getvalue()


def match_template(
    image: RawImage,
    template: RawImage,
    mask: RawImage | None = None,
) -> RawImage:
    if mask is None:
        method = cv2.TM_CCOEFF_NORMED
    else:
        method = cv2.TM_CCORR_NORMED
    return cv2.matchTemplate(image, template, method, mask=mask)


def match_template_by_gpu(
    matcher: GpuTemplateMatchable,
    image: cv2.cuda.GpuMat,
    template: cv2.cuda.GpuMat,
) -> RawImage:
    result = matcher.match(image, template)
    return result.download()
