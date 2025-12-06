import logging
import tkinter as tk
from typing import Any

from PIL import Image, ImageTk
from pokecontroller.core import image

from ....values import literals as l
from ....widgets import AppFrame

logger = logging.getLogger(__name__)

type Font = (
    str
    | tk.font.Font
    | list[Any]
    | tuple[str]
    | tuple[str, int]
    | tuple[str, int, str]
    | tuple[str, int, list[str] | tuple[str, ...]]
)


class Capture(AppFrame):
    _canvas: tk.Canvas
    _ratio: tuple[float, float]
    _image: ImageTk.PhotoImage
    _image_id: int

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._disabled_raw_image = image.read(
            path="../Images/disabled.png", mode="grayscale"
        )

        self._camera = self.app.camera
        self._serial = self.app.serial

        self._camera_id = self.app.gui_state.capture.camera_id
        self._fps = self.app.gui_state.capture.fps
        self._size = self.app.gui_state.capture.size
        self._show_realtime = self.app.gui_state.capture.show_realtime
        self._show_matched = self.app.gui_state.capture.show_matched
        self._show_guide = self.app.gui_state.capture.show_guide
        self._next_frame_time = 1000 // self._fps.get()
        self._width, self._height = self._parse_size()
        self._update_ratio()

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

        self.build_ui()

        self._register_hooks()
        self._update_frame()

    @property
    def frame_size(self) -> tuple[int, int]:
        return self._camera.frame_size

    def build_ui(self) -> None:
        self._create_new_canvas()

    def _register_hooks(self) -> None:
        self._fps.trace_add("write", self._on_fps_changed)
        self._size.trace_add("write", self._on_size_changed)

    def _update_frame(self) -> None:
        if self._show_realtime.get():
            self._load_frame()

        self._after_id = self.after(ms=self._next_frame_time, func=self._update_frame)

    def _draw_rect(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        *,
        outline: str,
        width: int,
        tag: str,
        ratio: tuple[float, float] | None = None,
        delete_after_ms: int | None = 100,
    ) -> None:
        if not self._show_realtime.get() or self._is_resizing:
            return

        rat = ratio if ratio is not None else self._ratio
        self._canvas.create_rectangle(
            (start[0] - 1.0) * rat[0],
            (start[1] - 1.0) * rat[1],
            (end[0] + 1.0) * rat[0],
            (end[1] + 1.0) * rat[1],
            width=width,
            outline=outline,
            tags=tag,
        )
        if delete_after_ms is not None:
            self.after(delete_after_ms, self._delete_tagged_item, tag)

    def _draw_circle(
        self,
        center: tuple[int, int],
        radius: int,
        *,
        outline: str,
        tag: str,
        ratio: tuple[float, float] | None = None,
        delete_after_ms: int | None = 100,
    ) -> None:
        if not self._show_realtime.get() or self._is_resizing:
            return

        rat = ratio if ratio is not None else self._ratio
        self._canvas.create_oval(
            (center[0] - radius) * rat[0],
            (center[1] - radius) * rat[1],
            (center[0] + radius) * rat[0],
            (center[1] + radius) * rat[1],
            width=2.5,
            outline=outline,
            tags=tag,
        )
        if delete_after_ms is not None:
            self.after(delete_after_ms, self._delete_tagged_item, tag)

    def _draw_text(
        self,
        start: tuple[int, int],
        text: str,
        *,
        font: Font,
        color: str,
        tag: str,
        ratio: tuple[float, float] | None = None,
        delete_after_ms: int | None = 100,
    ) -> None:
        if not self._show_realtime.get() or self._is_resizing:
            return

        rat = ratio if ratio is not None else self._ratio
        self._canvas.create_text(
            (start[0] - 1.0) * rat[0],
            (start[1] - 1.0) * rat[1],
            text=text,
            font=font,
            fill=color,
            tags=tag,
        )
        if delete_after_ms is not None:
            self.after(delete_after_ms, self._delete_tagged_item, tag)

    def _delete_tagged_item(self, tag: str) -> None:
        self._canvas.delete(tag)

    def _create_new_canvas(self) -> None:
        logger.info(f"Creating new canvas: {self._width}x{self._height}")
        self._canvas = tk.Canvas(self, width=self._width, height=self._height)
        self._image = self._disabled_image
        self._image_id = self._canvas.create_image(0, 0, anchor=l.NW, image=self._image)
        self._is_disabled = False
        self._canvas.pack(expand=True, fill=l.BOTH)
        logger.info("Canvas recreated")

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

    def _on_fps_changed(self, *_: Any) -> None:
        self._next_frame_time = 1000 // self._fps.get()

    def _on_size_changed(self, *_: Any) -> None:
        if self._show_realtime.get():
            return
        self._resize()
        self._width, self._height = self._parse_size()

    def _resize(self) -> None:
        # change size properties
        new_size = self._parse_size()

        logger.info(f"Resizing canvas: ({self._width}, {self._height}) -> {new_size}")

        self._width, self._height = new_size
        self._update_ratio()
        # resize disabled image
        if (disabled_raw_image := self._disabled_raw_image) is not None:
            self._disabled_image = ImageTk.PhotoImage(
                image=Image.fromarray(image.resize(disabled_raw_image, new_size)),
            )
        else:
            self._disabled_image = ImageTk.PhotoImage()
        self._is_show_disabled = False

        logger.info("Destroying canvas")
        self._canvas.destroy()
        self._create_new_canvas()

    def _parse_size(self) -> tuple[int, int]:
        width, height = self._size.get().split("x")
        return int(width), int(height)

    def _update_canvas(self) -> None:
        if not self._is_resizing:
            self._canvas.itemconfig(self._image_id, image=self._image)

    def _update_ratio(self) -> None:
        self._ratio = (
            self._width / self.frame_size[0],
            self._height / self.frame_size[1],
        )
