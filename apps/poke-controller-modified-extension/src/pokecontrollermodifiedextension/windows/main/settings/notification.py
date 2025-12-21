import tkinter as tk
from typing import Any, Callable

from pokecontrollermodifiedextension import widgets
from pokecontrollermodifiedextension.core.model import get_app_model
from pokecontrollermodifiedextension.core.settings import get_app_settings
from pokecontrollermodifiedextension.translation import t
from pokecontrollermodifiedextension.widgets.app import AppFrame


class NotificationSettings(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._app_settings = get_app_settings()
        self._app_model = get_app_model()

        self._enabled_windows_started = (
            self._app_settings.notification.line.enabled_started
        )
        self._enabled_windows_ended = self._app_settings.notification.line.enabled_ended
        self._enabled_discord_started = (
            self._app_settings.notification.discord.enabled_started
        )
        self._enabled_discord_ended = (
            self._app_settings.notification.discord.enabled_ended
        )

        self.build_ui()

    def build_ui(self) -> None:
        desktop_notification = self._build_desktop_notification()
        discord_notification = self._build_discord_notification()

        # Layout
        desktop_notification.pack(
            expand=False,
            fill=tk.NONE,
            anchor=tk.NE,
            side=tk.LEFT,
            padx=4,
        )
        discord_notification.pack(
            expand=False,
            fill=tk.NONE,
            anchor=tk.NE,
            side=tk.LEFT,
            padx=8,
        )

    def _build_desktop_notification(self) -> widgets.Labelframe:
        return self._build_notification(
            platform="desktop",
            enabled_started=self._enabled_windows_started,
            enabled_ended=self._enabled_windows_ended,
            on_enabled_started_changed=self._on_windows_start_changed,
            on_enabled_ended_changed=self._on_windows_end_changed,
            on_test_pushed=self._on_desktop_test_pushed,
        )

    def _build_discord_notification(self) -> widgets.Labelframe:
        return self._build_notification(
            platform="discord",
            enabled_started=self._enabled_discord_started,
            enabled_ended=self._enabled_discord_ended,
            on_enabled_started_changed=self._on_discord_start_changed,
            on_enabled_ended_changed=self._on_discord_end_changed,
            on_test_pushed=self._on_discord_test_pushed,
        )

    def _build_notification(
        self,
        platform: str,
        enabled_started: tk.BooleanVar,
        enabled_ended: tk.BooleanVar,
        on_enabled_started_changed: Callable[[], None],
        on_enabled_ended_changed: Callable[[], None],
        on_test_pushed: Callable[[], None],
    ) -> widgets.Labelframe:
        labelframe = widgets.Labelframe(
            self,
            text=t(f"main.settings.notification.{platform}.title"),
        )

        # Start
        enable_start_checkbutton = widgets.Checkbutton(
            labelframe,
            text=t(f"main.settings.notification.{platform}.start"),
            tooltip=t(f"main.settings.notification.{platform}.start.tooltip"),
            variable=enabled_started,
            command=on_enabled_started_changed,
        )

        # End
        enable_end_checkbutton = widgets.Checkbutton(
            labelframe,
            text=t(f"main.settings.notification.{platform}.end"),
            tooltip=t(f"main.settings.notification.{platform}.end.tooltip"),
            variable=enabled_ended,
            command=on_enabled_ended_changed,
        )

        # Test
        test_button = widgets.Button(
            labelframe,
            text=t(f"main.settings.notification.{platform}.test"),
            tooltip=t(f"main.settings.notification.{platform}.test.tooltip"),
            command=on_test_pushed,
        )

        # Layout
        enable_start_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4)
        enable_end_checkbutton.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=8)
        test_button.pack(expand=False, fill=tk.NONE, side=tk.LEFT, padx=4, pady=4)

        return labelframe

    def _on_windows_start_changed(self) -> None:
        self._app_model.apply_enabled_notify_windows_when_command_started()

    def _on_windows_end_changed(self) -> None:
        self._app_model.apply_enabled_notify_windows_when_command_ended()

    def _on_desktop_test_pushed(self) -> None:
        self._app_model.notify_desktop(message="Notification Test")

    def _on_discord_start_changed(self) -> None:
        self._app_model.apply_enabled_notify_discord_when_command_started()

    def _on_discord_end_changed(self) -> None:
        self._app_model.apply_enabled_notify_discord_when_command_ended()

    def _on_discord_test_pushed(self) -> None:
        self._app_model.notify_discord(message="Notification Test")
