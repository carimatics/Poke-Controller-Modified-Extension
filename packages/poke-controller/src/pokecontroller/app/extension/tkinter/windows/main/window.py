import tkinter as tk
import tkinter.ttk as ttk

from ...components import AppFrame

from .camera import CameraPane
from .controller import ControllerPane
from .outputs import OutputsPane
from .settings import SettingsPane

CAMERA = 'camera'
SETTINGS = 'settings'
OUTPUTS = 'outputs'
CONTROLLER = 'controller'

PANES = [
    (CAMERA, CameraPane, tk.LEFT),
    (SETTINGS, SettingsPane, tk.LEFT),
    (OUTPUTS, OutputsPane, tk.RIGHT),
    (CONTROLLER, ControllerPane, tk.RIGHT),
]


class MainWindow(AppFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # noinspection PyTypeChecker
        self._outputs_size: tk.IntVar = self.app_state.other_output_size
        # noinspection PyTypeChecker
        self._visible_output1: tk.BooleanVar = self.app_state.other_widget_visible_output1
        # noinspection PyTypeChecker
        self._visible_output2: tk.BooleanVar = self.app_state.other_widget_visible_output2
        # noinspection PyTypeChecker
        self._visible_controller: tk.BooleanVar = self.app_state.other_widget_visible_software_controller
        # noinspection PyTypeChecker
        self._controller_position: tk.StringVar = self.app_state.other_widget_software_controller_position
        self._callback_ids: list[tuple[tk.Variable, str]] = [
            (var, var.trace_add('write', self._on_widget_state_changed)) for var in [
                self._outputs_size,
                self._visible_output1,
                self._visible_output2,
                self._visible_controller,
                self._controller_position,
            ]
        ]

        self._panes: dict[str, ttk.Frame] = {}
        self._frames: dict[str, ttk.Frame] = {}
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
    def _right_frame(self) -> ttk.Frame:
        return self._frames[tk.RIGHT]

    def build_ui(self):
        # Frames
        self._frames[tk.LEFT] = ttk.Frame(self)
        self._frames[tk.RIGHT] = ttk.Frame(self)

        # Create Panes
        for name, pane_class, side in PANES:
            self._panes[name] = pane_class(self._frames[side])

        # Layout
        self._layout_left_frame()
        self._layout_right_frame()

    def _layout_left_frame(self):
        self._panes[CAMERA].pack(expand=True, fill=tk.BOTH)
        self._panes[SETTINGS].pack(expand=False, fill=tk.BOTH, pady=(4, 0))
        self._frames[tk.LEFT].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=4, pady=(0, 4))

    def _layout_right_frame(self):
        right_frame = self._right_frame
        outputs_pane = self._outputs_pane
        output1 = outputs_pane.outputs[0]
        output2 = outputs_pane.outputs[1]
        visible_output1 = self._visible_output1.get()
        visible_output2 = self._visible_output2.get()
        visible_outputs = visible_output1 or visible_output2
        controller_pane = self._controller_pane
        visible_controller = self._visible_controller.get()
        controller_position = self._controller_position.get()

        right_frame.pack_forget()
        outputs_pane.pack_forget()
        output1.pack_forget()
        output2.pack_forget()
        controller_pane.pack_forget()

        pady_output2 = (0, 0)
        if visible_output1:
            output1.pack(expand=True, fill=tk.BOTH)
            pady_output2 = (4, 0)
        if visible_output2:
            output2.pack(expand=True, fill=tk.BOTH, pady=pady_output2)

        pady_lower_pane = (0, 0)
        if controller_position == 'bottom':
            if visible_outputs:
                outputs_pane.pack(expand=True, fill=tk.BOTH)
                pady_lower_pane = (4, 0)
            if visible_controller:
                controller_pane.pack(expand=False, fill=tk.BOTH, pady=pady_lower_pane)
        else:
            if visible_controller:
                controller_pane.pack(expand=False, fill=tk.BOTH)
                pady_lower_pane = (4, 0)
            if visible_outputs:
                outputs_pane.pack(expand=True, fill=tk.BOTH, pady=pady_lower_pane)
        if visible_outputs or visible_controller:
            right_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=4, pady=(0, 4))

    def _on_widget_state_changed(self, _var_name: str, _index: str, _mode: str):
        self._layout_right_frame()

    def destroy(self):
        for var, callback_id in self._callback_ids:
            var.trace_remove('write', callback_id)
        super().destroy()
