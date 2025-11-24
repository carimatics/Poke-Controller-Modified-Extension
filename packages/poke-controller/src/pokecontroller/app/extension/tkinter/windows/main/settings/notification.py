import tkinter as tk
import tkinter.ttk as ttk

from ....components import AppFrame


class NotificationSettings(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.enabled_windows_started = self.app_state.notification_enabled_notify_windows_when_command_started
        self.enabled_windows_ended = self.app_state.notification_enabled_notify_windows_when_command_ended
        self.enabled_discord_started = self.app_state.notification_enabled_notify_discord_when_command_started
        self.enabled_discord_ended = self.app_state.notification_enabled_notify_discord_when_command_ended

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
                                                   variable=self.enabled_windows_started,
                                                   command=self.app_model.apply_enabled_notify_windows_when_command_started)

        # End
        enable_end_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="End",
                                                 variable=self.enabled_windows_ended,
                                                 command=self.app_model.apply_enabled_notify_windows_when_command_ended)

        # Test
        test_button = ttk.Button(labelframe,
                                 text="Test",
                                 command=self.app_model.notify_windows_force)

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
                                                   variable=self.enabled_discord_started,
                                                   command=self.app_model.apply_enabled_notify_discord_when_command_started)

        # End
        enable_end_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="End",
                                                 variable=self.enabled_discord_ended,
                                                 command=self.app_model.apply_enabled_notify_discord_when_command_ended)

        # Test
        test_button = ttk.Button(labelframe,
                                 text="Test",
                                 command=self.app_model.notify_discord_force)
        # Layout
        enable_start_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4)
        enable_end_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=8)
        test_button.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4, pady=4)

        return labelframe
