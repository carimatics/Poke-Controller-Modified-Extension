import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass, field
from typing import Any, Literal, Self, overload

from pokecontrollermodifiedextension.mixins import AppAccessorMixIn
from pokecontrollermodifiedextension.widgets.app.frame import AppFrame

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
    variable: tk.Variable
    kwargs: dict[str, Any] = field(default_factory=dict)


class DynamicForm(AppFrame):
    def __init__(
        self,
        master: tk.Misc,
        items: list[DynamicFormItem],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self._items = items
        self._variables: dict[str, tk.Variable] = {}
        self.build_ui()

    def build_ui(self) -> None:
        frame = tk.Frame(self)
        for item in self._items:
            self._build_dynamic_widgets(frame, item)
        frame.pack(expand=True, fill=tk.BOTH)

    def as_dict(self) -> dict[str, bool | int | float | str] | None:
        return {name: var.get() for name, var in self._variables.items()}

    def _build_dynamic_widgets(self, master: tk.Frame, item: DynamicFormItem) -> None:
        labelframe = ttk.LabelFrame(master, text=item.name, padding=(5, 5))
        match item:
            case DynamicFormItem(
                widget="checkbutton",
                name=str(name),
                variable=variable,
                kwargs=checkbutton_kwargs,
            ) if isinstance(variable, tk.BooleanVar):
                self._variables[name] = variable
                widget: tk.Widget = ttk.Checkbutton(
                    labelframe,
                    variable=variable,
                    **checkbutton_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    anchor=tk.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="combobox",
                name=str(name),
                variable=variable,
                kwargs=checkbox_kwargs,
            ) if isinstance(variable, tk.StringVar):
                self._variables[name] = variable
                widget = ttk.Combobox(
                    labelframe,
                    textvariable=variable,
                    **checkbox_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    anchor=tk.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="entry",
                name=str(name),
                variable=variable,
                kwargs=entry_kwargs,
            ) if isinstance(variable, tk.StringVar):
                self._variables[name] = variable
                widget = ttk.Entry(
                    labelframe,
                    textvariable=variable,
                    **entry_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    anchor=tk.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="radiobutton",
                name=str(name),
                variable=variable,
                kwargs={"values": values, **radiobutton_kwargs},
            ) if isinstance(variable, tk.StringVar):
                for column_index, value in enumerate(values):
                    radio = ttk.Radiobutton(
                        labelframe,
                        text=name,
                        variable=variable,
                        value=value,
                        **radiobutton_kwargs,
                    )
                    radio.pack(
                        expand=True,
                        side=tk.LEFT,
                        fill=tk.BOTH,
                        anchor=tk.CENTER,
                        padx=3,
                        pady=3,
                    )
            case DynamicFormItem(
                widget="spinbox",
                name=str(name),
                variable=variable,
                kwargs=spinbox_kwargs,
            ) if isinstance(variable, tk.StringVar):
                self._variables[name] = variable
                widget = ttk.Spinbox(
                    labelframe,
                    textvariable=variable,
                    **spinbox_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    anchor=tk.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="scale",
                name=str(name),
                variable=variable,
                kwargs={
                    "to": int(to),
                    "from_": int(from_),
                    **int_scale_kwargs,
                },
            ) if isinstance(variable, tk.IntVar):
                self._variables[name] = variable
                label = ttk.Label(labelframe, text=variable.get())
                variable.trace(
                    "w", lambda *_: label.configure(text=int(variable.get()))
                )
                label.pack(
                    expand=False,
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    anchor=tk.CENTER,
                )
                widget = ttk.Scale(
                    labelframe,
                    variable=variable,
                    to=to,
                    from_=from_,
                    **int_scale_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    anchor=tk.CENTER,
                    padx=3,
                    pady=3,
                )
            case DynamicFormItem(
                widget="scale",
                name=str(name),
                variable=variable,
                kwargs={
                    "to": float(to),
                    "from_": float(from_),
                    **float_scale_kwargs,
                },
            ) if isinstance(variable, tk.DoubleVar):
                self._variables[name] = variable
                label = ttk.Label(labelframe, text=f"{variable.get():.2f}")
                variable.trace(
                    "w", lambda *_: label.configure(text=f"{variable.get():.2f}")
                )
                label.pack(
                    expand=False,
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    anchor=tk.CENTER,
                )
                widget = ttk.Scale(
                    labelframe,
                    variable=variable,
                    to=to,
                    from_=from_,
                    **float_scale_kwargs,
                )
                widget.pack(
                    expand=True,
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    anchor=tk.CENTER,
                    padx=3,
                    pady=3,
                )
            case _:
                raise ValueError(f"Unsupported widget: {item}")
        labelframe.pack(expand=False, side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


class DynamicFormBuilder:
    def __init__(self, master: AppAccessorMixIn, title: str) -> None:
        self.master = master
        self.title = title
        self.items: list[DynamicFormItem] = []

    def build(self) -> DynamicForm:
        return DynamicForm(self.master, self.items)

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
            variable: tk.Variable = tk.IntVar(self.master)
        else:
            variable = tk.DoubleVar(self.master)
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
