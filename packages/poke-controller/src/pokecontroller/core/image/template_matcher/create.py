from typing import Literal

from .template_matcher import TemplateMatcher
from .cpu import CpuTemplateMatcher
from .gpu import GpuTemplateMatcher

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
