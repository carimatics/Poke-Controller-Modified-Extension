import tkinter as tk
from dataclasses import dataclass


@dataclass(kw_only=True)
class OutputsWidgetCatalog:
    textarea1: tk.Text | None = None
    textarea2: tk.Text | None = None


@dataclass(kw_only=True)
class CaptureWidgetCatalog:
    canvas: tk.Canvas | None = None


@dataclass(kw_only=True)
class AppWidgetCatalog:
    outputs: OutputsWidgetCatalog
    capture: CaptureWidgetCatalog


_app_widget_catalog = AppWidgetCatalog(
    outputs=OutputsWidgetCatalog(),
    capture=CaptureWidgetCatalog(),
)


def get_app_widget_catalog() -> AppWidgetCatalog:
    global _app_widget_catalog
    return _app_widget_catalog
