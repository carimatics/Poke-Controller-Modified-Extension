import logging
import tkinter as tk
import webbrowser
from typing import Any

from pokecontrollerext.core.settings import DEFAULT
from pokecontrollerext.singletons.app.settings import get_app_settings
from pokecontrollerext.singletons.widget.catalog import (
    get_app_widget_catalog,
)
from pokecontrollerext.windows import SettingsWindow
from pokecontrollerext.windows.changelogs.window import ChangelogWindow
from pokecontrollerext.windows.discord.window import DiscordSettingsWindow
from pokecontrollerext.windows.new_profile.window import NewProfileWindow
from pokecontrollerext.windows.question.window import QuestionWindow
from pokecontrollerext.windows.version.window import VersionWindow

logger = logging.getLogger(__name__)

GITHUB_URL = "https://github.com/futo030/Poke-Controller-Modified-Extension"
POKECONTROLLER_GUIDE_URL = "https://pokecontroller.info/"
WEBBROWSER_OPEN_IN_NEW_TAB = 2


class Menu(tk.Menu):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self._app_settings = get_app_settings()
        self._widget_catalog = get_app_widget_catalog()
        self.build_ui()

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
            label="Discord",
            command=self._on_command_discord_settings_pushed,
        )
        command_cascade.add_separator()
        command_cascade.add_command(
            label="新規プロファイル作成",
            command=self._on_command_new_profile_pushed,
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
            command=self._on_help_changelog_pushed,
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
        self._widget_catalog.window.open_settings(self, SettingsWindow)

    def _on_menu_reset_window_size_pushed(self) -> None:
        self._app_settings.capture.size.set(DEFAULT["capture"]["size"])

    def _on_command_discord_settings_pushed(self) -> None:
        self._widget_catalog.window.open_discord_settings(self, DiscordSettingsWindow)

    def _on_command_new_profile_pushed(self) -> None:
        self._widget_catalog.window.open_new_profile(self, NewProfileWindow)

    def _on_command_key_config_pushed(self) -> None:
        pass

    # noinspection PyMethodMayBeStatic
    def _on_help_github_pushed(self) -> None:
        webbrowser.open(url=GITHUB_URL, new=WEBBROWSER_OPEN_IN_NEW_TAB)

    # noinspection PyMethodMayBeStatic
    def _on_help_guide_pushed(self) -> None:
        webbrowser.open(url=POKECONTROLLER_GUIDE_URL, new=WEBBROWSER_OPEN_IN_NEW_TAB)

    def _on_help_question_template_pushed(self) -> None:
        self._widget_catalog.window.open_question(self, QuestionWindow)

    def _on_help_version_pushed(self) -> None:
        self._widget_catalog.window.open_version(self, VersionWindow)

    def _on_help_changelog_pushed(self) -> None:
        self._widget_catalog.window.open_changelog(self, ChangelogWindow)

    def _on_help_check_for_update_pushed(self) -> None:
        pass

    def _on_help_license_pushed(self) -> None:
        pass
