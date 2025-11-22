import tkinter as tk
import tkinter.ttk as ttk


class NotificationSettings(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.build_ui()

    def build_ui(self):
        windows_notification = self.build_windows_notification()
        discord_notification = self.build_discord_notification()

        # Layout
        windows_notification.pack(expand=False, fill=tk.NONE, anchor=tk.NE, side=tk.LEFT, padx=4)
        discord_notification.pack(expand=False, fill=tk.NONE, anchor=tk.NE, side=tk.LEFT, padx=8)

    def build_windows_notification(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Windows Notification")

        # Start
        is_enable_start = tk.BooleanVar()
        enable_start_checkbutton = ttk.Checkbutton(labelframe,
                                                   text="Start",
                                                   variable=is_enable_start,
                                                   command=self.set_is_enable_start_windows_notification)

        # End
        is_enable_end = tk.BooleanVar()
        enable_end_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="End",
                                                 variable=is_enable_end,
                                                 command=self.set_is_enable_end_windows_notification)

        # Test
        test_button = ttk.Button(labelframe,
                                 text="Test",
                                 command=self.test_windows_notification)

        # Layout
        enable_start_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4)
        enable_end_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=8)
        test_button.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4)

        return labelframe

    def build_discord_notification(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Discord Notification")

        # Start
        is_enable_start = tk.BooleanVar()
        enable_start_checkbutton = ttk.Checkbutton(labelframe,
                                                   text="Start",
                                                   variable=is_enable_start,
                                                   command=self.set_is_enable_start_discord_notification)

        # End
        is_enable_end = tk.BooleanVar()
        enable_end_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="End",
                                                 variable=is_enable_end,
                                                 command=self.set_is_enable_end_discord_notification)

        # Test
        test_button = ttk.Button(labelframe,
                                 text="Test",
                                 command=self.test_discord_notification)
        # Layout
        enable_start_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4)
        enable_end_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=8)
        test_button.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4)

        return labelframe

    def set_is_enable_start_windows_notification(self):
        pass

    def set_is_enable_end_windows_notification(self):
        pass

    def set_is_enable_start_discord_notification(self):
        pass

    def set_is_enable_end_discord_notification(self):
        pass

    def test_windows_notification(self):
        pass

    def test_discord_notification(self):
        pass
