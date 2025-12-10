import logging
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any

from ....style import get_themes
from ....widgets import AppFrame

logger = logging.getLogger(__name__)


class GeneralSettingsPane(AppFrame):
    _current_version: tk.StringVar

    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._current_version = self.app.settings.general.version
        self._latest_settings_version = self.app.app_info.latest_settings_version

        self._theme = self.app.settings.general.theme
        self._language = self.app.settings.general.language

        self.build_ui()

    def build_ui(self) -> None:
        frame = ttk.Frame(self)

        # settings version
        version_frame = ttk.Frame(frame)
        version_label = ttk.Label(version_frame, width=16, text="Settings Version:")
        version_value = ttk.Label(version_frame, textvariable=self._current_version)

        # theme
        theme_frame = ttk.Frame(frame)
        theme_label = ttk.Label(theme_frame, width=16, text="Theme:")
        theme_combobox = ttk.Combobox(
            theme_frame, textvariable=self._theme, values=get_themes()
        )

        # language
        language_frame = ttk.Frame(frame)
        language_label = ttk.Label(language_frame, width=16, text="Language:")
        language_combobox = ttk.Combobox(
            language_frame, textvariable=self._language, values=["ja", "en"]
        )
        language_caption = ttk.Label(language_frame, text="(Restart required)")

        # Layout
        version_label.pack(side=tk.LEFT)
        version_value.pack(side=tk.LEFT, padx=4)
        version_frame.pack(expand=False, fill=tk.X)

        theme_label.pack(side=tk.LEFT)
        theme_combobox.pack(side=tk.LEFT, padx=4)
        theme_frame.pack(expand=False, fill=tk.X, pady=(8, 0))

        language_label.pack(side=tk.LEFT)
        language_combobox.pack(side=tk.LEFT, padx=4)
        language_caption.pack(side=tk.LEFT, padx=4)
        language_frame.pack(expand=False, fill=tk.X, pady=(8, 0))

        frame.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)
