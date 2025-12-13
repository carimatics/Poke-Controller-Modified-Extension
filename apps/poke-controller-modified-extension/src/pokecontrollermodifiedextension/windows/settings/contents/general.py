import logging
import tkinter as tk
from typing import Any

from ....widgets.app import AppFrame
from .dynamic_input import DynamicInputsBuilder

logger = logging.getLogger(__name__)


class GeneralSettingsPane(AppFrame):
    _current_version: tk.StringVar

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._current_version = self.app.settings.general.version
        self._latest_settings_version = self.app.app_info.latest_settings_version

        self._style_manager = self.app.style_manager
        self._theme = self.app.settings.general.theme
        self._language = self.app.settings.general.language

        self.build_ui()

    def build_ui(self) -> None:
        frame = (
            DynamicInputsBuilder(self, label_width=16)
            .add_label_row("Version:", self._current_version)
            .add_combobox_row(
                "Theme:", self._theme, values=list(self._style_manager.get_themes())
            )
            .add_combobox_row("Language:", self._language, values=["ja", "en"])
            .build()
        )
        frame.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)
