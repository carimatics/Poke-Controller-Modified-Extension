import logging
import tkinter as tk
from typing import Any

from .frame import Frame
from .scrollbar import Scrollbar

logger = logging.getLogger(__name__)


class ScrollableFrame(Frame):
    _canvas: tk.Canvas
    _scrollbar: Scrollbar
    _canvas_window: int

    def __init__(
        self,
        master: tk.Misc,
        **kwargs: Any,
    ) -> None:
        self._canvas = tk.Canvas(master, highlightthickness=0)
        self._scrollbar = Scrollbar(
            master, orient="vertical", command=self._canvas.yview
        )
        super().__init__(self._canvas, **kwargs)

        self.build_ui()

    def build_ui(self) -> None:
        self.bind("<<Configure>>", self._on_frame_configure)
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self, anchor=tk.NW
        )
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.bind(
            "<Configure>",
            self._on_canvas_configure,
        )
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self._canvas.bind_all("<Button-4>", self._on_mouse_wheel)
        self._canvas.bind_all("<Button-5>", self._on_mouse_wheel)

    def _on_frame_configure(self, _: tk.Event) -> None:
        self._update_scroll_region()

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self._canvas.itemconfig(
            self._canvas_window,
            width=event.width,
        )
        self._update_scroll_region()

    def _update_scroll_region(self) -> None:
        self._canvas.update_idletasks()

        bbox = self._canvas.bbox("all")
        content_height = bbox[3] - bbox[1]
        canvas_height = self._canvas.winfo_height()

        if content_height > canvas_height:
            self._canvas.configure(scrollregion=bbox)
            self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self._canvas.configure(scrollregion=(0, 0, 0, canvas_height))
            self._canvas.yview_moveto(0)
            self._scrollbar.pack_forget()

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        bbox = self._canvas.bbox("all")
        if bbox and bbox[3] > self._canvas.winfo_height():
            if event.num == 5 or event.delta < 0:
                self._canvas.yview_scroll(1, "units")
            if event.num == 4 or event.delta > 0:
                self._canvas.yview_scroll(-1, "units")
