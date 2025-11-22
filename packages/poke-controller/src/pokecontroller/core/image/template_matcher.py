from abc import ABC, abstractmethod

import cv2

from .image_processing import (
    TemplateMatchResult,
    match_template,
    match_template_by_gpu,
)
from .raw_image import (
    RawImage,
)


class TemplateMatcher(ABC):
    def __init__(self, threshold: float = 0.8):
        self._image: RawImage | None = None
        self._template: RawImage | None = None
        self._mask: RawImage | None = None
        self._threshold: float = threshold
        self._last_result: TemplateMatchResult | None = None

    @property
    @abstractmethod
    def mode(self) -> str:
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
    def image(self) -> RawImage | None:
        return self._image

    @property
    def template(self) -> RawImage | None:
        return self._template

    @property
    def mask(self) -> RawImage | None:
        return self._mask

    @property
    def threshold(self) -> float:
        return self._threshold

    @property
    def last_result(self) -> TemplateMatchResult | None:
        return self._last_result

    def set_image(self, image: RawImage | None) -> "TemplateMatcher":
        self._image = image
        return self

    def clear_image(self):
        return self.set_image(None)

    def set_template(self, template: RawImage | None) -> "TemplateMatcher":
        self._template = template
        return self

    def clear_template(self):
        return self.set_template(None)

    def set_mask(self, mask: RawImage | None) -> "TemplateMatcher":
        self._mask = mask
        return self

    def clear_mask(self) -> "TemplateMatcher":
        return self.set_mask(None)

    def set_threshold(self, threshold: float) -> "TemplateMatcher":
        self._threshold = threshold
        return self

    def _match_result(self, matched: RawImage) -> TemplateMatchResult:
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
    def mode(self) -> str:
        return "cpu"

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

        result = match_template(self._image, self._template, self._mask)
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
    def mode(self) -> str:
        return "gpu"

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def mask(self) -> RawImage | None:
        return None

    @property
    def is_ready(self) -> bool:
        return self._initialized and self._gpu_image is not None and self._gpu_template is not None

    def initialize(self) -> None:
        if self._initialized:
            return

        try:
            self._gpu_matcher = cv2.cuda.createTemplateMatching(cv2.CV_8UC1, cv2.TM_CCOEFF_NORMED)
            self._gpu_image = cv2.cuda.GpuMat()
            self._gpu_template = cv2.cuda.GpuMat()
            self._initialized = True
        except Exception:
            self._gpu_matcher = None
            self._gpu_image = None
            self._gpu_template = None
            self._initialized = False

    def set_image(self, image: RawImage) -> "GpuTemplateMatcher":
        if self._initialized:
            super().set_image(image)
            self._gpu_image.upload(image)
        return self

    def set_template(self, template: RawImage) -> "GpuTemplateMatcher":
        if self._initialized:
            super().set_template(template)
            self._gpu_template.upload(template)
        return self

    def set_mask(self, mask: RawImage | None) -> "GpuTemplateMatcher":
        return self

    def match(self) -> TemplateMatchResult | None:
        if not self.is_ready:
            return None

        result = match_template_by_gpu(self._gpu_matcher, self._gpu_image, self._gpu_template)
        return self._match_result(result)


class TemplateMatcherGenerator:
    @staticmethod
    def generate(preferred_mode: str = "cpu") -> TemplateMatcher:
        match (preferred_mode):
            case "gpu":
                try:
                    matcher = GpuTemplateMatcher()
                    return matcher if matcher.initialized else CpuTemplateMatcher()
                except Exception:
                    return CpuTemplateMatcher()
            case _:  # default to cpu
                return CpuTemplateMatcher()
