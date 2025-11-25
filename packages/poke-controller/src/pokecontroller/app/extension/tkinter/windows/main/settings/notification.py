import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable

from ....components import AppFrame
from ....values import literals as l


class NotificationSettings(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._enabled_windows_started = self.app_state.notification_enabled_notify_windows_when_command_started
        self._enabled_windows_ended = self.app_state.notification_enabled_notify_windows_when_command_ended
        self._enabled_discord_started = self.app_state.notification_enabled_notify_discord_when_command_started
        self._enabled_discord_ended = self.app_state.notification_enabled_notify_discord_when_command_ended

        self.build_ui()

    def build_ui(self):
        windows_notification = self._build_windows_notification()
        discord_notification = self._build_discord_notification()

        # Layout
        windows_notification.pack(expand=False, fill=l.NONE, anchor=l.NE, side=l.LEFT, padx=4)
        discord_notification.pack(expand=False, fill=l.NONE, anchor=l.NE, side=l.LEFT, padx=8)

    def _build_windows_notification(self) -> ttk.Labelframe:
        return self._build_notification(platform="Windows",
                                        enabled_started=self._enabled_windows_started.container,
                                        enabled_ended=self._enabled_windows_ended.container,
                                        on_enabled_started_changed=self._on_windows_start_changed,
                                        on_enabled_ended_changed=self._on_windows_end_changed,
                                        on_test_pushed=self._on_windows_test_pushed)

    def _build_discord_notification(self) -> ttk.Labelframe:
        return self._build_notification(platform="Discord",
                                        enabled_started=self._enabled_discord_started.container,
                                        enabled_ended=self._enabled_discord_ended.container,
                                        on_enabled_started_changed=self._on_discord_start_changed,
                                        on_enabled_ended_changed=self._on_discord_end_changed,
                                        on_test_pushed=self._on_discord_test_pushed)

    def _build_notification(self,
                            platform: str,
                            enabled_started: tk.BooleanVar,
                            enabled_ended: tk.BooleanVar,
                            on_enabled_started_changed: Callable[[], None],
                            on_enabled_ended_changed: Callable[[], None],
                            on_test_pushed: Callable[[], None]) -> ttk.Labelframe:
        labelframe = ttk.Labelframe(self, text=f"{platform} Notification")

        # Start
        enable_start_checkbutton = ttk.Checkbutton(labelframe,
                                                   text="Start",
                                                   variable=enabled_started,
                                                   command=on_enabled_started_changed)

        # End
        enable_end_checkbutton = ttk.Checkbutton(labelframe,
                                                 text="End",
                                                 variable=enabled_ended,
                                                 command=on_enabled_ended_changed)

        # Test
        test_button = ttk.Button(labelframe,
                                 text="Test",
                                 command=on_test_pushed)

        # Layout
        enable_start_checkbutton.pack(expand=False, fill=l.NONE, side=l.LEFT, padx=4)
        enable_end_checkbutton.pack(expand=False, fill=l.NONE, side=l.LEFT, padx=8)
        test_button.pack(expand=False, fill=l.NONE, side=l.LEFT, padx=4, pady=4)

        return labelframe

    def _on_windows_start_changed(self):
        self.app_model.apply_enabled_notify_windows_when_command_started()

    def _on_windows_end_changed(self):
        self.app_model.apply_enabled_notify_windows_when_command_ended()

    def _on_windows_test_pushed(self):
        self.app_model.notify_windows_force()

    def _on_discord_start_changed(self):
        self.app_model.apply_enabled_notify_discord_when_command_started()

    def _on_discord_end_changed(self):
        self.app_model.apply_enabled_notify_discord_when_command_ended()

    def _on_discord_test_pushed(self):
        self.app_model.notify_discord_force()
