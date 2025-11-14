import os
from dataclasses import dataclass
from enum import Enum

import cv2


class ImageReadMode(Enum):
    BINARY = "binary"
    GRAY = "gray"
    COLOR = "color"


@dataclass
class ImageCropArgs:
    x: int
    y: int
    width: int
    height: int


@dataclass
class ImageBinarizeHsvArgs:
    lower: tuple[int, int, int]
    upper: tuple[int, int, int]


@dataclass
class TemplateMatchResult:
    contains: bool
    location: tuple[int, int]
    width: int
    height: int
    value: float


class Image:
    def __init__(self, raw_value: cv2.typing.MatLike):
        self.raw_value = raw_value
        self.width = self.raw_value.shape[1]
        self.height = self.raw_value.shape[0]

        self._gpu_initialized = False
        self._gpu_src = None
        self._gpu_template = None
        self._gpu_result = None

    def crop(self, args: ImageCropArgs) -> "Image":
        return Image(raw_value=self.raw_value[args.y:(args.y + args.height), args.x:(args.x + args.width)])

    def to_grayscale(self) -> "Image":
        return Image(raw_value=cv2.cvtColor(self.raw_value, cv2.COLOR_BGR2GRAY))

    def binarize_by_hsv(self, args: ImageBinarizeHsvArgs) -> "Image":
        return Image(raw_value=cv2.inRange(self.raw_value, args.lower, args.upper))

    def binarize_by_threshold(self, threshold: float) -> "Image":
        return Image(raw_value=cv2.threshold(self.raw_value, threshold, 255, cv2.THRESH_BINARY))

    def diff_interframe(self, next1: "Image", next2: "Image", threshold: float) -> "Image":
        diff1 = cv2.absdiff(self.raw_value, next1.raw_value)
        diff2 = cv2.absdiff(next1.raw_value, next2.raw_value)
        diff = cv2.bitwise_and(diff1, diff2)
        threshold = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
        return Image(cv2.medianBlur(threshold, 3))

    def match_template(self, template: "Image", threshold: float, mask: "Image" = None) -> TemplateMatchResult:
        mask_value = mask.raw_value if isinstance(mask, Image) else None
        method = cv2.TM_CCOEFF_NORMED if mask_value is None else cv2.TM_CCORR_NORMED
        result = cv2.matchTemplate(self.raw_value, template.raw_value, method, mask=mask_value)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        return TemplateMatchResult(
            contains=max_val > threshold,
            location=(max_loc[0], max_loc[1]),
            width=template.width,
            height=template.height,
            value=max_val,
        )

    def match_template_by_gpu(self, template: "Image", threshold: float) -> TemplateMatchResult | None:
        if not self._initialize_gpu():
            return None

        method = cv2.TM_CCOEFF_NORMED
        self._gpu_src.upload(self.raw_value)
        self._gpu_template.upload(template.raw_value)
        matcher = cv2.cuda.createTemplatematching(cv2.CV_8UC1, method)
        self._gpu_result = matcher.match(self._gpu_src, self._gpu_template)
        result = self._gpu_result.download()
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        return TemplateMatchResult(
            contains=max_val > threshold,
            location=(max_loc[0], max_loc[1]),
            width=template.width,
            height=template.height,
            value=max_val,
        )

    def write_to(self, path: str) -> bool:
        ext = os.path.splitext(path)[1]
        success, encoded = cv2.imencode(ext, self.raw_value)

        if not success:
            return False

        with open(path, mode="w+b") as f:
            encoded.tofile(f)
        return True

    def _initialize_gpu(self) -> bool:
        if self._gpu_initialized:
            return True

        try:
            self._gpu_src = cv2.cuda_GpuMat()
            self._gpu_template = cv2.cuda_GpuMat()
            self._gpu_result = cv2.cuda_GpuMat()
            self._gpu_initialized = True
            return True
        except Exception:
            self._gpu_initialized = False
            return False

    @staticmethod
    def read_from(path: str, mode: ImageReadMode = ImageReadMode.COLOR) -> "Image":
        if not path:
            return None

        if mode == ImageReadMode.BINARY:
            raw_value = cv2.imread(path, 0)
        elif mode == ImageReadMode.GRAY:
            raw_value = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        else:
            raw_value = cv2.imread(path, cv2.IMREAD_COLOR)

        return Image(raw_value)
