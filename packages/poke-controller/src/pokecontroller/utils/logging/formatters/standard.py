import logging


class StandardFormatter(logging.Formatter):
    """ライブラリの標準フォーマッター"""

    def format(self, record: logging.LogRecord) -> str:
        """ログレコードをフォーマット"""

        extended_attr = ["class"]
        for attr in extended_attr:
            if not hasattr(record, attr):
                setattr(record, attr, "")

        return super().format(record)
