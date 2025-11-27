from typing import Any

import requests

from ..config import Config
from ..datetime import from_timestamp
from ..image import RawImage, to_bytes
from .notifier import Notifier, RateLimit

LINE_API_URL_BASE = "https://notify-api.line.me/api"
LINE_STATUS_API_URL = f"{LINE_API_URL_BASE}/status"
LINE_NOTIFY_API_URL = f"{LINE_API_URL_BASE}/notify"


class LineConfig(Config):
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
        # set default token
        self.set_token("token", "")
        self.save(chmod=0o777, create_directory=True)

    def get_token(self, key: str) -> str | None:
        return self.get("LINE", key)

    def set_token(self, key: str, value: str) -> None:
        self.set("LINE", key, value)

    def get_tokens(self) -> dict[str, str]:
        return self.read_dict("LINE")


class LineNotifier(Notifier):
    def __init__(self, config_path: str):
        self._config = LineConfig(config_path)
        self._tokens = self._config.get_tokens()
        self._token_keys = list(self._tokens.keys())
        self._headers_list = self._make_headers_list()
        self._statuses = self._fetch_statuses()
        self._status_codes = self._make_status_codes()
        self._status_jsons = self._make_status_jsons()
        self._last_response: requests.Response | None = None

    def notify(
        self,
        message: str | None = None,
        image: RawImage | None = None,
        keys: list[str] | None = None,
    ) -> None:
        token = self._config.get_token(keys[0] if keys else "token")
        if token is None:
            # FIXME: logging
            print("[LINE]tokenが存在しません。")
            return

        params = {"Message": message}
        files = {"imageFile": to_bytes(image)} if image is not None else None

        if files:
            send_data_type = "テキスト・画像"
            _send_data_type_eng = "Text & Image"
            response = requests.post(
                LINE_NOTIFY_API_URL,
                headers=self._make_headers(token),
                params=params,
                files=files,
            )
        else:
            send_data_type = "テキスト"
            _send_data_type_eng = "Text"
            response = requests.post(
                LINE_NOTIFY_API_URL, headers=self._make_headers(token), params=params
            )
        self._last_response = response
        if response.status_code == 200:
            # FIXME: logging
            print(f"[LINE]{send_data_type}を送信しました。")
        else:
            # FIXME: logging
            print(f"[LINE]{send_data_type}の送信に失敗しました。")

    def get_late_limits(self) -> list[RateLimit]:
        return [
            RateLimit(
                key=self._token_keys[i],
                limit=response.headers.get("X-RateLimit-Limit"),
                remaining=response.headers.get("X-RateLimit-Remaining"),
                image_limit=response.headers.get("X-RateLimit-ImageLimit"),
                image_remaining=response.headers.get("X-RateLimit-ImageRemaining"),
                reset_time=self._time(response.headers.get("X-RateLimit-Reset")),
            )
            for i, response in enumerate(self._statuses)
        ]

    def _make_headers_list(self) -> list[dict[str, str]]:
        return [
            {"Authorization": f"Bearer {self._tokens[key]}"} for key in self._token_keys
        ]

    # noinspection PyMethodMayBeStatic
    def _make_headers(self, token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    def _fetch_statuses(self) -> list[requests.Response]:
        return [
            requests.get(LINE_STATUS_API_URL, headers=headers)
            for headers in self._headers_list
        ]

    def _make_status_codes(self) -> list[int]:
        return [response.status_code for response in self._statuses]

    def _make_status_jsons(self) -> list[Any]:
        return [response.json() for response in self._statuses]

    # noinspection PyMethodMayBeStatic
    def _time(self, timestamp: str | None) -> str | None:
        return str(from_timestamp(int(timestamp), 9)) if timestamp else None
