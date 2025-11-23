from contextlib import contextmanager
from typing import Generator

from .camera import Camera


@contextmanager
def open(
    camera_id: int,
    *,
    frame_size: tuple[int, int] = (1280, 720),
    fps: int = 45
) -> Generator[Camera, None, None]:
    camera = Camera(frame_size=frame_size, fps=fps)
    try:
        camera.open(camera_id=camera_id)
        yield camera
    finally:
        camera.close()
