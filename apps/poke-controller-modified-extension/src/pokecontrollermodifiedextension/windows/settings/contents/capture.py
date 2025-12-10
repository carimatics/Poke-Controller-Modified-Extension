import logging
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....widgets import AppFrame

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
        frame = ttk.Frame(self)

        # camera_id
        camera_id_frame = ttk.Frame(frame)
        camera_id_label = ttk.Label(camera_id_frame, width=16, text="Camera ID:")
        camera_id_combobox = ttk.Combobox(
            camera_id_frame,
            textvariable=self._camera_id,
            values=self.app.app_model.load_camera_list(),
        )

        # camera_name
        camera_name = ttk.Frame(frame)
        camera_name_label = ttk.Label(camera_name, width=16, text="Camera Name:")
        camera_name_value = ttk.Label(camera_name, textvariable=self._camera_name)

        # fps
        fps_frame = ttk.Frame(frame)
        fps_label = ttk.Label(fps_frame, width=16, text="FPS:")
        fps_spinbox = ttk.Spinbox(
            fps_frame,
            textvariable=self._fps,
            from_=1,
            to=60,
            increment=1,
        )

        # size
        camera_size_frame = ttk.Frame(frame)
        camera_size_label = ttk.Label(camera_size_frame, width=16, text="Camera Size:")
        self._camera_size_scale = ttk.Scale(
            camera_size_frame,
            from_=1,
            to=80,
            orient=tk.HORIZONTAL,
            state=tk.DISABLED if self._show_realtime.get() else tk.NORMAL,
            variable=self._camera_size_scale_value,
        )

        # show_realtime
        show_realtime_frame = ttk.Frame(frame)
        show_realtime_label = ttk.Label(
            show_realtime_frame, width=16, text="Show Realtime:"
        )
        show_realtime_checkbutton = ttk.Checkbutton(
            show_realtime_frame, variable=self._show_realtime
        )

        # show_matched
        show_matched_frame = ttk.Frame(frame)
        show_matched_label = ttk.Label(
            show_matched_frame, width=16, text="Show Matched Area:"
        )
        show_matched_checkbutton = ttk.Checkbutton(
            show_matched_frame, variable=self._show_matched
        )

        # show_guide
        show_guide_frame = ttk.Frame(frame)
        show_guide_label = ttk.Label(show_guide_frame, width=16, text="Show Guide:")
        show_guide_checkbutton = ttk.Checkbutton(
            show_guide_frame, variable=self._show_guide
        )

        # Layout
        camera_id_label.pack(side=tk.LEFT)
        camera_id_combobox.pack(side=tk.LEFT, padx=4)
        camera_id_frame.pack(expand=False, fill=tk.X)

        camera_name_label.pack(side=tk.LEFT)
        camera_name_value.pack(side=tk.LEFT, padx=4)
        camera_name.pack(expand=False, fill=tk.X)

        fps_label.pack(side=tk.LEFT)
        fps_spinbox.pack(side=tk.LEFT, padx=4)
        fps_frame.pack(expand=False, fill=tk.X)

        camera_size_label.pack(side=tk.LEFT)
        self._camera_size_scale.pack(side=tk.LEFT, padx=4)
        camera_size_frame.pack(expand=False, fill=tk.X)

        show_realtime_label.pack(side=tk.LEFT)
        show_realtime_checkbutton.pack(side=tk.LEFT, padx=4)
        show_realtime_frame.pack(expand=False, fill=tk.X)

        show_matched_label.pack(side=tk.LEFT)
        show_matched_checkbutton.pack(side=tk.LEFT, padx=4)
        show_matched_frame.pack(expand=False, fill=tk.X)

        show_guide_label.pack(side=tk.LEFT)
        show_guide_checkbutton.pack(side=tk.LEFT, padx=4)
        show_guide_frame.pack(expand=False, fill=tk.X)

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
        self._trace_ids.append(
            (
                self._show_realtime,
                self._show_realtime.trace_add("write", self._on_show_realtime_changed),
            )
        )

    def _on_camera_size_scale_value_changed(self, *_: Any) -> None:
        if self._show_realtime.get():
            return
        scale = self._camera_size_scale_value.get()
        self._camera_size.set(f"{scale * 16}x{scale * 9}")

    def _on_show_realtime_changed(self, *_: Any) -> None:
        self._camera_size_scale.configure(
            state=tk.DISABLED if self._show_realtime.get() else tk.NORMAL
        )

    def destroy(self) -> None:
        for var, trace_id in self._trace_ids:
            var.trace_remove("write", trace_id)
