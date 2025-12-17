from dataclasses import dataclass

from pokecontroller.core.camera import Camera
from pokecontroller.core.serial import Serial

from pokecontrollermodifiedextension.api.v0_1_8.camera import Camera as Camera_v0_1_8
from pokecontrollermodifiedextension.api.v0_1_8.command.sender import (
    Sender as Sender_v0_1_8,
)
from pokecontrollermodifiedextension.exception import AppRuntimeException


@dataclass(kw_only=True, frozen=True)
class AppResources:
    camera: Camera
    serial: Serial
    camera_v0_1_8: Camera_v0_1_8
    sender_v0_1_8: Sender_v0_1_8


_app_resources: AppResources | None = None


def get_app_resources() -> AppResources:
    global _app_resources
    if _app_resources is None:
        raise AppRuntimeException("App resources is not initialized.")
    return _app_resources


def setup_app_resources(
    camera: Camera,
    serial: Serial,
    camera_v0_1_8: Camera_v0_1_8,
    sender_v0_1_8: Sender_v0_1_8,
) -> AppResources:
    global _app_resources
    _app_resources = AppResources(
        camera=camera,
        serial=serial,
        camera_v0_1_8=camera_v0_1_8,
        sender_v0_1_8=sender_v0_1_8,
    )
    return _app_resources
