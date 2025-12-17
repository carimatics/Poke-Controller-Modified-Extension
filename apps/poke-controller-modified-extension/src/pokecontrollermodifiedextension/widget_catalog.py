import tkinter as tk
from dataclasses import dataclass


@dataclass(kw_only=True)
class OutputsWidgetCatalog:
    textarea1: tk.Text | None = None
    textarea2: tk.Text | None = None


@dataclass(kw_only=True)
class WidgetCatalog:
    outputs: OutputsWidgetCatalog


_widget_catalog = WidgetCatalog(outputs=OutputsWidgetCatalog())


def get_widget_catalog() -> WidgetCatalog:
    global _widget_catalog
    return _widget_catalog
