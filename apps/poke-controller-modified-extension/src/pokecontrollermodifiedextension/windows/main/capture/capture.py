import logging
import tkinter as tk
from typing import Any

from pokecontroller.core import image
from PIL import ImageTk, Image

from ....widgets import AppFrame
from ....values import literals as l

logger = logging.getLogger(__name__)


class Capture(AppFrame):
    _canvas: tk.Canvas
    _image: tk.PhotoImage
    _image_tag: int

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._disabled_image = ImageTk.PhotoImage(file="../Images/disabled.png")

        self._camera = self.app.camera

        self._fps = self.app.gui_state.capture.fps
        self._size = self.app.gui_state.capture.size
        self._show_realtime = self.app.gui_state.capture.show_realtime
        self._show_matched = self.app.gui_state.capture.show_matched
        self._show_guide = self.app.gui_state.capture.show_guide
        self._next_frame_time = int(1000 / self._fps.get())
        self._width, self._height = self._parse_size()

        self._register_hooks()

        self.build_ui()
        self._update_frame()

    def build_ui(self) -> None:
        self._canvas = tk.Canvas(self, width=self._width, height=self._height)
        self._image = ImageTk.PhotoImage(file="../Images/disabled.png")
        self._image_tag = self._canvas.create_image(0, 0, anchor=l.NW, image=self._image)
        self._canvas.pack(expand=True, fill=l.BOTH)

    def _update_frame(self) -> None:
        if self._show_realtime.get():
            self._load_frame()

        self.after(ms=self._next_frame_time, func=self._update_frame)

    def _load_frame(self) -> None:
        success, frame = self._camera.read()

        if not success:
            return

        frame_rgb = image.bgr_to_rgb(frame)
        frame_resized = image.resize(frame_rgb, (self._width, self._height))
        self._image = ImageTk.PhotoImage(image=Image.fromarray(frame_resized))
        self._canvas.itemconfig(self._image_tag, image=self._image)

    def _register_hooks(self) -> None:
        self._fps.trace_add("write", self._on_fps_changed)
        self._size.trace_add("write", self._on_size_changed)

    def _on_fps_changed(self, *_: Any) -> None:
        self._next_frame_time = int(1000 / self._fps.get())

    def _on_size_changed(self, *_: Any) -> None:
        width, height = self._parse_size()
        self.configure(width=width, height=height)
        self._canvas.config(width=width, height=height)
        self._width, self._height = width, height

    def _parse_size(self) -> tuple[int, int]:
        width, height = self._size.get().split("x")
        return int(width), int(height)
