import tkinter as tk
from dataclasses import dataclass
from typing import Callable


@dataclass(kw_only=True)
class OutputsWidgetCatalog:
    textarea1: tk.Text | None = None
    textarea2: tk.Text | None = None

    def clear_textarea(self, textarea_id: int) -> None:
        if (textarea := getattr(self, f"textarea{textarea_id}")) is not None:
            textarea.config(state=tk.NORMAL)
            textarea.delete("1.0", tk.END)
            textarea.config(state=tk.DISABLED)

    def clear_textareas(self) -> None:
        for i in [1, 2]:
            self.clear_textarea(i)


@dataclass(kw_only=True)
class CaptureWidgetCatalog:
    canvas: tk.Canvas | None = None


@dataclass(kw_only=True)
class WindowWidgetCatalog:
    controller: tk.Toplevel | None = None
    settings: tk.Toplevel | None = None

    def open_controller(
        self,
        master: tk.Misc,
        gen: Callable[[tk.Misc], tk.Toplevel],
    ) -> None:
        if (window := self.controller) is not None:
            if window.winfo_exists():
                window.lift()
                return
        self.controller = gen(master)
        self.controller.protocol(
            "WM_DELETE_WINDOW",
            self._on_controller_closed,
        )

    def open_settings(
        self,
        master: tk.Misc,
        gen: Callable[[tk.Misc], tk.Toplevel],
    ) -> None:
        if (window := self.settings) is not None:
            if window.winfo_exists():
                window.lift()
                return
        self.settings = gen(master)
        self.settings.protocol(
            "WM_DELETE_WINDOW",
            self._on_settings_closed,
        )

    def _on_controller_closed(self) -> None:
        self._destroy(self.controller)
        self.controller = None

    def _on_settings_closed(self) -> None:
        self._destroy(self.settings)
        self.settings = None

    def _destroy(self, window: tk.Toplevel | None) -> None:
        if window is None:
            return
        if window.winfo_exists():
            window.destroy()


@dataclass(kw_only=True)
class AppWidgetCatalog:
    outputs: OutputsWidgetCatalog
    capture: CaptureWidgetCatalog
    window: WindowWidgetCatalog
