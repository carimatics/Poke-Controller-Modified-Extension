#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import ImageProcPythonCommand
from Commands.PythonCommands.bridge_functions.bridge_functions import BridgeFunctions
import os


class BridgeFunctionsSample(ImageProcPythonCommand):
    NAME = "PokeCon橋渡し関数サンプル ver. 0.1.0"
    TAGS = ["Sample"]

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        # クロスプラットフォーム用クラス
        self.bf = BridgeFunctions(self)

        # プログラム情報の表示
        developer = "(名前)"
        self.bf.bf_show_informations(self.NAME, developer)

        # テンプレートファイルディレクトリの設定
        self.bf.set_template_directory(
            os.path.join(os.path.dirname(__file__)), "sample_image_path"
        )

        # 履歴保存用ファイル
        settings_file = os.path.join(
            os.path.dirname(__file__), "sample_setting_path1/setting.json"
        )

        # ダイアログ呼び出し(前回の値を初期値とする)
        ret = self.bf.bf_dialogue6widget_save_settings(
            "config",
            [["Entry", "テスト1", 1]],
            settings_file,
            desc="テスト用ウィジェット",
        )

        # 表示する
        self.bf.bf_print(f"ウィジェット1結果:{ret[0]}")

        # 履歴保存用ディレクトリ
        settings_dir = os.path.join(os.path.dirname(__file__), "sample_setting_path2")

        # ダイアログ呼び出し(保存した値を選択して呼び出す))
        ret = self.bf.bf_dialogue6widget_select_settings(
            "config",
            [["Combo", "テスト2", ["A", "B", "C"], "(n/a)"]],
            settings_dir,
            desc="テスト用ウィジェット2",
        )

        # 表示する
        self.bf.bf_print_w(f"ウィジェット2結果:{ret[0]}")
