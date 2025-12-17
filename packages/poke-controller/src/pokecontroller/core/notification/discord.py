import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

from ...utils.config import Config
from ...utils.datetime import from_timestamp
from ..image import RawImage, to_bytes
from .notifier import Notifier, RateLimit

logger = logging.getLogger(__name__)

DISCORD_SECTION_DEFAULT = "DISCORD"
DISCORD_WEBHOOK_SECTION_DEFAULT = "DISCORD_WEBHOOK"
DISCORD_WEBHOOK_SECTION_KEYWORD = "DISCORD_WEBHOOK"


@dataclass(kw_only=True, frozen=True)
class DiscordWebhookOptions:
    webhook_url: str = ""
    username: str = ""
    avatar_url: str = ""


class DiscordConfig(Config):
    def __init__(self, path: Path) -> None:
        super().__init__(path)
        self._initialize()

    def get_channel_id(self, section: str) -> str | None:
        return self[section]["channel_id"]

    def set_channel_id(self, section: str, channel_id: str) -> None:
        self[section]["channel_id"] = channel_id

    def get_token(self, section: str) -> str | None:
        return self[section]["token"]

    def set_token(self, section: str, token: str) -> None:
        self[section]["token"] = token

    def get_webhook_url(self, section: str) -> str | None:
        return self[section]["webhook_url"]

    def set_webhook_url(self, section: str, webhook_url: str) -> None:
        self[section]["webhook_url"] = webhook_url

    def get_username(self, section: str) -> str | None:
        return self[section]["username"]

    def set_username(self, section: str, username: str) -> None:
        self[section]["username"] = username

    def get_avatar_url(self, section: str) -> str | None:
        return self[section]["avatar_url"]

    def set_avatar_url(self, section: str, avatar_url: str) -> None:
        self[section]["avatar_url"] = avatar_url

    def get_directory_basename(self) -> str:
        return Path(self._path).parent.name

    def get_webhook_sections(self) -> list[str]:
        return [
            section
            for section in self.sections()
            if DISCORD_WEBHOOK_SECTION_KEYWORD in section
        ]

    def get_webhook_options(self) -> dict[str, DiscordWebhookOptions]:
        return {
            section: DiscordWebhookOptions(
                webhook_url=self[section]["webhook_url"],
                username=self[section]["username"],
                avatar_url=self[section]["avatar_url"],
            )
            for section in self.sections()
            if DISCORD_WEBHOOK_SECTION_KEYWORD in section
        }

    def _initialize(self) -> None:
        # load and create if not exists
        try:
            self.load()
        except FileNotFoundError:
            self._create()

    def _create(self) -> None:
        options = (
            (
                DISCORD_SECTION_DEFAULT,
                ["channel_id", "token"],
            ),
            (
                DISCORD_WEBHOOK_SECTION_DEFAULT,
                ["webhook_url", "username", "avatar_url"],
            ),
        )
        for section, ops in options:
            self.add_section(section)
            self[section] = {o: "" for o in ops}
        self.save(chmod=0o777, create_directory=True)


class DiscordNotifier(Notifier):
    def __init__(self, config: DiscordConfig) -> None:
        self._config = config
        self._default_username = self._make_default_username()
        self._sections = self._config.get_webhook_sections()
        self._options = self._config.get_webhook_options()
        self._last_responses = self._fetch_statuses()

    @property
    def keys(self) -> list[str]:
        return self._sections

    @property
    def has_error(self) -> bool:
        return any(
            400 <= response.status_code < 500
            for response in self._last_responses
            if response is not None
        )

    def notify(
        self,
        message: str | None = None,
        image: RawImage | None = None,
        keys: list[str] | None = None,
    ) -> None:
        if not (targets := keys if keys is not None else self._sections):
            logger.error(f"有効なkeysを指定してください。(keys={keys})")
            return

        for response_index, section in enumerate(self._sections):
            if section not in targets:
                logger.warning(f"[Discord]無効なkey({section})")
                continue

            try:
                self._notify(
                    response_index=response_index,
                    key=section,
                    message=message,
                    image=image,
                )
            except Exception:
                logger.error("webhook_urlを確認してください。")

    def get_late_limits(self) -> list[RateLimit]:
        return [
            RateLimit(
                key=key,
                limit=response.headers.get("X-RateLimit-Limit"),
                remaining=response.headers.get("X-RateLimit-Remaining"),
                reset_time=self._time(response.headers.get("X-RateLimit-Reset")),
            )
            for key, response in zip(self._sections, self._last_responses)
            if response is not None
        ]

    def apply_config(self) -> None:
        self._sections = self._config.get_webhook_sections()
        self._options = self._config.get_webhook_options()
        self._last_responses = self._fetch_statuses()

    def _fetch_statuses(self) -> list[requests.Response]:
        return [requests.get(self._options[key].webhook_url) for key in self._sections]

    def _make_default_username(self) -> str:
        return f"Poke-Controller (profile: {self._get_profile_name()})"

    def _get_profile_name(self) -> str:
        return self._config.get_directory_basename()

    def _notify(
        self,
        response_index: int,
        key: str,
        message: str | None = None,
        image: RawImage | None = None,
    ) -> None:
        files = self._make_files(key=key, message=message, image=image)
        self._last_responses[response_index] = response = requests.post(
            url=self._options[key].webhook_url,
            files=files,
        )
        self._log_response(
            response=response,
            message=message,
            image=image,
        )

    def _make_files(
        self,
        key: str,
        message: str | None,
        image: RawImage | None,
    ) -> dict[str, Any]:
        payload = self._make_payload(key=key, message=message)
        files: dict[str, Any] = {"payload_json": (None, json.dumps(payload))}
        if image is not None:
            files["media"] = ("pokecon_image.png", to_bytes(image, fmt="png"))
        return files

    def _make_payload(self, key: str, message: str | None) -> dict[str, str]:
        payload: dict[str, str] = {
            "username": self._options[key].username or self._default_username,
            "content": message or "",
        }
        if avatar_url := self._options[key].avatar_url:
            payload["avatar_url"] = avatar_url
        return payload

    def _log_response(
        self,
        response: requests.Response,
        message: str | None,
        image: RawImage | None,
    ) -> None:
        data_type, data_type_jpn = self._make_send_data_type(message, image)
        if (status_code := response.status_code) in [200, 204]:
            logger.info(f"{data_type_jpn}を送信しました。")
        else:
            logger.info(f"{data_type_jpn}の送信に失敗しました。({status_code})")

    # noinspection PyMethodMayBeStatic
    def _make_send_data_type(
        self,
        message: str | None,
        image: RawImage | None,
    ) -> tuple[str, str]:
        if message is not None and image is not None:
            return "テキスト・画像", "Text & Image"
        elif message is not None:
            return "テキスト", "Text"
        elif image is not None:
            return "画像", "Image"
        else:
            return "(empty)", "empty"

    # noinspection PyMethodMayBeStatic
    def _time(self, timestamp: str | None) -> str | None:
        return str(from_timestamp(int(timestamp), 9)) if timestamp else None
