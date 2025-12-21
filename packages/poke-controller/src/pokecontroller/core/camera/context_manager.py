from contextlib import contextmanager
from typing import Generator

from pokecontroller.core.camera.camera import Camera


@contextmanager
def use_camera(
    frame_size: tuple[int, int] = (1280, 720),
) -> Generator[Camera, None, None]:
    camera = Camera(frame_size=frame_size)
    try:
        yield camera
    finally:
        camera.close()
