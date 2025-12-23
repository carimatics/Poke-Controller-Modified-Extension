import logging
import tkinter as tk
from typing import Any, Callable

from pokecontrollermodifiedextension.state.settings import get_app_settings
from pokecontrollermodifiedextension.widgets.frame import Frame
from pokecontrollermodifiedextension.widgets.scrollable_frame import ScrollableFrame

logger = logging.getLogger(__name__)


class SettingsSidebarPane(Frame):
    _scrollable_frame: ScrollableFrame
    _current_button: tk.Button | None
    _section_buttons: dict[str, tk.Button]

    def __init__(
        self,
        master: tk.Misc,
        on_section_selected: Callable[[str, str], None],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self._on_section_selected = on_section_selected

        self._settings = get_app_settings()

        self.build_ui()

    def build_ui(self) -> None:
        self._scrollable_frame = ScrollableFrame(self, width=160)
        self._scrollable_frame.pack(expand=True, fill=tk.BOTH)

        self._current_button: tk.Button | None = None
        self._section_buttons: dict[str, tk.Button] = {}

    def add_section(self, section_id: str, section_name: str) -> None:
        bg_color = self._scrollable_frame._canvas.cget("background")
        btn = tk.Button(
            self._scrollable_frame.scrollable_frame,
            text=section_name,
            bg=bg_color,
            highlightbackground=bg_color,
            fg="black",
            activebackground="#e6e6e6",
            relief=tk.FLAT,
            anchor=tk.W,
            padx=4,
            pady=4,
            command=lambda: self._on_section_pushed(section_id, section_name),
        )
        btn.pack(fill=tk.X, padx=5, pady=1)
        self._section_buttons[section_id] = btn
        self._scrollable_frame.refresh()

    def select_section(self, section_id: str, section_name: str) -> None:
        bg_color = self._scrollable_frame._canvas.cget("background")
        if self._current_button is not None:
            self._current_button.configure(bg=bg_color, fg="black", state=tk.NORMAL)
        self._current_button = self._section_buttons[section_id]
        self._current_button.configure(bg=bg_color, fg="#6e6e6e", state=tk.DISABLED)

        self._on_section_selected(section_id, section_name)

    def _on_section_pushed(self, section_id: str, section_name: str) -> None:
        self.select_section(section_id, section_name)
