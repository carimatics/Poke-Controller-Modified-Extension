import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Callable, Literal, Protocol, Self, overload

from ..button import Button
from ..checkbutton import Checkbutton
from ..combobox import Combobox
from ..entry import Entry
from ..frame import Frame
from ..label import Label
from ..labelframe import Labelframe
from ..radiobutton import Radiobutton
from ..scale import Scale
from ..scrollable_frame import ScrollableFrame
from ..spinbox import Spinbox


class TraceRegisterable(Protocol):
    def register_trace(
        self,
        mode: Literal["write"],
        variable: tk.Variable,
        callback: Callable[[str, str, str], None],
    ) -> None: ...


class ComponentPackRowBuilder[T: TraceRegisterable]:
    def __init__(
        self,
        parent: T,
        master: Frame | Labelframe | ScrollableFrame,
    ) -> None:
        self._parent = parent
        self._master = master

    def add_button(
        self,
        text: str,
        command: Callable[[], Any],
        disabled: tk.BooleanVar | None = None,
    ) -> Self:
        button = Button(self._master, text=text, command=command)
        button.pack(side=tk.LEFT)
        if disabled is not None:
            button.configure(state=tk.DISABLED if disabled.get() else tk.NORMAL)
            self._register_disable_trace(button, disabled)
        return self

    def add_checkbutton(
        self,
        variable: tk.BooleanVar,
        text: str,
        disabled: tk.BooleanVar | None = None,
    ) -> Self:
        checkbutton = Checkbutton(self._master, variable=variable, text=text)
        checkbutton.pack(side=tk.LEFT)
        if disabled is not None:
            checkbutton.configure(state=tk.DISABLED if disabled.get() else tk.NORMAL)
            self._register_disable_trace(checkbutton, disabled)
        return self

    def add_combobox(
        self,
        variable: tk.IntVar | tk.StringVar,
        values: list[str],
        disabled: tk.BooleanVar | None = None,
    ) -> Self:
        combobox = Combobox(self._master, textvariable=variable, values=values)
        combobox.pack(side=tk.LEFT)
        if disabled is not None:
            combobox.configure(state=tk.DISABLED if disabled.get() else tk.NORMAL)
            self._register_disable_trace(combobox, disabled)
        return self

    def add_entry(
        self,
        variable: tk.StringVar,
        disabled: tk.BooleanVar | None = None,
    ) -> Self:
        entry = Entry(self._master, variable=variable)
        entry.pack(side=tk.LEFT)
        if disabled is not None:
            entry.configure(state=tk.DISABLED if disabled.get() else tk.NORMAL)
            self._register_disable_trace(entry, disabled)
        return self

    @overload
    def add_label(
        self, *, variable: tk.StringVar, width: int | None = None
    ) -> Self: ...

    @overload
    def add_label(self, *, text: str, width: int | None = None) -> Self: ...

    def add_label(
        self,
        *,
        variable: tk.StringVar | None = None,
        text: str | None = None,
        width: int | None = None,
    ) -> Self:
        if variable is not None:
            label = Label(self._master, textvariable=variable)
        elif text is not None:
            label = Label(self._master, text=text)
        else:
            raise ValueError("Either variable or text must be specified.")
        if width is not None:
            label.configure(width=width)
        label.pack(side=tk.LEFT)
        return self

    def add_radiobutton(self, variable: tk.StringVar, values: list[str]) -> Self:
        for value in values:
            Radiobutton(self._master, variable=variable, value=value).pack(side=tk.LEFT)
        return self

    @overload
    def add_scale(
        self,
        variable: tk.IntVar,
        from_: int,
        to: int,
        expand: bool = False,
        disabled: tk.BooleanVar | None = None,
    ) -> Self: ...

    @overload
    def add_scale(
        self,
        variable: tk.DoubleVar,
        from_: float,
        to: float,
        expand: bool = False,
        disabled: tk.BooleanVar | None = None,
    ) -> Self: ...

    def add_scale(
        self,
        variable: tk.IntVar | tk.DoubleVar,
        from_: int | float,
        to: int | float,
        expand: bool = False,
        disabled: tk.BooleanVar | None = None,
    ) -> Self:
        scale = Scale(
            self._master,
            variable=variable,
            from_=from_,
            to=to,
        )
        if disabled is not None:
            scale.configure(state=tk.DISABLED if disabled.get() else tk.NORMAL)
            self._register_disable_trace(scale, disabled)
        if expand:
            scale.pack(side=tk.LEFT, expand=expand, fill=tk.X)
        else:
            scale.pack(side=tk.LEFT)
        return self

    def add_spinbox(
        self,
        variable: tk.IntVar,
        to: int,
        from_: int,
        increment: int = 1,
        disabled: tk.BooleanVar | None = None,
    ) -> Self:
        spinbox = Spinbox(
            self._master,
            textvariable=variable,
            to=to,
            from_=from_,
            increment=increment,
        )
        if disabled is not None:
            spinbox.configure(state=tk.DISABLED if disabled.get() else tk.NORMAL)
            self._register_disable_trace(spinbox, disabled)
        spinbox.pack(side=tk.LEFT)
        return self

    def add_frame_row(self) -> "ComponentPackRowBuilder[Self]":
        return ComponentPackRowBuilder(self, Frame(self._master))

    def add_labelframe_row(self) -> "ComponentPackRowBuilder[Self]":
        return ComponentPackRowBuilder(self, Labelframe(self._master))

    def add_scrollable_frame_row(self) -> "ComponentPackRowBuilder[Self]":
        return ComponentPackRowBuilder(self, ScrollableFrame(self._master))

    def end(self) -> T:
        self._master.pack(expand=False, side=tk.TOP, fill=tk.X)
        return self._parent

    def register_trace(
        self,
        mode: Literal["write"],
        variable: tk.Variable,
        callback: Callable[[str, str, str], None],
    ) -> None:
        self._parent.register_trace(mode, variable, callback)

    def _register_disable_trace(
        self,
        widget: ttk.Widget,
        disabled: tk.BooleanVar,
    ) -> None:
        self._parent.register_trace(
            "write",
            disabled,
            lambda *_: widget.configure(  # type: ignore[call-arg]
                state=tk.DISABLED if disabled.get() else tk.NORMAL,
            ),
        )


class ComponentPackBuilder:
    _container: Frame | Labelframe | ScrollableFrame | None

    def __init__(self, master: Frame | Labelframe | ScrollableFrame) -> None:
        self._master = master
        self._container = None

    def add_frame_row(self) -> ComponentPackRowBuilder[Self]:
        self._container = Frame(self._master)
        return ComponentPackRowBuilder(self, self._container)

    def add_labelframe_row(self) -> ComponentPackRowBuilder[Self]:
        self._container = Labelframe(self._master)
        return ComponentPackRowBuilder(self, self._container)

    def add_scrollable_frame_row(self) -> ComponentPackRowBuilder[Self]:
        self._container = ScrollableFrame(self._master)
        return ComponentPackRowBuilder(self, self._container)

    def build(self) -> Frame | Labelframe | ScrollableFrame:
        if self._container is None:
            return self._master
        return self._container

    def register_trace(
        self,
        mode: Literal["write"],
        variable: tk.Variable,
        callback: Callable[[str, str, str], None],
    ) -> None:
        self._master.register_trace(mode, variable, callback)
