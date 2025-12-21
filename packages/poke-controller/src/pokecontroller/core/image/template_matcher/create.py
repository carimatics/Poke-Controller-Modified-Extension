from typing import Literal

from pokecontroller.core.image.template_matcher.cpu import CpuTemplateMatcher
from pokecontroller.core.image.template_matcher.gpu import GpuTemplateMatcher
from pokecontroller.core.image.template_matcher.template_matcher import TemplateMatcher

TemplateMatcherPreferredMode = Literal["cpu", "gpu"]


def create_template_matcher(
    preferred_mode: TemplateMatcherPreferredMode = "cpu",
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
