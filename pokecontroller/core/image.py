import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

import cv2
import cv2.cuda


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
    lower: cv2.typing.MatLike
    upper: cv2.typing.MatLike


@dataclass
class TemplateMatchResult:
    contains: bool
    location: tuple[int, int]
    width: int
    height: int
    value: float


def parse_crop(fmt: int, crop: list[int]) -> ImageCropArgs:
    if fmt < 10:  # pillow format
        if fmt == 1:  # [x軸始点, y軸始点, x軸終点, y軸終点]
            x, y, w, h = (crop[0], crop[1], crop[2] - crop[0], crop[3] - crop[1])
        elif fmt == 2:  # [x軸始点, y軸始点, トリミング後の画像のサイズ(横), トリミング後の画像のサイズ(縦)]
            x, y, w, h = (crop[0], crop[1], crop[2], crop[3])
        elif fmt == 3:  # [x軸始点, x軸終点, y軸始点, y軸終点]
            x, y, w, h = (crop[0], crop[2], crop[1] - crop[0], crop[3] - crop[2])
        else:  # [x軸始点, トリミング後の画像のサイズ(横), y軸始点, トリミング後の画像のサイズ(縦)]
            x, y, w, h = (crop[0], crop[2], crop[1], crop[3])

    else:  # opencv format
        if fmt == 11:  # [y軸始点, x軸始点, y軸終点, x軸終点]
            x, y, w, h = (crop[1], crop[0], crop[3] - crop[1], crop[2] - crop[0])
        elif fmt == 12:  # [y軸始点, x軸始点, トリミング後の画像のサイズ(縦), トリミング後の画像のサイズ(横)]
            x, y, w, h = (crop[1], crop[0], crop[3], crop[2])
        elif fmt == 13:  # [y軸始点, y軸終点, x軸始点, x軸終点]
            x, y, w, h = (crop[2], crop[0], crop[3] - crop[2], crop[1] - crop[0])
        else:  # [y軸始点, トリミング後の画像のサイズ(縦), x軸始点, トリミング後の画像のサイズ(横)]
            x, y, w, h = (crop[2], crop[0], crop[3], crop[1])

    return ImageCropArgs(x=x, y=y, width=w, height=h)


class Image:
    def __init__(self, raw_value: cv2.typing.MatLike):
        self.raw_value = raw_value
        self.width = self.raw_value.shape[1]
        self.height = self.raw_value.shape[0]

    def crop(self, args: ImageCropArgs) -> "Image":
        return Image(raw_value=self.raw_value[args.y:(args.y + args.height), args.x:(args.x + args.width)])

    def to_grayscale(self) -> "Image":
        return Image(raw_value=cv2.cvtColor(self.raw_value, cv2.COLOR_BGR2GRAY))

    def binarize_by_hsv(self, args: ImageBinarizeHsvArgs) -> "Image":
        return Image(raw_value=cv2.inRange(self.raw_value, args.lower, args.upper))

    def binarize_by_threshold(self, threshold: float) -> "Image":
        _, value = cv2.threshold(self.raw_value, threshold, 255, cv2.THRESH_BINARY)
        return Image(raw_value=value)

    def binarize_by_interframe_diff(self, next1: "Image", next2: "Image", threshold: float) -> "Image":
        diff1 = cv2.absdiff(self.raw_value, next1.raw_value)
        diff2 = cv2.absdiff(next1.raw_value, next2.raw_value)
        diff = cv2.bitwise_and(diff1, diff2)
        th = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
        return Image(cv2.medianBlur(th, 3))

    def write_to(self, path: str) -> bool:
        ext = os.path.splitext(path)[1]
        success, encoded = cv2.imencode(ext, self.raw_value)

        if not success:
            return False

        with open(path, mode="w+b") as f:
            encoded.tofile(f)
        return True

    @staticmethod
    def read_from(path: str, mode: ImageReadMode = ImageReadMode.COLOR) -> "Image | None":
        if not path:
            return None

        if mode == ImageReadMode.BINARY:
            raw_value = cv2.imread(path, 0)
        elif mode == ImageReadMode.GRAY:
            raw_value = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        else:
            raw_value = cv2.imread(path, cv2.IMREAD_COLOR)

        return Image(raw_value)


class TemplateMatcherMode(Enum):
    CPU = "cpu"
    GPU = "gpu"


class TemplateMatcher(ABC):
    def __init__(self, threshold: float = 0.8):
        self._image: Image | None = None
        self._template: Image | None = None
        self._mask: Image | None = None
        self._threshold: float = threshold
        self._last_result: TemplateMatchResult | None = None

    @property
    @abstractmethod
    def mode(self) -> TemplateMatcherMode:
        pass

    @property
    @abstractmethod
    def initialized(self) -> bool:
        return False

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        return False

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def match(self) -> TemplateMatchResult | None:
        pass

    @property
    def image(self) -> Image | None:
        return self._image

    @property
    def template(self) -> Image | None:
        return self._template

    @property
    def mask(self) -> Image | None:
        return self._mask

    @property
    def threshold(self) -> float:
        return self._threshold

    @property
    def last_result(self) -> TemplateMatchResult | None:
        return self._last_result

    def set_image(self, image: Image) -> "TemplateMatcher":
        self._image = image
        return self

    def set_template(self, template: Image) -> "TemplateMatcher":
        self._template = template
        return self

    def set_mask(self, mask: Image | None) -> "TemplateMatcher":
        self._mask = mask
        return self

    def clear_mask(self) -> "TemplateMatcher":
        return self.set_mask(None)

    def set_threshold(self, threshold: float) -> "TemplateMatcher":
        self._threshold = threshold
        return self

    def _match_result(self, matched: cv2.typing.MatLike) -> TemplateMatchResult:
        _, max_val, _, max_loc = cv2.minMaxLoc(matched)
        self._last_result = TemplateMatchResult(
            contains=max_val > self._threshold,
            location=(max_loc[0], max_loc[1]),
            width=self._template.width,
            height=self._template.height,
            value=max_val,
        )
        return self._last_result


class CpuTemplateMatcher(TemplateMatcher):
    def __init__(self, threshold: float = 0.8):
        super().__init__(threshold)

    @property
    def mode(self) -> TemplateMatcherMode:
        return TemplateMatcherMode.CPU

    @property
    def initialized(self) -> bool:
        return True

    @property
    def is_ready(self) -> bool:
        return self._image is not None and self._template is not None

    def initialize(self) -> None:
        pass

    def match(self) -> TemplateMatchResult | None:
        if not self.is_ready:
            return None

        mask_value = self._mask.raw_value
        method = cv2.TM_CCOEFF_NORMED if mask_value is None else cv2.TM_CCORR_NORMED
        result = cv2.matchTemplate(self._image.raw_value, self._template.raw_value, method, mask=mask_value)
        return self._match_result(result)


class GpuTemplateMatcher(TemplateMatcher):
    def __init__(self, threshold: float = 0.8):
        super().__init__(threshold)

        self._initialized: bool = False
        self._gpu_matcher = None
        self._gpu_image: cv2.cuda.GpuMat | None = None
        self._gpu_template: cv2.cuda.GpuMat | None = None
        self._gpu_result: cv2.cuda.GpuMat | None = None
        self.initialize()

    @property
    def mode(self) -> TemplateMatcherMode:
        return TemplateMatcherMode.GPU

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def mask(self) -> Image | None:
        return None

    @property
    def is_ready(self) -> bool:
        return self._initialized and self._image is not None and self._template is not None

    def initialize(self) -> None:
        if self._initialized:
            return

        try:
            self._gpu_matcher = cv2.cuda.createTemplateMatching(cv2.CV_8UC1, cv2.TM_CCOEFF_NORMED)
            self._gpu_image = cv2.cuda.GpuMat()
            self._gpu_template = cv2.cuda.GpuMat()
            self._gpu_result = cv2.cuda.GpuMat()
            self._initialized = True
        except:
            self._initialized = False

    def set_image(self, image: Image) -> "GpuTemplateMatcher":
        if self._initialized:
            super().set_image(image)
            self._gpu_image.upload(image.raw_value)
        return self

    def set_template(self, template: Image) -> "GpuTemplateMatcher":
        if self._initialized:
            super().set_template(template)
            self._gpu_template.upload(template.raw_value)
        return self

    def set_mask(self, mask: Image | None) -> "GpuTemplateMatcher":
        return self

    def match(self) -> TemplateMatchResult | None:
        if not self.is_ready:
            return None

        self._gpu_result = self._gpu_matcher.match(self._gpu_image, self._gpu_template)
        result = self._gpu_result.download()
        return self._match_result(result)


class TemplateMatcherGenerator:
    @staticmethod
    def generate(preferred_mode: TemplateMatcherMode = TemplateMatcherMode.CPU) -> TemplateMatcher:
        if preferred_mode == TemplateMatcherMode.CPU:
            return CpuTemplateMatcher()
        elif preferred_mode == TemplateMatcherMode.GPU:
            try:
                matcher = GpuTemplateMatcher()
                return matcher if matcher.initialized else CpuTemplateMatcher()
            except:
                return CpuTemplateMatcher()
        else:
            raise ValueError(f"Invalid mode: {preferred_mode}")
