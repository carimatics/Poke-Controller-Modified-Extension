import tkinter as tk
from dataclasses import dataclass


@dataclass(kw_only=True)
class OutputsWidgetCatalog:
    textarea1: tk.Text | None = None
    textarea2: tk.Text | None = None


@dataclass(kw_only=True)
class WidgetCatalog:
    outputs: OutputsWidgetCatalog


WIDGET_CATALOG_SINGLETON = WidgetCatalog(outputs=OutputsWidgetCatalog())


def get_widget_catalog() -> WidgetCatalog:
    global WIDGET_CATALOG_SINGLETON
    return WIDGET_CATALOG_SINGLETON
