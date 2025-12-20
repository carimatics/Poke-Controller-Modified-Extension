import logging
import re
import subprocess
from dataclasses import dataclass

import cv2

from ...utils import platform

logger = logging.getLogger(__name__)


@dataclass
class CameraInfo:
    index: int
    name: str
    backend: str | None = None


class CameraDetector:
    def __init__(self, max_cameras: int) -> None:
        self._max_cameras = max_cameras

    def detect(self) -> list[CameraInfo]:
        camera_names = self._get_all_camera_names()
        logger.debug(f"camera_name_map: {camera_names}")

        cameras: list[CameraInfo] = []
        for i in range(self._max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                name = camera_names[i] if i < len(camera_names) else f"Camera {i}"
                backend = cap.getBackendName()
                cameras.append(CameraInfo(i, name, backend))
                cap.release()
                logger.debug(f"Found camera {i}: {name} (backend: {backend})")

        logger.info(f"Found {len(cameras)} cameras.")
        return cameras

    def _get_all_camera_names(self) -> list[str]:
        if platform.is_windows():
            return self._get_windows_camera_names()
        elif platform.is_macos():
            return self._get_macos_camera_names()
        elif platform.is_linux():
            return self._get_linux_camera_names()
        else:
            return []

    def _get_windows_camera_names(self) -> list[str]:
        try:
            result = subprocess.run(
                ["ffmpeg", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
                capture_output=True,
                text=True,
                stderr=subprocess.STDOUT,
                timeout=5,
            )
            lines = result.stdout.splitlines()
            cameras = []
            in_video_section = False

            for line in lines:
                if "DirectShow video devices" in line:
                    in_video_section = True
                    continue
                if "DirectShow audio devices" in line:
                    break
                if in_video_section:
                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        cameras.append(match.group(1))
            return cameras

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning(f"ffmpeg not available, falling back to PowerShell: {e}")
            return self._get_windows_camera_names_powershell()

    def _get_windows_camera_names_powershell(self) -> list[str]:
        try:
            ps_command = (
                "Get-CimInstance Win32_PnPEntity | "
                + "Where-Object {$_.PNPClass -eq 'Camera' -or $_.PNPClass -eq 'Image'} | "
                + "Select-Object -ExpandProperty Name"
            )
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                return [
                    name.strip() for name in result.stdout.splitlines() if name.strip()
                ]
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning(f"Failed to get camera names via PowerShell: {e}")

        return []

    def _get_macos_camera_names(self) -> list[str]:
        try:
            result = subprocess.run(
                ["system_profiler", "SPCameraDataType"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                return re.findall(r"Model ID:\s*(.+)", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning(f"Failed to get camera names via system_profiler: {e}")

        return []

    def _get_linux_camera_names(self) -> list[str]:
        return []
