import logging
import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import fields, is_dataclass
from typing import Any

from ...mixins import AppAccessorMixIn
from ...values import literals as l
from ...widgets import AppDialog
from .buttons import SettingsButtonsPane
from .sidebar import SettingsSidebarPane

logger = logging.getLogger(__name__)


class SettingsWindow(AppDialog):
    _backup: dict[str, Any]
    _has_changes: tk.BooleanVar
    _trace_ids: list[tuple[tk.Variable, str]]

    def __init__(
        self,
        master: AppAccessorMixIn,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, *args, **kwargs)

        self._settings = self.app.settings
        self._backup = self._settings.to_dict()

        self._trace_ids = []
        self._has_changes = tk.BooleanVar(value=False)
        self._register_hooks()

        self.build_ui()

    def build_ui(self) -> None:
        upper_frame = ttk.Frame(self)
        sidebar = self._build_sidebar(master=upper_frame)
        labelframe = ttk.Labelframe(upper_frame, text="Foo")

        lower_frame = ttk.Frame(self)
        buttons = SettingsButtonsPane(
            lower_frame,
            self._has_changes,
            self._on_apply_pushed,
        )

        # Layout
        sidebar.pack(expand=False, fill=l.Y, side=l.LEFT, padx=(0, 4))
        labelframe.pack(expand=True, fill=l.BOTH, side=l.LEFT)
        buttons.pack(fill=l.X)
        upper_frame.pack(expand=True, fill=l.BOTH, anchor=l.CENTER)
        lower_frame.pack(expand=False, fill=l.X, anchor=l.CENTER)

    def _build_sidebar(self, master: ttk.Frame) -> SettingsSidebarPane:
        sidebar = SettingsSidebarPane(
            master,
            self._on_section_selected,
        )

        sidebar.add_section("general", "General")
        sidebar.add_section("capture", "Capture")
        sidebar.add_section("serial", "Serial")
        sidebar.add_section("device_input", "Device Input")
        sidebar.add_section("command", "Command")
        sidebar.add_section("notification", "Notification")
        sidebar.add_section("widget", "Widget")
        sidebar.add_section("external", "External Tools")

        return sidebar

    def _on_apply_pushed(self) -> None:
        logger.info("Settings saving.")
        # self.app.papico.save_settings(self.app.settings)
        logger.info("Settings saved.")

    def _register_hooks(self) -> None:
        def add_hook(current: Any) -> None:
            if isinstance(current, tk.Variable):
                self._trace_ids.append(
                    (current, current.trace_add("write", self._on_settings_changed))
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
        for var, trace_id in self._trace_ids:
            var.trace_remove("write", trace_id)
        logger.debug("SettingsWindow destroyed.")
        super().destroy()

    def _on_settings_changed(self, *_: Any) -> None:
        self._has_changes.set(
            self._settings.has_diff(self._backup),
        )

    def _on_section_selected(self, section: str) -> None:
        pass
