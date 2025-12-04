from typing import Literal

from ..image_processing import match_template
from ..raw_image import RawImage
from .template_matcher import TemplateMatchResult, TemplateMatcher


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
