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


class TemplateMatcher[I](ABC):
    def __init__(self, threshold: float = 0.8):
        self._image: I | None = None
        self._template: I | None = None
        self._mask: I | None = None
        self._threshold: float = threshold
        self._last_result: TemplateMatchResult | None = None

    @property
    @abstractmethod
    def mode(self) -> str: ...

    @property
    @abstractmethod
    def initialized(self) -> bool: ...

    @property
    @abstractmethod
    def is_ready(self) -> bool: ...

    @property
    def image(self) -> I | None:
        return self._image

    @property
    def template(self) -> I | None:
        return self._template

    @property
    def mask(self) -> I | None:
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
    def set_image(self, image: RawImage | None) -> "TemplateMatcher[I]": ...

    @abstractmethod
    def set_template(self, template: RawImage | None) -> "TemplateMatcher[I]": ...

    @abstractmethod
    def set_mask(self, mask: RawImage | None) -> "TemplateMatcher[I]": ...

    def set_threshold(self, threshold: float) -> "TemplateMatcher[I]":
        self._threshold = threshold
        return self

    def _match_result(self, matched: RawImage) -> TemplateMatchResult:
        _, max_val, _, max_loc = cv2.minMaxLoc(matched)

        if (tmpl := self._template) is None:
            # FIXME: define better exception
            raise ValueError("Template is not set")

        if isinstance(tmpl, cv2.cuda.GpuMat):
            w, h = tmpl.size()
        else:
            h, w = tmpl.shape  # type: ignore[attr-defined]
        self._last_result = TemplateMatchResult(
            contains=max_val > self._threshold,
            location=(max_loc[0], max_loc[1]),
            width=w,
            height=h,
            value=max_val,
        )
        return self._last_result


class CpuTemplateMatcher(TemplateMatcher[RawImage]):
    @property
    def mode(self) -> str:
        return "cpu"

    @property
    def initialized(self) -> bool:
        return True

    @property
    def is_ready(self) -> bool:
        return self._image is not None and self._template is not None

    def set_image(self, image: RawImage | None) -> TemplateMatcher[RawImage]:
        self._image = image
        return self

    def set_template(self, template: RawImage | None) -> TemplateMatcher[RawImage]:
        self._template = template
        return self

    def set_mask(self, mask: RawImage | None) -> TemplateMatcher[RawImage]:
        self._mask = mask
        return self

    def initialize(self) -> None:
        pass

    def match(self) -> TemplateMatchResult | None:
        if (img := self._image) is None or (tmpl := self._template) is None:
            return None

        result = match_template(img, tmpl, self._mask)
        return self._match_result(result)


class GpuTemplateMatcher(TemplateMatcher[cv2.cuda.GpuMat]):
    def __init__(self, threshold: float = 0.8):
        super().__init__(threshold)

        self._initialized: bool = False
        self._gpu_matcher = None
        self.initialize()

    @property
    def mode(self) -> str:
        return "gpu"

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def mask(self) -> None:
        return None

    @property
    def is_ready(self) -> bool:
        return (
            self._initialized and self._image is not None and self._template is not None
        )

    def initialize(self) -> None:
        if self._initialized:
            return

        try:
            # noinspection PyUnresolvedReferences
            self._gpu_matcher = cv2.cuda.createTemplateMatching(  # type: ignore[attr-defined]
                cv2.CV_8UC1,
                cv2.TM_CCOEFF_NORMED,
            )
            self._image = cv2.cuda.GpuMat()
            self._template = cv2.cuda.GpuMat()
            self._initialized = True
        except Exception:  # noqa
            self._gpu_matcher = None
            self._image = None
            self._template = None
            self._initialized = False

    def set_image(self, image: RawImage | None) -> TemplateMatcher[cv2.cuda.GpuMat]:
        self._upload_image(self._image, image)
        return self

    def set_template(
        self, template: RawImage | None
    ) -> TemplateMatcher[cv2.cuda.GpuMat]:
        self._upload_image(self._template, template)
        return self

    def set_mask(self, mask: RawImage | None) -> TemplateMatcher[cv2.cuda.GpuMat]:
        return self

    def match(self) -> TemplateMatchResult | None:
        if not self._initialized:
            return None
        if (matcher := self._gpu_matcher) is None:
            return None
        if (img := self._image) is None:  # type: ignore[unreachable]
            return None
        if (tmpl := self._template) is None:
            return None

        result = match_template_by_gpu(matcher, img, tmpl)
        return self._match_result(result)

    def _upload_image(self, var: cv2.cuda.GpuMat | None, val: RawImage | None) -> None:
        if not self._initialized:
            return

        if var is not None and val is not None:
            var.upload(val)


class TemplateMatcherCreator:
    @staticmethod
    def create(
        preferred_mode: str = "cpu",
    ) -> tuple[CpuTemplateMatcher, None] | tuple[None, GpuTemplateMatcher]:
        if preferred_mode == "gpu":
            try:
                gpu = GpuTemplateMatcher()
                if gpu.initialized:
                    return None, gpu
            except Exception:  # noqa
                pass
        cpu = CpuTemplateMatcher()
        return cpu, None
