import json
from typing import Any

import requests

from ..config import Config
from ..datetime import from_timestamp
from ..image import RawImage, to_bytes
from ..path import basename, directory_name, to_absolute
from .notifier import Notifier, RateLimit

DISCORD_SECTION_DEFAULT = "DISCORD"
DISCORD_WEBHOOK_SECTION_DEFAULT = "DISCORD_WEBHOOK"
DISCORD_WEBHOOK_SECTION_KEYWORD = "DISCORD_WEBHOOK"


class DiscordConfig(Config):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self._initialize()

    def _initialize(self) -> None:
        # load and create if not exists
        try:
            self.load()
        except FileNotFoundError:
            self._create()

    def _create(self) -> None:
        # set default values
        self.set_default_channel_id("")
        self.set_default_token("")
        self.set_default_webhook_url("")
        self.set_default_username("")
        self.set_default_avatar_url("")
        self.save(chmod=0o777, create_directory=True)

    def set_default_channel_id(self, channel_id: str) -> None:
        self.set_channel_id(DISCORD_SECTION_DEFAULT, channel_id)

    def set_default_token(self, token: str) -> None:
        self.set_token(DISCORD_SECTION_DEFAULT, token)

    def set_default_webhook_url(self, webhook_url: str) -> None:
        self.set_webhook_url(DISCORD_WEBHOOK_SECTION_DEFAULT, webhook_url)

    def set_default_username(self, username: str) -> None:
        self.set_username(DISCORD_WEBHOOK_SECTION_DEFAULT, username)

    def set_default_avatar_url(self, avatar_url: str) -> None:
        self.set_avatar_url(DISCORD_WEBHOOK_SECTION_DEFAULT, avatar_url)

    def get_channel_id(self, section: str) -> str | None:
        return self.get(section, "channel_id")

    def set_channel_id(self, section: str, channel_id: str) -> None:
        self.set(section, "channel_id", channel_id)

    def get_token(self, section: str) -> str | None:
        return self.get(section, "token")

    def set_token(self, section: str, token: str) -> None:
        self.set(section, "token", token)

    def get_webhook_url(self, section: str) -> str | None:
        return self.get(section, "webhook_url")

    def set_webhook_url(self, section: str, webhook_url: str) -> None:
        self.set(section, "webhook_url", webhook_url)

    def get_username(self, section: str) -> str | None:
        return self.get(section, "username")

    def set_username(self, section: str, username: str) -> None:
        self.set(section, "username", username)

    def get_avatar_url(self, section: str) -> str | None:
        return self.get(section, "avatar_url")

    def set_avatar_url(self, section: str, avatar_url: str) -> None:
        self.set(section, "avatar_url", avatar_url)

    def get_directory_basename(self) -> str:
        return basename(directory_name(self._path))

    def get_webhook_keys(self) -> list[str]:
        return [
            key for key in self.sections() if DISCORD_WEBHOOK_SECTION_KEYWORD in key
        ]

    def get_webhook_urls(self) -> dict[str, str]:
        return self._get_options_of_webhook_sections("webhook_url")

    def get_webhook_usernames(self) -> dict[str, str]:
        return self._get_options_of_webhook_sections("username")

    def get_webhook_avatar_url(self) -> dict[str, str]:
        return self._get_options_of_webhook_sections("avatar_url")

    def _get_options_of_webhook_sections(self, option: str) -> dict[str, str]:
        """
        `DISCORD_WEBHOOK` という文字列が含まれるセクションの指定された `option` を辞書形式で取得します。
        キーはセクション名、値は対応する `option` です。
        """
        return {
            section: self.get(section, option) or ""
            for section in self.sections()
            if DISCORD_WEBHOOK_SECTION_KEYWORD in section
        }


class DiscordNotifier(Notifier):
    def __init__(self, config_path: str) -> None:
        self._config = DiscordConfig(config_path)
        self._default_username = self._make_default_username()
        self._sections = self._config.sections()
        self._webhook_keys = self._config.get_webhook_keys()
        self._webhook_urls = self._config.get_webhook_urls()
        self._usernames = self._config.get_webhook_usernames()
        self._avatar_urls = self._config.get_webhook_avatar_url()
        self._statuses = self._fetch_statuses()
        self._status_codes = self._make_status_codes()
        self._status_jsons = self._make_status_jsons()
        self._last_response: list[requests.Response | None] = [None] * len(
            self._webhook_keys
        )

    def notify(
        self,
        message: str | None = None,
        image: RawImage | None = None,
        keys: list[str] | None = None,
    ) -> None:
        if not keys:
            # FIXME: logging
            print("[Discord]keysを指定してください")
            return

        for i, key in enumerate(self._webhook_keys):
            if key not in keys:
                continue

            try:
                payload: dict[str, str] = {
                    "username": self._config.get_username(key)
                    or self._default_username,
                    "content": message or "",
                }
                if avatar_url := self._config.get_avatar_url(key):
                    payload["avatar_url"] = avatar_url

                files: dict[str, Any] = {"payload_json": (None, json.dumps(payload))}
                if image is not None:
                    files["media"] = ("pokecon_image.png", to_bytes(image))

                if message is not None and image is not None:
                    send_data_type = "テキスト・画像"
                    _send_data_type_eng = "Text & Image"
                elif message is not None:
                    send_data_type = "テキスト"
                    _send_data_type_eng = "Text"
                elif image is not None:
                    send_data_type = "画像"
                    _send_data_type_eng = "Image"
                else:
                    send_data_type = "(empty)"
                    _send_data_type_eng = "empty"

                self._last_response[i] = res = requests.post(
                    self._webhook_urls[key], files=files
                )

                if res.status_code in [200, 204]:
                    # FIXME: logging
                    print(f"[Discord({key})]{send_data_type}を送信しました。")
                else:
                    # FIXME: logging
                    print(
                        f"[Discord({key})]{send_data_type}の送信に失敗しました。({res.status_code})"
                    )

            except Exception:
                # FIXME: logging
                print(f"[Discord({key})]webhook_urlを確認してください。")

    def get_late_limits(self) -> list[RateLimit]:
        return [
            RateLimit(
                key=key,
                limit=response.headers.get("X-RateLimit-Limit"),
                remaining=response.headers.get("X-RateLimit-Remaining"),
                image_limit=response.headers.get("X-RateLimit-ImageLimit"),
                image_remaining=response.headers.get("X-RateLimit-ImageRemaining"),
                reset_time=self._time(response.headers.get("X-RateLimit-Reset")),
            )
            for key, response in zip(self._webhook_keys, self._last_response)
            if response is not None
        ]

    def _fetch_statuses(self) -> list[requests.Response]:
        return [requests.get(self._webhook_urls[key]) for key in self._webhook_keys]

    def _make_status_codes(self) -> list[int]:
        return [status.status_code for status in self._statuses]

    def _make_status_jsons(self) -> list[Any]:
        return [response.json() for response in self._statuses]

    def _make_default_username(self) -> str:
        return f"Poke-Controller Modified Extension (profile: {self._config.get_directory_basename()})"

    # noinspection PyMethodMayBeStatic
    def _time(self, timestamp: str | None) -> str | None:
        return str(from_timestamp(int(timestamp), 9)) if timestamp else None
