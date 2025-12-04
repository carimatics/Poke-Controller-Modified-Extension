from typing import Literal

import cv2

from ..raw_image import RawImage
from ..image_processing import GpuTemplateMatchable, match_template_by_gpu
from .template_matcher import TemplateMatchResult, TemplateMatcher


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
