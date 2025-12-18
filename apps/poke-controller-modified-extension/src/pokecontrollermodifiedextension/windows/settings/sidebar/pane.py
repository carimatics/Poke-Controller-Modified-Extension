import logging
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Callable

from .... import widgets
from ....settings import get_app_settings
from ....widgets.app import AppFrame

logger = logging.getLogger(__name__)


class SettingsSidebarPane(AppFrame):
    _canvas: tk.Canvas
    _scrollable_frame: tk.Frame
    _scrollbar: widgets.Scrollbar
    _bg_color: str
    _canvas_window: int
    _current_button: tk.Button | None
    _section_buttons: dict[str, tk.Button]
    _hook_ids: list[str]

    def __init__(
        self,
        master: tk.Misc,
        on_section_selected: Callable[[str, str], None],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self._bg_color = self._get_parent_bg(master)
        logging.debug(f"Sidebar background color: {self._bg_color}")

        self._settings = get_app_settings()

        self._theme = self._settings.general.theme

        self._on_section_selected = on_section_selected
        self._hook_ids = []
        self._register_hooks()

        self.build_ui()

    def build_ui(self) -> None:
        self._canvas = tk.Canvas(
            self, bg=self._bg_color, width=140, highlightthickness=0
        )
        self._scrollbar = widgets.Scrollbar(
            self, orient="vertical", command=self._canvas.yview
        )
        self._scrollable_frame = tk.Frame(self._canvas, bg=self._bg_color)
        self._scrollable_frame.bind(
            "<Configure>",
            self._on_frame_configure,
        )

        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._scrollable_frame, anchor=tk.NW
        )
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._canvas.bind(
            "<Configure>",
            self._on_canvas_configure,
        )
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self._canvas.bind_all("<Button-4>", self._on_mouse_wheel)
        self._canvas.bind_all("<Button-5>", self._on_mouse_wheel)

        self._current_button: tk.Button | None = None
        self._section_buttons: dict[str, tk.Button] = {}

    def add_section(self, section_id: str, section_name: str) -> None:
        bg_color = self._canvas.cget("background")
        btn = tk.Button(
            self._scrollable_frame,
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

    def select_section(self, section_id: str, section_name: str) -> None:
        bg_color = self._canvas.cget("background")
        if self._current_button is not None:
            self._current_button.configure(bg=bg_color, fg="black", state=tk.NORMAL)
        self._current_button = self._section_buttons[section_id]
        self._current_button.configure(bg=bg_color, fg="#6e6e6e", state=tk.DISABLED)

        self._on_section_selected(section_id, section_name)

    def destroy(self) -> None:
        for trace_id in self._hook_ids:
            self._theme.trace_remove("write", trace_id)
        super().destroy()

    def _on_frame_configure(self, _: tk.Event) -> None:
        self._update_scroll_region()

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self._canvas.itemconfig(
            self._canvas_window,
            width=event.width,
        )
        self._update_scroll_region()

    def _update_scroll_region(self) -> None:
        self._canvas.update_idletasks()

        bbox = self._canvas.bbox("all")
        content_height = bbox[3] - bbox[1]
        canvas_height = self._canvas.winfo_height()

        if content_height > canvas_height:
            self._canvas.configure(scrollregion=bbox)
            self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self._canvas.configure(scrollregion=(0, 0, 0, canvas_height))
            self._canvas.yview_moveto(0)
            self._scrollbar.pack_forget()

    def _on_section_pushed(self, section_id: str, section_name: str) -> None:
        self.select_section(section_id, section_name)

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        bbox = self._canvas.bbox("all")
        if bbox and bbox[3] > self._canvas.winfo_height():
            if event.num == 5 or event.delta < 0:
                self._canvas.yview_scroll(1, "units")
            if event.num == 4 or event.delta > 0:
                self._canvas.yview_scroll(-1, "units")

    def _get_parent_bg(self, widget: tk.Misc) -> str:
        try:
            bg = None
            if isinstance(widget, (tk.Frame, tk.Tk, tk.Toplevel)):
                bg = widget.cget("background")
            elif isinstance(widget, widgets.Frame):
                style = ttk.Style(widget)
                bg = style.lookup("TFrame", "background")
            if bg:
                rgb = widget.winfo_rgb(bg)
                r, g, b = [x >> 8 for x in rgb]
                return f"#{r:02x}{g:02x}{b:02x}"
            logger.warning("Failed to get parent background color")
            return "#f0f0f0"
        except Exception:
            logger.exception("Failed to get parent background color")
            return "#f0f0f0"

    def _apply_theme(self, *_: Any) -> None:
        def apply() -> None:
            self._bg_color = self._get_parent_bg(self)
            self._canvas.configure(bg=self._bg_color)
            self._scrollable_frame.configure(bg=self._bg_color)
            for btn in self._section_buttons.values():
                btn.configure(bg=self._bg_color)

        self.after(10, apply)

    def _register_hooks(self) -> None:
        self._hook_ids.append(self._theme.trace_add("write", self._apply_theme))
