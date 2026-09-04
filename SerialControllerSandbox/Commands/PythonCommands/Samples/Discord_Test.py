#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import ImageProcPythonCommand


class DiscordTest(ImageProcPythonCommand):
    NAME = "Discord通知テスト"

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        # テキストのみ
        print("テキストのみ")
        self.discord_text("テキストのみ")

        # 画像のみ
        print("画像のみ")
        self.discord_image()

        # テキスト+画像
        print("テキスト+画像")
        self.discord_image("テキスト+画像")
