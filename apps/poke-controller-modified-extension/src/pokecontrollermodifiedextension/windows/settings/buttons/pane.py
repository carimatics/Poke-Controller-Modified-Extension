import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Callable

from ....values import literals as l
from ....widgets import AppFrame


class SettingsButtonsPane(AppFrame):
    _apply_button: ttk.Button
    _has_changes: tk.BooleanVar
    _on_apply_pushed: Callable[[], None]

    def __init__(
        self,
        master: tk.Misc,
        has_changes: tk.BooleanVar,
        on_apply_pushed: Callable[[], None],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self._has_changes = has_changes
        self._on_apply_pushed = on_apply_pushed
        self._register_hooks()
        self.build_ui()

    def build_ui(self) -> None:
        ok_button = ttk.Button(self, text="OK", command=self._on_ok_pushed)
        self._apply_button = ttk.Button(
            self,
            text="Apply",
            state=l.NORMAL if self._has_changes.get() else l.DISABLED,
            command=self._on_apply_pushed,
        )
        cancel_button = ttk.Button(self, text="Cancel", command=self._on_cancel_pushed)

        # Layout
        ok_button.pack(side=l.RIGHT, padx=(4, 0))
        self._apply_button.pack(side=l.RIGHT, padx=4)
        cancel_button.pack(side=l.RIGHT, padx=4)
        self.pack(expand=True, fill=l.X, padx=4, pady=4)

    def _on_ok_pushed(self) -> None:
        self._on_apply_pushed()
        self.master.destroy()

    def _on_cancel_pushed(self) -> None:
        self.master.destroy()

    def _register_hooks(self) -> None:
        self._has_changes.trace_add("write", self._on_has_changes_changed)

    def _on_has_changes_changed(self, *_: Any) -> None:
        if self._has_changes.get():
            self._apply_button.configure(state=l.NORMAL)
        else:
            self._apply_button.configure(state=l.DISABLED)
