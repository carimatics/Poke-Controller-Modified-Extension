import logging
import os

from plyer import notification

from pokecontroller.core.image.raw_image import RawImage
from pokecontroller.core.notification.notifier import Notifier, RateLimit
from pokecontroller.utils import platform

logger = logging.getLogger(__name__)


class DesktopNotifier(Notifier):
    def __init__(self, title: str) -> None:
        self._title = title

    @property
    def keys(self) -> list[str]:
        logger.info("Desktop notification do not have any keys")
        return []

    @property
    def has_error(self) -> bool:
        return False

    def notify(
        self,
        message: str | None = None,
        image: RawImage | None = None,
        keys: list[str] | None = None,
    ) -> None:
        if message is None:
            logger.warning("Desktop notification is not supported empty message")
            return
        if image is not None:
            logger.info("Desktop notification is not supported image")
        if keys is not None:
            logger.info("Desktop notification is not supported keys")

        if platform.is_macos():
            self._notify_macos(message)
        else:
            self._notify(message)

    def get_late_limits(self) -> list[RateLimit]:
        logger.info("Desktop notification is not supported rate limit")
        return []

    def apply_config(self) -> None:
        logger.info("Desktop notification is not supported config")

    def _notify(self, message: str) -> None:
        notification.notify(
            title=self._title,
            message=message,
            timeout=5,
        )

    def _notify_macos(self, message: str) -> None:
        sound_name = "default"

        message_text = f'display notification "{message}"'
        title_text = f'with title "{self._title}"'
        sound_text = f'sound name "{sound_name}"'
        notification_text = f"{message_text} {title_text} {sound_text}"
        os.system(f"osascript -e '{notification_text}'")
