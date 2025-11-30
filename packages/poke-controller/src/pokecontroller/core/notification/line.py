import logging
from typing import Any

import requests

from ..config import Config
from ..datetime import from_timestamp
from ..image import RawImage, to_bytes
from .notifier import Notifier, RateLimit

logger = logging.getLogger(__name__)

LINE_API_URL_BASE = "https://notify-api.line.me/api"
LINE_STATUS_API_URL = f"{LINE_API_URL_BASE}/status"
LINE_NOTIFY_API_URL = f"{LINE_API_URL_BASE}/notify"


class LineConfig(Config):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self._initialize()

    def get_token(self, option: str) -> str | None:
        return self["LINE"][option]

    def set_token(self, option: str, value: str) -> None:
        self["LINE"][option] = value

    def get_tokens(self) -> dict[str, str]:
        return self.options("LINE")

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


class LineNotifier(Notifier):
    def __init__(self, config: LineConfig):
        self._config = config
        self._tokens = self._config.get_tokens()
        self._token_keys = list(self._tokens.keys())
        self._headers_list = self._make_headers_list()
        self._last_responses = self._fetch_statuses()

    @property
    def keys(self) -> list[str]:
        return list(self._tokens.keys())

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
        if not (targets := keys if keys is not None else self._token_keys):
            logger.error("有効なkeysを指定してください")
            return

        for response_index, key in enumerate(self._token_keys):
            if key not in targets:
                continue

            try:
                self._notify(
                    response_index=response_index,
                    key=key,
                    message=message,
                    image=image,
                )
            except Exception:
                logger.error("tokenを確認してください。")

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
            for key, response in zip(self._token_keys, self._last_responses)
            if response is not None
        ]

    def apply_config(self) -> None:
        self._tokens = self._config.get_tokens()
        self._token_keys = list(self._tokens.keys())
        self._headers_list = self._make_headers_list()
        self._last_responses = self._fetch_statuses()

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

    def _notify(
        self,
        response_index: int,
        key: str,
        message: str | None = None,
        image: RawImage | None = None,
    ) -> None:
        params = self._make_params(message=message)
        files = self._make_files(image=image)
        headers = self._make_headers(token=key)
        self._last_responses[response_index] = response = requests.post(
            url=LINE_NOTIFY_API_URL,
            headers=headers,
            params=params,
            files=files,
        )
        self._log_response(
            response=response,
            message=message,
            image=image,
        )

    # noinspection PyMethodMayBeStatic
    def _make_params(self, message: str | None) -> dict[str, Any]:
        return {"message": message if message is not None else ""}

    # noinspection PyMethodMayBeStatic
    def _make_files(self, image: RawImage | None) -> dict[str, Any] | None:
        return {"imageFile": to_bytes(image, fmt="png")} if image is not None else None

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
            logger.error(f"{data_type_jpn}の送信に失敗しました。({status_code})")

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
