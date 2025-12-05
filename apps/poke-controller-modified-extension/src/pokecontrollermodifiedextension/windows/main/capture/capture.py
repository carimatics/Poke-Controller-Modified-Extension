import logging
import tkinter as tk
from typing import Any

from PIL import Image, ImageTk
from pokecontroller.core import image

from ....values import literals as l
from ....widgets import AppFrame

logger = logging.getLogger(__name__)


class Capture(AppFrame):
    _canvas: tk.Canvas
    _image: ImageTk.PhotoImage
    _image_id: int

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._disabled_raw_image = image.read(
            path="../Images/disabled.png", mode="grayscale"
        )

        self._camera = self.app.camera

        self._camera_id = self.app.gui_state.capture.camera_id
        self._fps = self.app.gui_state.capture.fps
        self._size = self.app.gui_state.capture.size
        self._show_realtime = self.app.gui_state.capture.show_realtime
        self._show_matched = self.app.gui_state.capture.show_matched
        self._show_guide = self.app.gui_state.capture.show_guide
        self._next_frame_time = int(1000 / self._fps.get())
        self._width, self._height = self._parse_size()

        if (disabled_raw_image := self._disabled_raw_image) is not None:
            self._disabled_image = ImageTk.PhotoImage(
                image=Image.fromarray(
                    image.resize(disabled_raw_image, self._parse_size())
                ),
            )
        else:
            self._disabled_image = ImageTk.PhotoImage()

        self._after_id: str | None = None
        self._is_resizing = False
        self._is_disabled = True
        self._is_show_disabled = False
        self._pending_resize: tuple[int, int] | None = None

        self._register_hooks()
        self.build_ui()

        self._update_frame()

    def build_ui(self) -> None:
        self._create_new_canvas()

    def _create_new_canvas(self) -> None:
        logger.info(f"Creating new canvas: {self._width}x{self._height}")
        self._canvas = tk.Canvas(self, width=self._width, height=self._height)
        self._image = self._disabled_image
        self._image_id = self._canvas.create_image(0, 0, anchor=l.NW, image=self._image)
        self._is_disabled = False
        self._canvas.pack(expand=True, fill=l.BOTH)
        logger.info("Canvas recreated")

    def _update_frame(self) -> None:
        logger.info("_update_frame called")
        if self._is_resizing:
            return

        if self._show_realtime.get():
            self._load_frame()

        if not self._is_resizing:
            self._after_id = self.after(
                ms=self._next_frame_time, func=self._update_frame
            )

    def _load_frame(self) -> None:
        try:
            success, frame = self._camera.read()
            if not success or frame is None:
                if self._is_disabled and self._is_show_disabled:
                    return

                self._show_disabled_image()
                return

            self._show_captured_image(frame)

        except Exception as e:
            logger.error(f"Frame load error: {e}")

    def _show_disabled_image(self) -> None:
        self._is_disabled = True
        self._image = self._disabled_image
        self._update_canvas()
        self._is_show_disabled = True

    def _show_captured_image(self, frame: image.RawImage) -> None:
        self._is_disabled = False
        frame_rgb = image.bgr_to_rgb(frame)
        frame_resized = image.resize(frame_rgb, (self._width, self._height))
        self._image = ImageTk.PhotoImage(image=Image.fromarray(frame_resized))
        self._update_canvas()
        self._is_show_disabled = False

    def _register_hooks(self) -> None:
        self._fps.trace_add("write", self._on_fps_changed)
        self._size.trace_add("write", self._on_size_changed)

    def _on_fps_changed(self, *_: Any) -> None:
        self._next_frame_time = int(1000 / self._fps.get())

    def _on_size_changed(self, *_: Any) -> None:
        logger.info("_on_size_changed called")
        self._is_resizing = True

        width, height = self._parse_size()
        self._pending_resize = (width, height)

        logger.info(f"Scheduling resize to {width}x{height}")
        self.after(1, self._resize)
        logger.info("Resize scheduled")

    def _resize(self) -> None:
        logger.info("_resize called")
        if (new_size := self._pending_resize) is None:
            self._is_resizing = False
            return

        # change size properties
        self._width, self._height = new_size
        self._pending_resize = None

        # resize disabled image
        if (disabled_raw_image := self._disabled_raw_image) is not None:
            self._disabled_image = ImageTk.PhotoImage(
                image=Image.fromarray(image.resize(disabled_raw_image, new_size)),
            )
        else:
            self._disabled_image = ImageTk.PhotoImage()
        self._is_show_disabled = False

        # recreate canvas
        logger.info("Destroying canvas")
        self._canvas.destroy()
        self._create_new_canvas()

        logger.info("Scheduling resume")
        self.after(50, self._resume_after_resize)
        logger.info("Resume scheduled")

    def _resume_after_resize(self) -> None:
        logger.info("_resume_after_resize called")
        logger.info(f"current after_id: {self._after_id}")
        logger.info(f"is_resizing: {self._is_resizing}")
        self._is_resizing = False
        logger.info(f"After setting False, after_id: {self._after_id}")
        self._update_frame()
        logger.info("_resume_after_resize complete")

    def _parse_size(self) -> tuple[int, int]:
        width, height = self._size.get().split("x")
        return int(width), int(height)

    def _update_canvas(self) -> None:
        logger.info("_update_canvas called")
        if not self._is_resizing:
            self._canvas.itemconfig(self._image_id, image=self._image)
