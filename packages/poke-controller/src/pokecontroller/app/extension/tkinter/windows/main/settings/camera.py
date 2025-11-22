import tkinter as tk
import tkinter.ttk as ttk

from ....utils import (
    separator,
)


class CameraSettings(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
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
        name = tk.StringVar()
        name_label = ttk.Label(upper_frame,
                               text="Camera Name:",
                               anchor=tk.CENTER)
        name_combobox = ttk.Combobox(upper_frame,
                                     state="readonly",
                                     textvariable=name,
                                     values=["Camera 1", "Camera 2"])
        name_combobox.bind("<<ComboboxSelected>>", self.set_camera_id, add="")

        # Lower Frame
        lower_frame = ttk.Frame(labelframe)

        # ID
        id = tk.IntVar()
        id_label = ttk.Label(lower_frame,
                             text="Camera ID:      ",
                             anchor=tk.CENTER)
        id_entry = ttk.Entry(lower_frame,
                             width=3,
                             state=tk.DISABLED,
                             textvariable=id)

        # FPS
        fps_list = [60, 45, 30, 15, 5]
        fps = tk.StringVar()
        fps_label = ttk.Label(lower_frame, text="FPS: ")
        fps_combobox = ttk.Combobox(lower_frame,
                                    width=3,
                                    justify=tk.LEFT,
                                    state="readonly",
                                    textvariable=fps,
                                    values=[str(f) for f in fps_list])
        fps_combobox.bind("<<ComboboxSelected>>", self.set_camera_fps, add="")

        # Size
        size_list: list[tuple[int, int]] = [(320 * i, 180 * i) for i in range(1, 7)]
        size = tk.StringVar()
        size_label = ttk.Label(lower_frame, text="Show Size: ")
        size_combobox = ttk.Combobox(lower_frame,
                                     width=8,
                                     state="readonly",
                                     textvariable=size,
                                     values=[f"{w}x{h}" for w, h in size_list])
        size_combobox.bind("<<ComboboxSelected>>", self.set_camera_size, add="")

        # Reload
        reload_button = ttk.Button(lower_frame,
                                   text="Reload Camera",
                                   command=self.reload_camera)

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
        is_show_realtime = tk.BooleanVar()
        show_realtime_checkbutton = ttk.Checkbutton(labelframe,
                                                    text="Show Realtime",
                                                    variable=is_show_realtime,
                                                    command=self.set_is_show_realtime)

        # Show Value
        is_show_value = tk.BooleanVar()
        show_value_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="Show Value",
                                                 variable=is_show_value,
                                                 command=self.set_is_show_value)

        # Show Guide
        is_show_guide = tk.BooleanVar()
        show_guide_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="Show Guide",
                                                 variable=is_show_guide,
                                                 command=self.set_is_show_guide)

        # Layout
        show_realtime_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)
        show_value_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=8, pady=4)
        show_guide_checkbutton.pack(expand=False, fill=tk.X, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def set_camera_id(self, event):
        pass

    def set_camera_fps(self, event):
        pass

    def set_camera_size(self, event):
        pass

    def reload_camera(self):
        pass

    def set_is_show_realtime(self):
        pass

    def set_is_show_value(self):
        pass

    def set_is_show_guide(self):
        pass
