import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass, field
from typing import Any, Literal, Self, overload

from ...mixins import AppAccessorMixIn
from ...values import literals as l
from ..dialog import AppDialog

type WidgetType = Literal[
    "checkbutton",
    "combobox",
    "entry",
    "radiobutton",
    "spinbox",
    "scale",
]


@dataclass
class DynamicFormItem:
    widget: WidgetType
    name: str
    value: int | float | bool | str
    kwargs: dict[str, Any] = field(default_factory=dict)


class DynamicForm(AppDialog):
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
        self._variables: dict[str, tk.Variable] = {}
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.title(title)
        self.build_ui()
        self.master.wait_window(self)

    def build_ui(self) -> None:
        confirm_button_position = (
            self.app.gui_state.widget.dialog.confirm_buttons_position.get()
        )

        frame = tk.Frame(self)
        if confirm_button_position in ["top", "both"]:
            self._build_confirm_button(frame)
        for item in self._items:
            self._build_dynamic_widgets(frame, item)
        if confirm_button_position in ["bottom", "both"]:
            self._build_confirm_button(frame)
        frame.pack(expand=True, fill=l.BOTH)

    def as_dict(self) -> dict[str, bool | int | float | str] | None:
        if not self._is_ok:
            return None
        return {name: var.get() for name, var in self._variables.items()}

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
            side=l.LEFT,
            fill=l.BOTH,
            anchor=l.CENTER,
            padx=5,
            pady=5,
        )
        cancel_button.pack(
            expand=True,
            side=l.LEFT,
            fill=l.BOTH,
            anchor=l.CENTER,
            padx=5,
            pady=5,
        )
        frame.pack(
            expand=True,
            side=l.TOP,
            fill=l.BOTH,
            anchor=l.CENTER,
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

    def _build_dynamic_widgets(self, master: tk.Frame, item: DynamicFormItem) -> None:
        labelframe = ttk.LabelFrame(master, text=item.name, padding=(5, 5))
        match item:
            case DynamicFormItem(
                widget="checkbutton",
                name=str(name),
                value=bool(value),
                kwargs=checkbutton_kwargs,
            ):
                variable: tk.Variable = tk.BooleanVar(value=value)
                self._variables[name] = variable
                widget: tk.Widget = ttk.Checkbutton(
                    labelframe,
                    variable=variable,
                    **checkbutton_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="combobox",
                name=str(name),
                value=str(value),
                kwargs=checkbox_kwargs,
            ):
                variable = tk.StringVar(value=value)
                self._variables[name] = variable
                widget = ttk.Combobox(
                    labelframe,
                    textvariable=variable,
                    **checkbox_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="entry",
                name=str(name),
                value=str(value),
                kwargs=entry_kwargs,
            ):
                variable = tk.StringVar(value=value)
                self._variables[name] = variable
                widget = ttk.Entry(
                    labelframe,
                    textvariable=variable,
                    **entry_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="radiobutton",
                name=str(name),
                value=str(value),
                kwargs={"values": values, **radiobutton_kwargs},
            ):
                variable = tk.StringVar(value=value)
                self._variables[name] = variable
                for column_index, value in enumerate(values):
                    radio = ttk.Radiobutton(
                        labelframe,
                        text=value,
                        variable=variable,
                        value=value,
                        **radiobutton_kwargs,
                    )
                    radio.pack(
                        expand=True,
                        side=l.LEFT,
                        fill=l.BOTH,
                        anchor=l.CENTER,
                        padx=3,
                        pady=3,
                    )
            case DynamicFormItem(
                widget="spinbox",
                name=str(name),
                value=str(value),
                kwargs=spinbox_kwargs,
            ):
                variable = tk.StringVar(value=value)
                self._variables[name] = variable
                widget = ttk.Spinbox(
                    labelframe,
                    textvariable=variable,
                    **spinbox_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="scale",
                name=str(name),
                value=int(value),
                kwargs={
                    "to": int(to),
                    "from_": int(from_),
                    **int_scale_kwargs,
                },
            ):
                variable = tk.IntVar(value=value)
                self._variables[name] = variable
                label = ttk.Label(labelframe, text=variable.get())
                variable.trace(
                    "w", lambda *_: label.configure(text=int(variable.get()))
                )
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                )
                widget = ttk.Scale(
                    labelframe,
                    value=value,
                    variable=variable,
                    to=to,
                    from_=from_,
                    **int_scale_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="scale",
                name=str(name),
                value=float(value),
                kwargs={
                    "to": float(to),
                    "from_": float(from_),
                    **float_scale_kwargs,
                },
            ):
                variable = tk.DoubleVar(value=value)
                self._variables[name] = variable
                label = ttk.Label(labelframe, text=f"{variable.get():.2f}")
                variable.trace(
                    "w", lambda *_: label.configure(text=f"{variable.get():.2f}")
                )
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                )
                widget = ttk.Scale(
                    labelframe,
                    value=value,
                    variable=variable,
                    to=to,
                    from_=from_,
                    **float_scale_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                    padx=3,
                    pady=3,
                )
            case _:
                raise ValueError(f"Unsupported widget: {item}")
        labelframe.pack(expand=False, side=l.TOP, fill=l.BOTH, padx=5, pady=5)


class DynamicFormBuilder:
    def __init__(self, master: AppAccessorMixIn, title: str) -> None:
        self.master = master
        self.title = title
        self.items: list[DynamicFormItem] = []

    def build(self) -> DynamicForm:
        return DynamicForm(self.master, self.title, self.items)

    def add_checkbutton_row(self, name: str, text: str, initial_value: bool) -> Self:
        self.items.append(
            DynamicFormItem(
                name=name,
                value=initial_value,
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
        self.items.append(
            DynamicFormItem(
                name=name,
                value=initial_value,
                widget="combobox",
                kwargs={
                    "values": values,
                },
            )
        )
        return self

    def add_entry_row(self, name: str, initial_value: str) -> Self:
        self.items.append(
            DynamicFormItem(
                name=name,
                value=initial_value,
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
        self.items.append(
            DynamicFormItem(
                name=name,
                value=initial_value,
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
        self.items.append(
            DynamicFormItem(
                name=name,
                value=initial_value,
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
        self.items.append(
            DynamicFormItem(
                name=name,
                value=initial_value,
                widget="scale",
                kwargs={
                    "to": to,
                    "from_": from_,
                },
            )
        )
        return self
