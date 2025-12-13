import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass, field
from typing import Any, Literal, Self, overload

from .... import widgets
from ....mixins import AppAccessorMixIn
from ....values import literals as l
from ....widgets.app.frame import AppFrame

type WidgetType = Literal[
    "label",
    "checkbutton",
    "combobox",
    "entry",
    "radiobutton",
    "spinbox",
    "scale",
]


@dataclass
class DynamicInputItem:
    widget: WidgetType
    label_text: str
    label_width: int
    variable: tk.Variable
    kwargs: dict[str, Any] = field(default_factory=dict)


class DynamicInputs(AppFrame):
    def __init__(
        self,
        master: tk.Misc,
        items: list[DynamicInputItem],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self._items = items
        self._variable_traces: list[tuple[tk.Variable, str]] = []
        self.build_ui()

    def build_ui(self) -> None:
        frame = widgets.Frame(self)
        for item in self._items:
            self._build_dynamic_widgets(frame, item)
        frame.pack(expand=True, fill=l.BOTH)

    def _build_dynamic_widgets(
        self, master: widgets.Frame, item: DynamicInputItem
    ) -> None:
        frame = widgets.Frame(master, padding=(5, 5))
        match item:
            case DynamicInputItem(
                widget="label",
                label_text=label_text,
                label_width=label_width,
                variable=variable,
                kwargs=label_kwargs,
            ) if isinstance(variable, tk.StringVar):
                label = widgets.Label(frame, text=label_text, width=label_width)
                widget: ttk.Widget = widgets.Label(
                    frame,
                    textvariable=variable,
                    **label_kwargs,
                )

                # Layout
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.W,
                )
                widget.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.NONE,
                    anchor=l.CENTER,
                )
            case DynamicInputItem(
                widget="checkbutton",
                label_text=label_text,
                label_width=label_width,
                variable=variable,
                kwargs=checkbutton_kwargs,
            ) if isinstance(variable, tk.BooleanVar):
                label = widgets.Label(frame, text=label_text, width=label_width)
                widget = widgets.Checkbutton(
                    frame,
                    variable=variable,
                    **checkbutton_kwargs,
                )

                # Layout
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.W,
                )
                widget.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.NONE,
                    anchor=l.CENTER,
                )
            case DynamicInputItem(
                widget="combobox",
                label_text=label_text,
                label_width=label_width,
                variable=variable,
                kwargs=checkbox_kwargs,
            ) if isinstance(variable, (tk.StringVar, tk.IntVar)):
                label = widgets.Label(frame, text=label_text, width=label_width)
                widget = widgets.Combobox(
                    frame,
                    textvariable=variable,
                    **checkbox_kwargs,
                )

                # Layout
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.W,
                )
                widget.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.NONE,
                    anchor=l.CENTER,
                )
            case DynamicInputItem(
                widget="entry",
                label_text=label_text,
                label_width=label_width,
                variable=variable,
                kwargs=entry_kwargs,
            ) if isinstance(variable, tk.StringVar):
                label = widgets.Label(frame, text=label_text, width=label_width)
                widget = widgets.Entry(
                    frame,
                    textvariable=variable,
                    **entry_kwargs,
                )

                # Layout
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.W,
                )
                widget.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.NONE,
                    anchor=l.CENTER,
                )
            case DynamicInputItem(
                widget="radiobutton",
                label_text=label_text,
                label_width=label_width,
                variable=variable,
                kwargs={"values": values, **radiobutton_kwargs},
            ) if isinstance(variable, tk.StringVar):
                label = widgets.Label(frame, text=label_text, width=label_width)
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.W,
                )
                for column_index, value in enumerate(values):
                    radio = widgets.Radiobutton(
                        frame,
                        text=value,
                        variable=variable,
                        value=value,
                        **radiobutton_kwargs,
                    )
                    radio.pack(
                        expand=False,
                        side=l.LEFT,
                        fill=l.NONE,
                        anchor=l.CENTER,
                    )
            case DynamicInputItem(
                widget="spinbox",
                label_text=label_text,
                label_width=label_width,
                variable=variable,
                kwargs={
                    "disabled": disabled,
                    **spinbox_kwargs,
                },
            ) if all(
                (
                    isinstance(variable, tk.IntVar),
                    isinstance(disabled, tk.BooleanVar),
                )
            ):
                label = widgets.Label(frame, text=label_text, width=label_width)
                widget = widgets.Spinbox(
                    frame,
                    textvariable=variable,
                    state=l.DISABLED if disabled.get() else l.NORMAL,
                    **spinbox_kwargs,
                )

                # trace
                self._trace_disabled(widget, disabled)

                # Layout
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.W,
                )
                widget.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.NONE,
                    anchor=l.CENTER,
                )
            case DynamicInputItem(
                widget="scale",
                label_text=label_text,
                label_width=label_width,
                variable=variable,
                kwargs={
                    "to": int(to),
                    "from_": int(from_),
                    "disabled": disabled,
                    **int_scale_kwargs,
                },
            ) if all(
                (
                    isinstance(variable, tk.IntVar),
                    isinstance(disabled, tk.BooleanVar),
                )
            ):
                label = widgets.Label(frame, text=label_text, width=label_width)
                scale_label = widgets.Label(
                    frame,
                    width=3,
                    text=variable.get(),
                )
                widget = widgets.Scale(
                    frame,
                    variable=variable,
                    to=to,
                    from_=from_,
                    state=l.DISABLED if disabled.get() else l.NORMAL,
                    **int_scale_kwargs,
                )

                # trace
                self._variable_traces.append(
                    (
                        variable,
                        variable.trace_add(
                            "write",
                            lambda *_: scale_label.configure(text=int(variable.get())),
                        ),
                    )
                )
                self._trace_disabled(widget, disabled)

                # Layout
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.W,
                )
                scale_label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                )
                widget.pack(
                    expand=True,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                )
            case DynamicInputItem(
                widget="scale",
                label_text=label_text,
                label_width=label_width,
                variable=variable,
                kwargs={
                    "to": float(to),
                    "from_": float(from_),
                    "disabled": disabled,
                    **float_scale_kwargs,
                },
            ) if all(
                (
                    isinstance(variable, tk.DoubleVar),
                    isinstance(disabled, tk.BooleanVar),
                )
            ):
                label = widgets.Label(frame, text=label_text, width=label_width)
                scale_label = widgets.Label(
                    frame,
                    width=3,
                    text=f"{variable.get():.2f}",
                )
                widget = widgets.Scale(
                    frame,
                    variable=variable,
                    to=to,
                    from_=from_,
                    state=l.DISABLED if disabled.get() else l.NORMAL,
                    **float_scale_kwargs,
                )

                # trace
                self._variable_traces.append(
                    (
                        variable,
                        variable.trace_add(
                            "write",
                            lambda *_: scale_label.configure(
                                text=f"{variable.get():.2f}"
                            ),
                        ),
                    )
                )
                self._trace_disabled(widget, disabled)

                # Layout
                label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.W,
                )
                scale_label.pack(
                    expand=False,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                )
                widget.pack(
                    expand=True,
                    side=l.LEFT,
                    fill=l.BOTH,
                    anchor=l.CENTER,
                )
            case _:
                raise ValueError(f"Unsupported widget: {item}")
        frame.pack(expand=False, side=l.TOP, fill=l.BOTH, padx=5, pady=5)

    def destroy(self) -> None:
        for variable, trace_id in self._variable_traces:
            variable.trace_remove("write", trace_id)
        super().destroy()

    def _trace_disabled(self, widget: ttk.Widget, disabled: tk.BooleanVar) -> None:
        self._variable_traces.append(
            (
                disabled,
                disabled.trace_add(
                    "write",
                    lambda *_: widget.configure(  # type: ignore[call-arg]
                        state=l.DISABLED if disabled.get() else l.NORMAL,
                    ),
                ),
            )
        )


class DynamicInputsBuilder:
    def __init__(self, master: AppAccessorMixIn, label_width: int) -> None:
        self.master = master
        self.label_width = label_width
        self.items: list[DynamicInputItem] = []

    def build(self) -> DynamicInputs:
        return DynamicInputs(self.master, self.items)

    def add_label_row(
        self,
        label_text: str,
        variable: tk.StringVar,
    ) -> Self:
        self.items.append(
            DynamicInputItem(
                widget="label",
                label_text=label_text,
                label_width=self.label_width,
                variable=variable,
            )
        )
        return self

    def add_checkbutton_row(
        self,
        label_text: str,
        text: str,
        variable: tk.BooleanVar,
    ) -> Self:
        self.items.append(
            DynamicInputItem(
                label_text=label_text,
                label_width=self.label_width,
                variable=variable,
                widget="checkbutton",
                kwargs={"text": text},
            )
        )
        return self

    def add_combobox_row(
        self,
        label_text: str,
        variable: tk.StringVar | tk.IntVar,
        values: list[str],
    ) -> Self:
        self.items.append(
            DynamicInputItem(
                label_text=label_text,
                label_width=self.label_width,
                variable=variable,
                widget="combobox",
                kwargs={
                    "values": values,
                },
            )
        )
        return self

    def add_entry_row(
        self,
        label_text: str,
        variable: tk.StringVar,
    ) -> Self:
        self.items.append(
            DynamicInputItem(
                label_text=label_text,
                label_width=self.label_width,
                variable=variable,
                widget="entry",
            )
        )
        return self

    def add_radiobutton_row(
        self,
        label_text: str,
        variable: tk.StringVar,
        values: list[str],
    ) -> Self:
        self.items.append(
            DynamicInputItem(
                label_text=label_text,
                label_width=self.label_width,
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
        label_text: str,
        variable: tk.IntVar,
        to: int,
        from_: int,
        increment: int = 1,
        disabled: tk.BooleanVar | None = None,
    ) -> Self:
        self.items.append(
            DynamicInputItem(
                label_text=label_text,
                label_width=self.label_width,
                variable=variable,
                widget="spinbox",
                kwargs={
                    "to": to,
                    "from_": from_,
                    "increment": increment,
                    "disabled": disabled,
                },
            )
        )
        return self

    @overload
    def add_scale_row(
        self,
        label_text: str,
        variable: tk.IntVar,
        to: int,
        from_: int,
        orient: Literal["horizontal", "vertical"] = "horizontal",
        disabled: tk.BooleanVar | None = None,
    ) -> Self: ...

    @overload
    def add_scale_row(
        self,
        label_text: str,
        variable: tk.DoubleVar,
        to: float,
        from_: float,
        orient: Literal["horizontal", "vertical"] = "horizontal",
        disabled: tk.BooleanVar | None = None,
    ) -> Self: ...

    def add_scale_row(
        self,
        label_text: str,
        variable: tk.IntVar | tk.DoubleVar,
        to: int | float,
        from_: int | float,
        orient: Literal["horizontal", "vertical"] = "horizontal",
        disabled: tk.BooleanVar | None = None,
    ) -> Self:
        self.items.append(
            DynamicInputItem(
                widget="scale",
                label_text=label_text,
                label_width=self.label_width,
                variable=variable,
                kwargs={
                    "to": to,
                    "from_": from_,
                    "orient": orient,
                    "disabled": disabled,
                },
            )
        )
        return self
