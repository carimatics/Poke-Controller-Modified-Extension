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


APP_RESOURCES_SINGLETON: AppResources | None = None


def get_app_resources() -> AppResources:
    global APP_RESOURCES_SINGLETON
    if APP_RESOURCES_SINGLETON is None:
        raise AppRuntimeException("App resources is not initialized.")
    return APP_RESOURCES_SINGLETON


def setup_app_resources(
    camera: Camera,
    serial: Serial,
    camera_v0_1_8: Camera_v0_1_8,
    sender_v0_1_8: Sender_v0_1_8,
) -> AppResources:
    global APP_RESOURCES_SINGLETON
    APP_RESOURCES_SINGLETON = AppResources(
        camera=camera,
        serial=serial,
        camera_v0_1_8=camera_v0_1_8,
        sender_v0_1_8=sender_v0_1_8,
    )
    return APP_RESOURCES_SINGLETON
