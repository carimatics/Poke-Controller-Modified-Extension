import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame
from ....utils import (
    separator,
)


class CameraSettings(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.name_list: list[str] = self.app_model.load_camera_list()
        self.size_list: list[str] = self.app_model.load_camera_size_list()

        # noinspection PyTypeChecker
        self.id: tk.StringVar = self.app_state.camera_id
        # noinspection PyTypeChecker
        self.name: tk.StringVar = self.app_state.camera_name
        # noinspection PyTypeChecker
        self.fps: tk.IntVar = self.app_state.camera_fps
        # noinspection PyTypeChecker
        self.size: tk.StringVar = self.app_state.camera_size
        # noinspection PyTypeChecker
        self.show_realtime: tk.BooleanVar = self.app_state.camera_show_realtime
        # noinspection PyTypeChecker
        self.show_value: tk.BooleanVar = self.app_state.camera_show_matched
        # noinspection PyTypeChecker
        self.show_guide: tk.BooleanVar = self.app_state.camera_show_guide

        self.build_ui()

    def build_ui(self):
        # Create Labelframes
        camera_settings = self.build_camera_settings()
        display_settings = self.build_display_settings()

        # Layout
        camera_settings.pack(expand=False, fill=tk.BOTH, pady=4)
        display_settings.pack(expand=False, fill=tk.BOTH, pady=4)

    def build_camera_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Camera Settings")

        # Upper Frame
        upper_frame = ttk.Frame(labelframe)

        # Name
        name_label = ttk.Label(upper_frame,
                               text="Camera Name: ",
                               width=11,
                               anchor=tk.CENTER)
        name_combobox = ttk.Combobox(upper_frame,
                                     state="readonly",
                                     textvariable=self.name,
                                     values=self.name_list)
        # FIXME: 必要か検証する
        name_combobox.bind("<<ComboboxSelected>>", self.app_model.apply_camera_name, add="")
        name_combobox.current(0)
        self.id.set(self.name_list[0])

        # Lower Frame
        lower_frame = ttk.Frame(labelframe)

        # ID
        id_label = ttk.Label(lower_frame,
                             text="Camera ID: ",
                             width=11,
                             anchor=tk.W)
        id_entry = ttk.Entry(lower_frame,
                             width=3,
                             state=tk.DISABLED,
                             textvariable=self.id)

        # FPS
        fps_list = [60, 45, 30, 15, 5]
        fps_label = ttk.Label(lower_frame, text="FPS: ")
        fps_combobox = ttk.Combobox(lower_frame,
                                    width=3,
                                    justify=tk.LEFT,
                                    state="readonly",
                                    textvariable=self.fps,
                                    values=[str(f) for f in fps_list])
        # FIXME: 必要か検証する
        fps_combobox.bind("<<ComboboxSelected>>", self.app_model.apply_camera_fps, add="")

        # Size
        size_label = ttk.Label(lower_frame, text="Show Size: ")
        size_combobox = ttk.Combobox(lower_frame,
                                     width=8,
                                     state="readonly",
                                     textvariable=self.size,
                                     values=self.size_list)
        # FIXME: 必要か検証する
        size_combobox.bind("<<ComboboxSelected>>", self.app_model.apply_camera_size, add="")
        size_combobox.current(self.size_list.index(self.size.get()))

        # Reload
        reload_button = ttk.Button(lower_frame,
                                   text="Reload Camera",
                                   command=self.app_model.connect_camera)

        # Layout
        name_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        name_combobox.pack(expand=True, fill=tk.X, side=tk.LEFT)
        upper_frame.pack(expand=True, fill=tk.X, side=tk.TOP, padx=4, pady=4)

        id_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        id_entry.pack(expand=True, fill=tk.X, side=tk.LEFT)
        separator(lower_frame).pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8)
        fps_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        fps_combobox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        separator(lower_frame).pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8)
        size_label.pack(expand=False, fill=tk.X, side=tk.LEFT)
        size_combobox.pack(expand=False, fill=tk.X, side=tk.LEFT)
        separator(lower_frame).pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=5, pady=8)
        reload_button.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4)
        lower_frame.pack(expand=True, fill=tk.BOTH, side=tk.TOP, padx=4, pady=4)

        return labelframe

    def build_display_settings(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Display Settings")

        # Show Realtime
        show_realtime_checkbutton = ttk.Checkbutton(labelframe,
                                                    text="Show Realtime",
                                                    variable=self.show_realtime,
                                                    command=self.app_model.apply_camera_show_realtime)

        # Show Value
        show_matched_checkbutton = ttk.Checkbutton(labelframe,
                                                   text="Show Matched",
                                                   variable=self.show_value,
                                                   command=self.app_model.apply_camera_show_matched)

        # Show Guide
        show_guide_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="Show Guide",
                                                 variable=self.show_guide,
                                                 command=self.app_model.apply_camera_show_guide)

        # Layout
        show_realtime_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        show_matched_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=8, pady=4)
        show_guide_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe
