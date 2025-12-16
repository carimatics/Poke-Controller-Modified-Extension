import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....model import get_app_model
from ....settings import get_app_settings
from ....widgets.app import AppFrame


class CameraSettings(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._app_settings = get_app_settings()
        self._app_model = get_app_model()

        self._name_list: list[str] = self._load_camera_list()
        self._size_list: list[str] = self._load_camera_size_list()

        self._camera_id = self._app_settings.capture.camera_id
        self._camera_name = self._app_settings.capture.camera_name
        self._fps = self._app_settings.capture.fps
        self._size = self._app_settings.capture.size
        self._show_realtime = self._app_settings.capture.show_realtime
        self._show_matched = self._app_settings.capture.show_matched
        self._show_guide = self._app_settings.capture.show_guide

        self.build_ui()

    def build_ui(self) -> None:
        # Create Labelframes
        camera_settings = self._build_camera_settings()
        display_settings = self._build_display_settings()

        # Layout
        camera_settings.pack(expand=False, fill=tk.BOTH, pady=4)
        display_settings.pack(expand=False, fill=tk.BOTH, pady=4)

    def _build_camera_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Camera Settings")

        # Upper Frame
        upper_frame = ttk.Frame(labelframe)

        # Name
        name_label = ttk.Label(
            upper_frame,
            text="Camera Name: ",
            width=11,
            anchor=tk.CENTER,
        )
        name_combobox = ttk.Combobox(
            upper_frame,
            state="readonly",
            textvariable=self._camera_name,
            values=self._name_list,
        )
        # FIXME: 必要か検証する
        name_combobox.bind(
            "<<ComboboxSelected>>",
            self._on_camera_name_selected,
            add="",
        )
        self._camera_name.set(self._name_list[0])

        # Lower Frame
        lower_frame = ttk.Frame(labelframe)

        # ID
        id_label = ttk.Label(
            lower_frame,
            text="Camera ID: ",
            width=11,
            anchor=tk.W,
        )
        id_entry = ttk.Entry(
            lower_frame,
            width=3,
            state=tk.DISABLED,
            textvariable=self._camera_id,
        )

        # FPS
        fps_list = [60, 45, 30, 15, 5]
        fps_label = ttk.Label(lower_frame, text="FPS: ")
        fps_combobox = ttk.Combobox(
            lower_frame,
            width=3,
            justify=tk.LEFT,
            state="readonly",
            textvariable=self._fps,
            values=[str(f) for f in fps_list],
        )
        # FIXME: 必要か検証する
        fps_combobox.bind("<<ComboboxSelected>>", self._on_camera_fps_selected, add="")

        # Size
        size_label = ttk.Label(lower_frame, text="Show Size: ")
        size_combobox = ttk.Combobox(
            lower_frame,
            width=8,
            state="readonly",
            textvariable=self._size,
            values=self._size_list,
        )
        # FIXME: 必要か検証する
        size_combobox.bind(
            "<<ComboboxSelected>>",
            self._on_camera_size_selected,
            add="",
        )
        size_combobox.current(self._size_list.index(self._size.get()))

        # Reload
        reload_button = ttk.Button(
            lower_frame,
            text="Reload Camera",
            command=self._on_reload_pushed,
        )

        # Layout
        name_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        name_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        upper_frame.pack(expand=True, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        id_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        id_entry.pack(expand=True, fill=tk.X, side=tk.LEFT)
        # noinspection DuplicatedCode
        ttk.Separator(master=lower_frame, orient=tk.VERTICAL).pack(
            expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8
        )
        fps_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        fps_combobox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        # noinspection DuplicatedCode
        ttk.Separator(master=lower_frame, orient=tk.VERTICAL).pack(
            expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8
        )
        size_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        size_combobox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        ttk.Separator(master=lower_frame, orient=tk.VERTICAL).pack(
            expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8
        )
        reload_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        lower_frame.pack(expand=True, fill=tk.BOTH, side=tk.TOP, padx=4, pady=4)

        return labelframe

    def _build_display_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Display Settings")

        # Show Realtime
        show_realtime_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Show Realtime",
            variable=self._show_realtime,
            command=self._on_show_realtime_changed,
        )

        # Show Value
        show_matched_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Show Matched",
            variable=self._show_matched,
            command=self._on_show_matched_changed,
        )

        # Show Guide
        show_guide_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Show Guide",
            variable=self._show_guide,
            command=self._on_show_guide_changed,
        )

        # Layout
        show_realtime_checkbutton.pack(
            expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4
        )
        show_matched_checkbutton.pack(
            expand=False, fill=tk.X, side=tk.LEFT, padx=8, pady=4
        )
        show_guide_checkbutton.pack(
            expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4
        )

        return labelframe

    def _load_camera_list(self) -> list[str]:
        return self._app_model.load_camera_list()

    def _load_camera_size_list(self) -> list[str]:
        return self._app_model.load_camera_size_list()

    def _on_camera_name_selected(self, _event: tk.Event) -> None:
        self._app_model.apply_camera_name()

    def _on_camera_fps_selected(self, _event: tk.Event) -> None:
        self._app_model.apply_camera_fps()

    def _on_camera_size_selected(self, _event: tk.Event) -> None:
        self._app_model.apply_camera_size()

    def _on_reload_pushed(self) -> None:
        self._app_model.connect_camera()

    def _on_show_realtime_changed(self) -> None:
        self._app_model.apply_camera_show_realtime()

    def _on_show_matched_changed(self) -> None:
        self._app_model.apply_camera_show_matched()

    def _on_show_guide_changed(self) -> None:
        self._app_model.apply_camera_show_guide()
