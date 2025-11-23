import os
from dataclasses import dataclass
from enum import Enum
from typing import Sequence

import cv2

from .raw_image import RawImage


class ImageReadMode(Enum):
    GRAYSCALE = "grayscale"
    COLOR = "color"


@dataclass
class ImageCropArgs:
    x: int
    y: int
    width: int
    height: int


@dataclass
class ImageBinarizeHsvArgs:
    lower: RawImage
    upper: RawImage


@dataclass
class TemplateMatchResult:
    contains: bool
    location: tuple[int, int]
    width: int
    height: int
    value: float


def crop(src: RawImage, args: ImageCropArgs) -> RawImage:
    return src[args.y:(args.y + args.height), args.x:(args.x + args.width)]


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


def write(src: RawImage, path: str, params: Sequence[int] = None) -> bool:
    ext = os.path.splitext(path)[1]
    success, encoded = cv2.imencode(ext, src, params)

    if not success:
        return False

    with open(path, mode="w+b") as f:
        encoded.tofile(f)
    return True


def read(path: str, mode: ImageReadMode = ImageReadMode.COLOR) -> RawImage | None:
    if not path:
        return None

    match (mode):
        case ImageReadMode.GRAYSCALE:
            return cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        case ImageReadMode.COLOR:
            return cv2.imread(path, cv2.IMREAD_COLOR)
        case _:
            return None


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
    matcher,
    image: cv2.cuda.GpuMat,
    template: cv2.cuda.GpuMat,
) -> cv2.cuda.GpuMat:
    result = matcher.match(image, template)
    return result.download()
