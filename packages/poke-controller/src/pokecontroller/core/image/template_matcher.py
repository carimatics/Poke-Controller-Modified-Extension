from abc import ABC, abstractmethod
from typing import Literal

import cv2

from .image_processing import (
    GpuTemplateMatchable,
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
    def mode(self) -> str: ...

    @property
    @abstractmethod
    def is_initialized(self) -> bool: ...

    @property
    @abstractmethod
    def is_ready(self) -> bool: ...

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

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def match(self) -> TemplateMatchResult | None: ...

    @abstractmethod
    def set_image(self, image: RawImage | None) -> "TemplateMatcher": ...

    @abstractmethod
    def set_template(self, template: RawImage | None) -> "TemplateMatcher": ...

    @abstractmethod
    def set_mask(self, mask: RawImage | None) -> "TemplateMatcher": ...

    def set_threshold(self, threshold: float) -> "TemplateMatcher":
        self._threshold = threshold
        return self

    def _result_from(self, result: RawImage) -> TemplateMatchResult:
        _, value_max, _, location_max = cv2.minMaxLoc(result)

        if (tmpl := self._template) is None:
            # FIXME: define better exception
            raise ValueError("Template is not set")

        h, w = tmpl.shape
        self._last_result = TemplateMatchResult(
            contains=value_max > self._threshold,
            location_max=(location_max[0], location_max[1]),
            width=w,
            height=h,
            value_max=value_max,
        )
        return self._last_result


class CpuTemplateMatcher(TemplateMatcher):
    @property
    def mode(self) -> str:
        return "cpu"

    @property
    def is_initialized(self) -> bool:
        return True

    @property
    def is_ready(self) -> bool:
        ready, *_ = self._ready_state()
        return ready

    def set_image(self, image: RawImage | None) -> TemplateMatcher:
        self._image = image
        return self

    def set_template(self, template: RawImage | None) -> TemplateMatcher:
        self._template = template
        return self

    def set_mask(self, mask: RawImage | None) -> TemplateMatcher:
        self._mask = mask
        return self

    def initialize(self) -> None:
        pass

    def match(self) -> TemplateMatchResult | None:
        ready, *state = self._ready_state()
        if not ready:
            return None

        result = match_template(*state)
        return self._result_from(result)

    def _ready_state(
        self,
    ) -> (
        tuple[Literal[True], RawImage, RawImage, RawImage | None]
        | tuple[Literal[False], None, None, None]
    ):
        if (img := self._image) is None or (tmpl := self._template) is None:
            return False, None, None, None
        return True, img, tmpl, self._mask


class GpuTemplateMatcher(TemplateMatcher):
    def __init__(self, threshold: float = 0.8) -> None:
        super().__init__(threshold)

        self._initialized: bool = False
        self._gpu_matcher: GpuTemplateMatchable | None = None
        self._gpu_image: cv2.cuda.GpuMat | None = None
        self._gpu_template: cv2.cuda.GpuMat | None = None
        self.initialize()

    @property
    def mode(self) -> str:
        return "gpu"

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def mask(self) -> None:
        return None

    @property
    def is_ready(self) -> bool:
        ready, *_ = self._ready_state()
        return ready

    def initialize(self) -> None:
        if self._initialized:
            return

        self._gpu_matcher = cv2.cuda.createTemplateMatching(  # type: ignore[attr-defined]
            cv2.CV_8UC1,
            cv2.TM_CCOEFF_NORMED,
        )
        self._gpu_image = cv2.cuda.GpuMat()
        self._gpu_template = cv2.cuda.GpuMat()
        self._initialized = True

    def set_image(self, image: RawImage | None) -> TemplateMatcher:
        self._image = image
        self._upload_image(self._gpu_image, image)
        return self

    def set_template(self, template: RawImage | None) -> TemplateMatcher:
        self._template = template
        self._upload_image(self._gpu_template, template)
        return self

    def set_mask(self, mask: RawImage | None) -> TemplateMatcher:
        return self

    def match(self) -> TemplateMatchResult | None:
        ready, *state = self._ready_state()
        if not ready:
            return None

        result = match_template_by_gpu(*state)
        return self._result_from(result)

    def _ready_state(
        self,
    ) -> (
        (tuple[Literal[True], GpuTemplateMatchable, cv2.cuda.GpuMat, cv2.cuda.GpuMat])
        | (tuple[Literal[False], None, None, None])
    ):
        if not self._initialized:
            return False, None, None, None
        if self._image is None or self._template is None:
            return False, None, None, None
        if (matcher := self._gpu_matcher) is None:
            return False, None, None, None
        if (img := self._gpu_image) is None or img.empty():
            return False, None, None, None
        if (tmpl := self._gpu_template) is None or tmpl.empty():
            return False, None, None, None
        return True, matcher, img, tmpl

    def _upload_image(self, var: cv2.cuda.GpuMat | None, val: RawImage | None) -> None:
        if not self._initialized:
            return

        if var is None or val is None:
            return

        var.upload(val)


class TemplateMatcherCreator:
    @staticmethod
    def create(
        preferred_mode: Literal["cpu", "gpu"] = "cpu",
    ) -> TemplateMatcher:
        if preferred_mode == "gpu":
            try:
                gpu = GpuTemplateMatcher()
                if gpu.is_initialized:
                    return gpu
            except Exception:  # noqa
                pass
        cpu = CpuTemplateMatcher()
        return cpu
