from abc import ABC, abstractmethod
from typing import Self

import cv2

from ..image_processing import TemplateMatchResult
from ..raw_image import RawImage


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
    def set_image(self, image: RawImage | None) -> Self: ...

    @abstractmethod
    def set_template(self, template: RawImage | None) -> Self: ...

    @abstractmethod
    def set_mask(self, mask: RawImage | None) -> Self: ...

    def set_threshold(self, threshold: float) -> Self:
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
