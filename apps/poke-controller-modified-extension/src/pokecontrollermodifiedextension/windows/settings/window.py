import logging
import tkinter as tk
from dataclasses import fields, is_dataclass
from typing import Any

from ... import widgets
from ...mixins import AppAccessorMixIn
from ...widgets.app import AppDialog, AppFrame
from .buttons import SettingsButtonsPane
from .contents import (
    CaptureSettingsPane,
    CommandSettingsPane,
    DeviceSettingsPane,
    ExternalSettingsPane,
    GeneralSettingsPane,
    NotificationSettingsPane,
    SerialSettingsPane,
    WidgetSettingsPane,
)
from .sidebar import SettingsSidebarPane

logger = logging.getLogger(__name__)


class SettingsWindow(AppDialog):
    _backup: dict[str, Any]
    _has_changes: tk.BooleanVar
    _content_labelframe: widgets.Labelframe
    _contents: dict[str, AppFrame]
    _current_content: AppFrame | None

    def __init__(
        self,
        master: AppAccessorMixIn,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, *args, **kwargs)

        self._settings = self.app.settings
        self._backup = self._settings.to_dict()

        self._has_changes = tk.BooleanVar(value=False)
        self._register_hooks()
        self.minsize(width=800, height=600)

        self._contents = {}
        self._current_content = None

        self.build_ui()

    def build_ui(self) -> None:
        upper_frame = widgets.Frame(self)

        # Sidebar
        sidebar = self._build_sidebar(master=upper_frame)

        # Content
        self._build_contents(master=upper_frame)

        lower_frame = widgets.Frame(self)
        buttons = SettingsButtonsPane(
            lower_frame,
            self._has_changes,
            self._on_ok_pushed,
            self._on_apply_pushed,
            self._on_cancel_pushed,
        )

        # Layout
        sidebar.pack(expand=False, fill=tk.Y, side=tk.LEFT, padx=(0, 4), pady=(4, 0))
        self._content_labelframe.pack(
            expand=True, fill=tk.BOTH, side=tk.LEFT, padx=(0, 8), pady=(8, 0)
        )
        buttons.pack(fill=tk.X)
        upper_frame.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)
        lower_frame.pack(expand=False, fill=tk.X, anchor=tk.CENTER)

        # Select first section
        sidebar.select_section("general", "General")

    def _build_sidebar(self, master: widgets.Frame) -> SettingsSidebarPane:
        sidebar = SettingsSidebarPane(
            master,
            self._on_section_selected,
        )

        sidebar.add_section("general", "General")
        sidebar.add_section("capture", "Capture")
        sidebar.add_section("serial", "Serial")
        sidebar.add_section("device", "Device")
        sidebar.add_section("command", "Command")
        sidebar.add_section("notification", "Notification")
        sidebar.add_section("widget", "Widget")
        sidebar.add_section("external", "External")

        return sidebar

    def _build_contents(self, master: widgets.Frame) -> None:
        self._content_labelframe = widgets.Labelframe(master)
        self._contents["general"] = GeneralSettingsPane(self._content_labelframe)
        self._contents["capture"] = CaptureSettingsPane(self._content_labelframe)
        self._contents["serial"] = SerialSettingsPane(self._content_labelframe)
        self._contents["device"] = DeviceSettingsPane(self._content_labelframe)
        self._contents["command"] = CommandSettingsPane(self._content_labelframe)
        self._contents["notification"] = NotificationSettingsPane(
            self._content_labelframe
        )
        self._contents["widget"] = WidgetSettingsPane(self._content_labelframe)
        self._contents["external"] = ExternalSettingsPane(self._content_labelframe)

    def _save_settings(self) -> None:
        logger.info("Settings saving.")
        self._settings.general.version.set(self.app.app_info.latest_settings_version)
        self.app.papico.save_settings(self.app.settings)
        logger.info("Settings saved.")

    def _check_has_changes(self) -> None:
        self._has_changes.set(self._settings.has_diff(self._backup))

    def _backup_settings(self) -> None:
        self._backup = self._settings.to_dict()

    def _revert_settings(self) -> None:
        show_realtime = self._settings.capture.show_realtime
        if show_realtime.get():
            show_realtime.set(False)
            self.update_idletasks()
        self._settings.apply_dict(self._backup)

    def _on_ok_pushed(self) -> None:
        self._save_settings()
        self.destroy()

    def _on_apply_pushed(self) -> None:
        self._save_settings()
        self._backup_settings()
        self._check_has_changes()

    def _on_cancel_pushed(self) -> None:
        self._revert_settings()
        self.destroy()

    def _register_hooks(self) -> None:
        def add_hook(current: Any) -> None:
            if isinstance(current, tk.Variable):
                self.register_trace(
                    "write",
                    current,
                    self._on_settings_changed,
                )
                return

            if isinstance(current, dict):
                for v in current.values():
                    add_hook(v)
                return

            if not is_dataclass(current):
                raise ValueError(f"unsupported type: {type(current)}")

            for field in fields(current):
                v = getattr(current, field.name)
                add_hook(v)

        add_hook(self._settings)

    def destroy(self) -> None:
        if self._has_changes.get():
            self._revert_settings()
        logger.debug("SettingsWindow destroyed.")
        super().destroy()

    def _on_settings_changed(self, *_: Any) -> None:
        self._check_has_changes()

    def _on_section_selected(self, section_id: str, section_name: str) -> None:
        self._content_labelframe.configure(text=f"{section_name} Settings")
        if (content := self._current_content) is not None:
            content.pack_forget()
        self._current_content = self._contents[section_id]
        self._current_content.pack(expand=True, fill=tk.BOTH, padx=4, pady=4)
        self._current_content.refresh()
        self._content_labelframe.update_idletasks()
