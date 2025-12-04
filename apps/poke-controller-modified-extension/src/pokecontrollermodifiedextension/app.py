import tkinter as tk
from typing import Any

from pokecontroller.core.camera import Camera

from .info import AppInfo
from .model import AppModel
from .state import AppGuiState, load_state

INFO = AppInfo(
    name="Poke-Controller Modified Extension",
    version="0.2.0",
)


class App(tk.Tk):
    _camera_id: tk.StringVar
    _camera_size: tk.StringVar
    _fps: tk.IntVar

    def __init__(
        self,
        base_dir: str,
        profile: str,
        camera: Camera,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._base_dir = base_dir
        self._profile = profile

        self._camera = camera

        self._app_info = INFO
        self._gui_state = load_state(base_dir=base_dir, profile=profile)
        self._app_model = AppModel(self._app_info, self._gui_state)

        # Theme
        # style = ttk.Style(self)
        # style.theme_use(self._gui_state.general.theme.get())

        # Title
        self.title(f"{INFO.name}(v{INFO.version})")

        self.resizable(width=False, height=False)

        # Camera
        self._initialize_camera()

        self._register_hooks()

    @property
    def base_dir(self) -> str:
        return self._base_dir

    @property
    def profile(self) -> str:
        return self._profile

    @property
    def camera(self) -> Camera:
        return self._camera

    @property
    def app_info(self) -> AppInfo:
        return self._app_info

    @property
    def app_model(self) -> AppModel:
        return self._app_model

    @property
    def gui_state(self) -> AppGuiState:
        return self._gui_state

    def run(self) -> None:
        self.mainloop()

    def _initialize_camera(self) -> None:
        self._camera_id = self._gui_state.capture.camera_id
        self._camera_size = self._gui_state.capture.size
        self._fps = self._gui_state.capture.fps
        width, height = self._parse_camera_size()
        fps = self._fps.get()
        self._camera.frame_size = (width, height)
        self._camera.fps = fps
        self._camera.open(camera_id=int(self._camera_id.get()))

    def _register_hooks(self) -> None:
        self._camera_size.trace_add("write", self._on_camera_size_changed)
        self._fps.trace_add("write", self._on_fps_changed)
        self._camera_id.trace_add("write", self._on_camera_id_changed)

    def _on_camera_size_changed(self, *_: Any) -> None:
        width, height = self._parse_camera_size()
        self._camera.frame_size = (width, height)

    def _on_fps_changed(self, *_: Any) -> None:
        self._camera.fps = self._fps.get()

    def _on_camera_id_changed(self, *_: Any) -> None:
        self._camera.open(camera_id=int(self._camera_id.get()))

    def _parse_camera_size(self) -> tuple[int, int]:
        width, height =  self._camera_size.get().split("x")
        return int(width), int(height)
