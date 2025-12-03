import os
import platform
import subprocess
from pathlib import Path
from typing import Any


class CrossPlatformCommand:
    def __init__(self) -> None:
        self._is_windows = platform.system() == "Windows"

    def run(
        self,
        command: list[str],
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
        capture: bool = False,
    ) -> subprocess.CompletedProcess:
        kwargs = {
            "check": True,
            "text": True,
            "cwd": cwd,
            "env": env,
            "timeout": timeout,
        }
        if capture:
            kwargs["capture_output"] = True

        try:
            return subprocess.run(command, **kwargs)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {' '.join(command)}:")
            print(f"Return code: {e.returncode}")
            if e.stdout:
                print(f"stdout: {e.stdout}")
            if e.stderr:
                print(f"stderr: {e.stderr}")
            raise

    def run_shell(
        self,
        command: str,
        **kwargs: Any,
    ) -> subprocess.CompletedProcess:
        if self._is_windows:
            cmd = ["powershell", "-Command", command]
        else:
            cmd = ["/bin/bash", "-c", command]
        return self.run(cmd, **kwargs)


def get_usage_envs(keys: tuple[str, ...]) -> dict[str, str]:
    return {key: os.getenv(f"usage_{key}") for key in keys}
