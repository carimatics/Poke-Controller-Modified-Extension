import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....components import AppFrame
from ....utils import separator
from ....values import literals as l


class CameraSettings(AppFrame):
    def __init__(
        self,
        master: tk.Misc,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ):
        super().__init__(master, *args, **kwargs)

        self._name_list: list[str] = self._load_camera_list()
        self._size_list: list[str] = self._load_camera_size_list()

        self._id = self.app_state.camera_id
        self._camera_name = self.app_state.camera_name
        self._fps = self.app_state.camera_fps
        self._size = self.app_state.camera_size
        self._show_realtime = self.app_state.camera_show_realtime
        self._show_value = self.app_state.camera_show_matched
        self._show_guide = self.app_state.camera_show_guide

        self.build_ui()

    def build_ui(self) -> None:
        # Create Labelframes
        camera_settings = self._build_camera_settings()
        display_settings = self._build_display_settings()

        # Layout
        camera_settings.pack(expand=False, fill=l.BOTH, pady=4)
        display_settings.pack(expand=False, fill=l.BOTH, pady=4)

    def _build_camera_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Camera Settings")

        # Upper Frame
        upper_frame = ttk.Frame(labelframe)

        # Name
        name_label = ttk.Label(
            upper_frame,
            text="Camera Name: ",
            width=11,
            anchor=l.CENTER,
        )
        name_combobox = ttk.Combobox(
            upper_frame,
            state=l.READONLY,
            textvariable=self._camera_name.container,
            values=self._name_list,
        )
        # FIXME: 必要か検証する
        name_combobox.bind(
            "<<ComboboxSelected>>",
            self._on_camera_name_selected,
            add="",
        )
        name_combobox.current(0)
        self._id.set(self._name_list[0])

        # Lower Frame
        lower_frame = ttk.Frame(labelframe)

        # ID
        id_label = ttk.Label(
            lower_frame,
            text="Camera ID: ",
            width=11,
            anchor=l.W,
        )
        id_entry = ttk.Entry(
            lower_frame,
            width=3,
            state=l.DISABLED,
            textvariable=self._id.container,
        )

        # FPS
        fps_list = [60, 45, 30, 15, 5]
        fps_label = ttk.Label(lower_frame, text="FPS: ")
        fps_combobox = ttk.Combobox(
            lower_frame,
            width=3,
            justify=l.LEFT,
            state=l.READONLY,
            textvariable=self._fps.container,
            values=[str(f) for f in fps_list],
        )
        # FIXME: 必要か検証する
        fps_combobox.bind("<<ComboboxSelected>>", self._on_camera_fps_selected, add="")

        # Size
        size_label = ttk.Label(lower_frame, text="Show Size: ")
        size_combobox = ttk.Combobox(
            lower_frame,
            width=8,
            state=l.READONLY,
            textvariable=self._size.container,
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
        name_label.pack(expand=False, fill=l.X, side=l.LEFT)
        name_combobox.pack(expand=True, fill=l.X, side=l.LEFT)
        upper_frame.pack(expand=True, fill=l.X, side=l.TOP, padx=4, pady=4)

        id_label.pack(expand=False, fill=l.X, side=l.LEFT)
        id_entry.pack(expand=True, fill=l.X, side=l.LEFT)
        # noinspection DuplicatedCode
        separator(lower_frame).pack(expand=False, fill=l.Y, side=l.LEFT, padx=5, pady=8)
        fps_label.pack(expand=False, fill=l.X, side=l.LEFT)
        fps_combobox.pack(expand=False, fill=l.X, side=l.LEFT)
        # noinspection DuplicatedCode
        separator(lower_frame).pack(expand=False, fill=l.Y, side=l.LEFT, padx=5, pady=8)
        size_label.pack(expand=False, fill=l.X, side=l.LEFT)
        size_combobox.pack(expand=False, fill=l.X, side=l.LEFT)
        separator(lower_frame).pack(expand=False, fill=l.Y, side=l.LEFT, padx=5, pady=8)
        reload_button.pack(expand=False, fill=l.X, side=l.LEFT, padx=4)
        lower_frame.pack(expand=True, fill=l.BOTH, side=l.TOP, padx=4, pady=4)

        return labelframe

    def _build_display_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Display Settings")

        # Show Realtime
        show_realtime_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Show Realtime",
            variable=self._show_realtime.container,
            command=self._on_show_realtime_changed,
        )

        # Show Value
        show_matched_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Show Matched",
            variable=self._show_value.container,
            command=self._on_show_matched_changed,
        )

        # Show Guide
        show_guide_checkbutton = ttk.Checkbutton(
            labelframe,
            text="Show Guide",
            variable=self._show_guide.container,
            command=self._on_show_guide_changed,
        )

        # Layout
        show_realtime_checkbutton.pack(
            expand=False, fill=l.X, side=l.LEFT, padx=4, pady=4
        )
        show_matched_checkbutton.pack(
            expand=False, fill=l.X, side=l.LEFT, padx=8, pady=4
        )
        show_guide_checkbutton.pack(expand=False, fill=l.X, side=l.LEFT, padx=4, pady=4)

        return labelframe

    def _load_camera_list(self) -> list[str]:
        return self.app_model.load_camera_list()

    def _load_camera_size_list(self) -> list[str]:
        return self.app_model.load_camera_size_list()

    def _on_camera_name_selected(self, _event: tk.Event) -> None:
        self.app_model.apply_camera_name()

    def _on_camera_fps_selected(self, _event: tk.Event) -> None:
        self.app_model.apply_camera_fps()

    def _on_camera_size_selected(self, _event: tk.Event) -> None:
        self.app_model.apply_camera_size()

    def _on_reload_pushed(self) -> None:
        self.app_model.connect_camera()

    def _on_show_realtime_changed(self) -> None:
        self.app_model.apply_camera_show_realtime()

    def _on_show_matched_changed(self) -> None:
        self.app_model.apply_camera_show_matched()

    def _on_show_guide_changed(self) -> None:
        self.app_model.apply_camera_show_guide()
