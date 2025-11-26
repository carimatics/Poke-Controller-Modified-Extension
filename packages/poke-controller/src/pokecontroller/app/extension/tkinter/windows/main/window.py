import tkinter.ttk as ttk
from typing import Literal

import math

from ...components import AppFrame
from ...values import literals as l

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
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._outputs_size = self.app_state.other_output_size
        self._visible_output1 = self.app_state.other_widget_visible_output1
        self._visible_output2 = self.app_state.other_widget_visible_output2
        self._visible_controller = (
            self.app_state.other_widget_visible_software_controller
        )
        self._controller_position = (
            self.app_state.other_widget_software_controller_position
        )

        self._panes: dict[str, ttk.Frame] = {}
        self._frames: dict[str, ttk.Frame] = {}
        self._register_hooks()
        self.build_ui()

    @property
    def _outputs_pane(self) -> OutputsPane:
        # noinspection PyTypeChecker
        return self._panes[OUTPUTS]

    @property
    def _controller_pane(self) -> ControllerPane:
        # noinspection PyTypeChecker
        return self._panes[CONTROLLER]

    @property
    def _left_frame(self) -> ttk.Frame:
        return self._frames[l.LEFT]

    @property
    def _right_frame(self) -> ttk.Frame:
        return self._frames[l.RIGHT]

    def build_ui(self):
        # Frames
        self._frames[l.LEFT] = ttk.Frame(self)
        self._frames[l.RIGHT] = ttk.Frame(self)

        # Create Panes
        for name, pane_class, side in PANES:
            self._panes[name] = pane_class(self._frames[side])

        # Layout
        self._layout_left_frame()
        self._layout_right_frame()

    def _register_hooks(self):
        self._outputs_size.register_hook("write", self._on_outputs_size_changed)
        self._visible_output1.register_hook("write", self._on_widget_visibility_changed)
        self._visible_output2.register_hook("write", self._on_widget_visibility_changed)
        self._visible_controller.register_hook(
            "write", self._on_widget_visibility_changed
        )
        self._controller_position.register_hook(
            "write", self._on_controller_position_changed
        )

    def _layout_left_frame(self):
        self._panes[CAMERA].pack(expand=True, fill=l.BOTH)
        self._panes[SETTINGS].pack(expand=False, fill=l.BOTH, pady=(4, 0))
        self._frames[l.LEFT].pack(
            expand=True,
            fill=l.BOTH,
            side=l.LEFT,
            padx=4,
            pady=(0, 4),
        )

    def _layout_right_frame(self):
        def pack(
            frame: ttk.Frame,
            visible: bool,
            *,
            side: Literal["top", "left"] = l.TOP,
            px: tuple[int, int] | int = 0,
            py: tuple[int, int] | int = 0,
        ):
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
        visible_right_frame = (
            visible_output1 or visible_output2 or self._visible_controller.get()
        )
        pack(right_frame, visible_right_frame, side=l.LEFT, px=4, py=(0, 4))

    def _repack_right_panes(self):
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

    def _adjust_outputs_size(self):
        outputs_pane_height = self._left_frame.winfo_height()
        if self._visible_controller.get():
            controller_height = self._controller_pane.winfo_height()
            outputs_pane_height -= controller_height

        shareable_height = (outputs_pane_height / 13) - 8
        size_share_percentage = math.ceil(self._outputs_size.get()) / 100

        output1, output2 = self._outputs_pane.outputs
        output1.text_area.configure(height=shareable_height * size_share_percentage)
        output2.text_area.configure(
            height=shareable_height * (1.0 - size_share_percentage)
        )

    def _on_widget_visibility_changed(self):
        self._layout_right_frame()

    def _on_outputs_size_changed(self):
        self._adjust_outputs_size()

    def _on_controller_position_changed(self):
        self._repack_right_panes()
