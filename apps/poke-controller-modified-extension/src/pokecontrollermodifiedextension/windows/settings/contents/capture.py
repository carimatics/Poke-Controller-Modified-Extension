import logging
import tkinter as tk
from typing import Any

from ....widgets.app import AppFrame
from .dynamic_input import DynamicInputsBuilder

logger = logging.getLogger(__name__)


class CaptureSettingsPane(AppFrame):
    _camera_size_scale: tk.Scale

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._camera_id = self.app.settings.capture.camera_id
        self._camera_name = self.app.settings.capture.camera_name
        self._fps = self.app.settings.capture.fps
        self._camera_size = self.app.settings.capture.size
        self._camera_size_scale_value = tk.IntVar(
            value=int(self._camera_size.get().split("x")[0]) // 16,
        )
        self._show_realtime = self.app.settings.capture.show_realtime
        self._show_matched = self.app.settings.capture.show_matched
        self._show_guide = self.app.settings.capture.show_guide

        self._trace_ids: list[tuple[tk.Variable, str]] = []
        self._register_hooks()
        self.build_ui()

    def build_ui(self) -> None:
        frame = (
            DynamicInputsBuilder(self, label_width=16)
            .add_combobox_row(
                "Camera ID:", self._camera_id, self.app.app_model.load_camera_list()
            )
            .add_label_row("Camera Name:", self._camera_name)
            .add_spinbox_row(
                "FPS:",
                self._fps,
                from_=1,
                to=60,
                increment=1,
                disabled=self._show_realtime,
            )
            .add_scale_row(
                "Camera Size:",
                self._camera_size_scale_value,
                from_=1,
                to=80,
                disabled=self._show_realtime,
            )
            .add_checkbutton_row("Show Realtime:", "", self._show_realtime)
            .add_checkbutton_row("Show Matched:", "", self._show_matched)
            .add_checkbutton_row("Show Guide:", "", self._show_guide)
            .build()
        )
        frame.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)

    def _register_hooks(self) -> None:
        self._trace_ids.append(
            (
                self._camera_size_scale_value,
                self._camera_size_scale_value.trace_add(
                    "write", self._on_camera_size_scale_value_changed
                ),
            )
        )

    def _on_camera_size_scale_value_changed(self, *_: Any) -> None:
        if self._show_realtime.get():
            return
        scale = self._camera_size_scale_value.get()
        self._camera_size.set(f"{scale * 16}x{scale * 9}")

    def destroy(self) -> None:
        for var, trace_id in self._trace_ids:
            var.trace_remove("write", trace_id)
        super().destroy()
