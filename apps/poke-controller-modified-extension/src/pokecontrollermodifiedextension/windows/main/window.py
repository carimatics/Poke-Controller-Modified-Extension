import math
import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, Literal

from ...state import AppGuiState
from ...values import literals as l
from ...widgets import AppFrame
from .camera import CameraPane
from .controller import ControllerPane
from .outputs import OutputsPane
from .settings import SettingsPane

CAMERA = "camera"
SETTINGS = "settings"
OUTPUTS = "outputs"
CONTROLLER = "controller"

PANES = [
    (CAMERA, CameraPane, l.LEFT),
    (SETTINGS, SettingsPane, l.LEFT),
    (OUTPUTS, OutputsPane, l.RIGHT),
    (CONTROLLER, ControllerPane, l.RIGHT),
]


class MainWindow(AppFrame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self._outputs_size = self.app_state.widget.outputs.size_balance
        self._visible_output1 = self.app_state.widget.outputs.visible_output1
        self._visible_output2 = self.app_state.widget.outputs.visible_output2
        self._visible_controller = self.app_state.widget.software_controller.visible
        self._controller_position = self.app_state.widget.software_controller.position

        self._panes: dict[str, ttk.Frame] = {}
        self._frames: dict[str, ttk.Frame] = {}
        self._register_hooks()
        self.build_ui()

    @property
    def app_state(self) -> AppGuiState:
        return self.app.app_state

    @property
    def _outputs_pane(self) -> OutputsPane:
        # noinspection PyTypeChecker
        return self._panes[OUTPUTS]  # type: ignore[return-value]

    @property
    def _controller_pane(self) -> ControllerPane:
        # noinspection PyTypeChecker
        return self._panes[CONTROLLER]  # type: ignore[return-value]

    @property
    def _left_frame(self) -> ttk.Frame:
        return self._frames[l.LEFT]

    @property
    def _right_frame(self) -> ttk.Frame:
        return self._frames[l.RIGHT]

    def build_ui(self) -> None:
        # Frames
        self._frames[l.LEFT] = ttk.Frame(self)
        self._frames[l.RIGHT] = ttk.Frame(self)

        # Create Panes
        for name, pane_class, side in PANES:
            self._panes[name] = pane_class(self._frames[side])

        # Layout
        self._layout_left_frame()
        self._layout_right_frame()

    def _register_hooks(self) -> None:
        self._outputs_size.trace_add("write", self._on_outputs_size_changed)
        self._visible_output1.trace_add("write", self._on_widget_visibility_changed)
        self._visible_output2.trace_add("write", self._on_widget_visibility_changed)
        self._visible_controller.trace_add("write", self._on_widget_visibility_changed)
        self._controller_position.trace_add(
            "write", self._on_controller_position_changed
        )

    def _layout_left_frame(self) -> None:
        self._panes[CAMERA].pack(expand=True, fill=l.BOTH)
        self._panes[SETTINGS].pack(expand=False, fill=l.BOTH, pady=(4, 0))
        self._frames[l.LEFT].pack(
            expand=True,
            fill=l.BOTH,
            side=l.LEFT,
            padx=4,
            pady=(0, 4),
        )

    def _layout_right_frame(self) -> None:
        def pack(
            frame: ttk.Frame,
            visible: bool,
            *,
            side: Literal["top", "left"] = l.TOP,
            px: tuple[int, int] | int = 0,
            py: tuple[int, int] | int = 0,
        ) -> None:
            frame.pack_forget()
            if visible:
                frame.pack(expand=True, fill=l.BOTH, side=side, padx=px, pady=py)

        # pack output frames
        output1, output2 = self._outputs_pane.outputs
        visible_output1 = self._visible_output1.get()
        visible_output2 = self._visible_output2.get()
        pack(output1, visible_output1)
        pack(output2, visible_output2, py=(4, 0) if visible_output1 else 0)

        # pack panes
        self._repack_right_panes()

        # pack right frame
        right_frame = self._right_frame
        visible_controller = self._visible_controller.get()
        visible_right_frame = visible_output1 or visible_output2 or visible_controller
        pack(right_frame, visible_right_frame, side=l.LEFT, px=4, py=(0, 4))

    def _repack_right_panes(self) -> None:
        self._adjust_outputs_size()

        outputs_pane, controller_pane = self._outputs_pane, self._controller_pane
        outputs_pane.pack_forget()
        controller_pane.pack_forget()

        visible_outputs = self._visible_output1.get() or self._visible_output2.get()
        visible_controller = self._visible_controller.get()
        if self._controller_position.get() == "bottom":
            if visible_outputs:
                outputs_pane.pack(expand=True, fill=l.BOTH)
            if visible_controller:
                controller_pane.pack(
                    expand=False,
                    fill=l.BOTH,
                    pady=(4, 0) if visible_outputs else (0, 0),
                )
        else:
            if visible_controller:
                controller_pane.pack(expand=False, fill=l.BOTH)
            if visible_outputs:
                outputs_pane.pack(
                    expand=True,
                    fill=l.BOTH,
                    pady=(4, 0) if visible_controller else (0, 0),
                )

    def _adjust_outputs_size(self) -> None:
        output1, output2 = self._outputs_pane.outputs
        if (t1 := output1.text_area) is None or (t2 := output2.text_area) is None:
            raise RuntimeError("Outputs text areas are not initialized.")

        if (size := self._outputs_size.get()) is None:
            raise RuntimeError("Outputs size is not initialized.")

        outputs_pane_height = self._left_frame.winfo_height()
        if self._visible_controller.get():
            controller_height = self._controller_pane.winfo_height()
            outputs_pane_height -= controller_height

        shareable_height = (outputs_pane_height / 13) - 8
        size_share_percentage = math.ceil(size) / 100

        t1.configure(height=shareable_height * size_share_percentage)
        t2.configure(height=shareable_height * (1.0 - size_share_percentage))

    def _on_widget_visibility_changed(self, *_: Any) -> None:
        self._layout_right_frame()

    def _on_outputs_size_changed(self, *_: Any) -> None:
        self._adjust_outputs_size()

    def _on_controller_position_changed(self, *_: Any) -> None:
        self._repack_right_panes()
