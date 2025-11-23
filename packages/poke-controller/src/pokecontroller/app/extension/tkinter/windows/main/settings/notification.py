import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame


class NotificationSettings(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.enabled_notify_windows_start = self.app_state.notification_enabled_windows_start
        self.enabled_notify_windows_end = self.app_state.notification_enabled_windows_end
        self.enabled_notify_discord_start = self.app_state.notification_enabled_discord_start
        self.enabled_notify_discord_end = self.app_state.notification_enabled_discord_end

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
        enable_start_checkbutton = ttk.Checkbutton(labelframe,
                                                   text="Start",
                                                   variable=self.enabled_notify_windows_start,
                                                   command=self.app_model.set_enabled_notify_windows_start)

        # End
        enable_end_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="End",
                                                 variable=self.enabled_notify_windows_end,
                                                 command=self.app_model.set_enabled_notify_windows_end)

        # Test
        test_button = ttk.Button(labelframe,
                                 text="Test",
                                 command=self.app_model.test_windows_notification)

        # Layout
        enable_start_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4)
        enable_end_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=8)
        test_button.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def build_discord_notification(self) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text="Discord Notification")

        # Start
        enable_start_checkbutton = ttk.Checkbutton(labelframe,
                                                   text="Start",
                                                   variable=self.enabled_notify_discord_start,
                                                   command=self.app_model.set_enabled_notify_discord_start)

        # End
        enable_end_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="End",
                                                 variable=self.enabled_notify_discord_end,
                                                 command=self.app_model.set_enabled_notify_discord_end)

        # Test
        test_button = ttk.Button(labelframe,
                                 text="Test",
                                 command=self.app_model.test_discord_notification)
        # Layout
        enable_start_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4)
        enable_end_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=8)
        test_button.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4, pady=4)

        return labelframe
