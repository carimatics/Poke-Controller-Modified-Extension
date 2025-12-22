import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Self, overload

from pokecontrollermodifiedextension.mixins import AppAccessorMixIn
from pokecontrollermodifiedextension.state.settings import get_app_settings
from pokecontrollermodifiedextension.widgets.app.dialog import AppDialog
from pokecontrollermodifiedextension.widgets.components.dynamic_form import (
    DynamicForm,
    DynamicFormItem,
)


class DynamicFormDialog(AppDialog):
    _form: DynamicForm
    _is_ok: bool
    _items: list[DynamicFormItem]

    def __init__(
        self,
        master: AppAccessorMixIn,
        title: str,
        items: list[DynamicFormItem],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self._is_ok = False
        self._items = items
        self._app_settings = get_app_settings()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.title(title)
        self.build_ui()
        self.master.wait_window(self)

    def build_ui(self) -> None:
        confirm_button_position = (
            self._app_settings.widget.dialog.confirm_buttons_position.get()
        )

        frame = tk.Frame(self)
        if confirm_button_position in ["top", "both"]:
            self._build_confirm_button(frame)
        self._form = DynamicForm(frame, self._items)
        self._form.pack(expand=True, fill=tk.BOTH)
        if confirm_button_position in ["bottom", "both"]:
            self._build_confirm_button(frame)
        frame.pack(expand=True, fill=tk.BOTH)

    def as_dict(self) -> dict[str, bool | int | float | str] | None:
        if not self._is_ok:
            return None
        return self._form.as_dict()

    def _build_confirm_button(
        self,
        master: tk.Frame,
    ) -> None:
        frame = tk.Frame(master)
        ok_button = ttk.Button(
            frame,
            text="OK",
            command=self._on_ok_pressed,
        )
        cancel_button = ttk.Button(
            frame,
            text="Cancel",
            command=self._on_cancel_pressed,
        )

        ok_button.pack(
            expand=True,
            side=tk.LEFT,
            fill=tk.BOTH,
            anchor=tk.CENTER,
            padx=5,
            pady=5,
        )
        cancel_button.pack(
            expand=True,
            side=tk.LEFT,
            fill=tk.BOTH,
            anchor=tk.CENTER,
            padx=5,
            pady=5,
        )
        frame.pack(
            expand=True,
            side=tk.TOP,
            fill=tk.BOTH,
            anchor=tk.CENTER,
            padx=5,
            pady=5,
        )

    def _on_close(self) -> None:
        self.destroy()
        self._is_ok = False

    def _on_ok_pressed(self) -> None:
        self.destroy()
        self._is_ok = True

    def _on_cancel_pressed(self) -> None:
        self.destroy()
        self._is_ok = False


class DynamicFormDialogBuilder:
    def __init__(self, master: AppAccessorMixIn, title: str) -> None:
        self.master = master
        self.title = title
        self.items: list[DynamicFormItem] = []

    def build(self) -> DynamicFormDialog:
        return DynamicFormDialog(self.master, self.title, self.items)

    def add_checkbutton_row(self, name: str, text: str, initial_value: bool) -> Self:
        variable = tk.BooleanVar(value=initial_value)
        self.items.append(
            DynamicFormItem(
                name=name,
                variable=variable,
                widget="checkbutton",
                kwargs={"text": text},
            )
        )
        return self

    def add_combobox_row(
        self,
        name: str,
        initial_value: str,
        values: list[str],
    ) -> Self:
        variable = tk.StringVar(value=initial_value)
        self.items.append(
            DynamicFormItem(
                name=name,
                variable=variable,
                widget="combobox",
                kwargs={
                    "values": values,
                },
            )
        )
        return self

    def add_entry_row(self, name: str, initial_value: str) -> Self:
        variable = tk.StringVar(value=initial_value)
        self.items.append(
            DynamicFormItem(
                name=name,
                variable=variable,
                widget="entry",
            )
        )
        return self

    def add_radiobutton_row(
        self,
        name: str,
        initial_value: str,
        values: list[str],
    ) -> Self:
        variable = tk.StringVar(value=initial_value)
        self.items.append(
            DynamicFormItem(
                name=name,
                variable=variable,
                widget="radiobutton",
                kwargs={
                    "values": values,
                },
            )
        )
        return self

    def add_spinbox_row(
        self,
        name: str,
        initial_value: str,
        values: list[str],
    ) -> Self:
        variable = tk.StringVar(value=initial_value)
        self.items.append(
            DynamicFormItem(
                name=name,
                variable=variable,
                widget="spinbox",
                kwargs={
                    "values": values,
                },
            )
        )
        return self

    @overload
    def add_scale_row(
        self, name: str, initial_value: int, to: int, from_: int
    ) -> Self: ...

    @overload
    def add_scale_row(
        self, name: str, initial_value: float, to: float, from_: float
    ) -> Self: ...

    def add_scale_row(
        self,
        name: str,
        initial_value: int | float,
        to: int | float,
        from_: int | float,
    ) -> Self:
        if isinstance(initial_value, int):
            variable: tk.Variable = tk.IntVar(value=initial_value)
        else:
            variable = tk.DoubleVar(value=initial_value)
        self.items.append(
            DynamicFormItem(
                name=name,
                variable=variable,
                widget="scale",
                kwargs={
                    "to": to,
                    "from_": from_,
                },
            )
        )
        return self
