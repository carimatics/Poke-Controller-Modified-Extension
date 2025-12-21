import logging
import tkinter as tk
import webbrowser
from typing import Any

from pokecontrollermodifiedextension.app import App
from pokecontrollermodifiedextension.core.settings import DEFAULT, get_app_settings
from pokecontrollermodifiedextension.mixins import AppAccessorMixIn
from pokecontrollermodifiedextension.windows import SettingsWindow

logger = logging.getLogger(__name__)

GITHUB_URL = "https://github.com/futo030/Poke-Controller-Modified-Extension"
POKECONTROLLER_GUIDE_URL = "https://pokecontroller.info/"
WEBBROWSER_OPEN_IN_NEW_TAB = 2


class AppMenu(tk.Menu, AppAccessorMixIn):
    _settings_window: SettingsWindow | None = None

    def __init__(self, master: App, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self._app: App = master
        self._app_settings = get_app_settings()
        self.build_ui()

    @property
    def app(self) -> App:
        return self._app

    def build_ui(self) -> None:
        self._build_menu_cascade()
        self._build_command_cascade()
        self._build_help_cascade()

    def _build_menu_cascade(self) -> None:
        menu_cascade = tk.Menu(self, tearoff=False)
        menu_cascade.add_separator()
        menu_cascade.add_command(
            label="設定",
            command=self._on_menu_settings_pushed,
        )
        menu_cascade.add_separator()
        menu_cascade.add_command(
            label="画面サイズのリセット",
            command=self._on_menu_reset_window_size_pushed,
        )
        self.add_cascade(menu=menu_cascade, label="メニュー")

    def _build_command_cascade(self) -> None:
        command_cascade = tk.Menu(self, tearoff=False)
        command_cascade.add_command(
            label="LINE",
            command=self._on_command_line_settings_pushed,
        )
        command_cascade.add_command(
            label="Discord",
            command=self._on_command_discord_settings_pushed,
        )
        command_cascade.add_separator()
        command_cascade.add_command(
            label="batファイル作成",
            command=self._on_command_bat_pushed,
        )
        command_cascade.add_command(
            label="プロファイル作成",
            command=self._on_command_profile_pushed,
        )
        command_cascade.add_separator()
        command_cascade.add_command(
            label="Pokémon HOME連携",
            command=self._on_command_pokemon_home_pushed,
        )
        command_cascade.add_separator()
        command_cascade.add_command(
            label="キーコンフィグ",
            command=self._on_command_key_config_pushed,
        )
        self.add_cascade(menu=command_cascade, label="コマンド")

    def _build_help_cascade(self) -> None:
        help_cascade = tk.Menu(self, tearoff=False)
        help_cascade.add_command(
            label="GitHub",
            command=self._on_help_github_pushed,
        )
        help_cascade.add_command(
            label="Poke-Controller Guide",
            command=self._on_help_guide_pushed,
        )
        help_cascade.add_separator()
        help_cascade.add_command(
            label="質問テンプレート",
            command=self._on_help_question_template_pushed,
        )
        help_cascade.add_separator()
        help_cascade.add_command(
            label="バージョン確認",
            command=self._on_help_version_pushed,
        )
        help_cascade.add_command(
            label="更新履歴表示",
            command=self._on_help_update_note_pushed,
        )
        help_cascade.add_command(
            label="アップデート確認",
            command=self._on_help_check_for_update_pushed,
        )
        help_cascade.add_command(
            label="ライセンス",
            command=self._on_help_license_pushed,
        )
        self.add_cascade(
            menu=help_cascade,
            label="ヘルプ",
        )

    def _on_menu_settings_pushed(self) -> None:
        if (window := self._settings_window) is not None:
            if window.winfo_exists():
                window.lift()
                return
        self._settings_window = SettingsWindow(self)
        self._settings_window.protocol(
            "WM_DELETE_WINDOW",
            self._on_settings_window_closed,
        )

    def _on_menu_reset_window_size_pushed(self) -> None:
        self._app_settings.capture.size.set(DEFAULT["capture"]["size"])

    def _on_command_line_settings_pushed(self) -> None:
        pass

    def _on_command_discord_settings_pushed(self) -> None:
        pass

    def _on_command_bat_pushed(self) -> None:
        pass

    def _on_command_profile_pushed(self) -> None:
        pass

    def _on_command_pokemon_home_pushed(self) -> None:
        pass

    def _on_command_key_config_pushed(self) -> None:
        pass

    # noinspection PyMethodMayBeStatic
    def _on_help_github_pushed(self) -> None:
        webbrowser.open(url=GITHUB_URL, new=WEBBROWSER_OPEN_IN_NEW_TAB)

    # noinspection PyMethodMayBeStatic
    def _on_help_guide_pushed(self) -> None:
        webbrowser.open(url=POKECONTROLLER_GUIDE_URL, new=WEBBROWSER_OPEN_IN_NEW_TAB)

    def _on_help_question_template_pushed(self) -> None:
        pass

    def _on_help_version_pushed(self) -> None:
        pass

    def _on_help_update_note_pushed(self) -> None:
        pass

    def _on_help_check_for_update_pushed(self) -> None:
        pass

    def _on_help_license_pushed(self) -> None:
        pass

    def _on_settings_window_closed(self) -> None:
        logger.info("Settings window closed.")
        if (window := self._settings_window) is None:
            return
        if window.winfo_exists():
            window.destroy()
        self._settings_window = None
