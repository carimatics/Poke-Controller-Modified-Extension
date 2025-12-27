#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations  # 3.7向け。廃止したい。

import os
from typing import List, Optional
from Commands.PythonCommandBase import ImageProcPythonCommand

"""
PokeCon橋渡し用関数
PokeCon Modified版とExtension版で処理を切り替える関数を定義する。(主にprint系)
developed by フウ
"""
# initにてPokeConの種類を判定する。


def remove_next_item(dialogue_list):
    dialogue_list_out = []
    for widget_list in dialogue_list:
        if widget_list[0].casefold() == "next".casefold():
            pass
        else:
            dialogue_list_out.append(widget_list)
    return dialogue_list_out


class BridgeFunctions(object):
    def __init__(self, commands):
        self.commands = commands
        self.is_extension = os.path.exists("Constant.py")
        if not self.is_extension and not hasattr(
            self.commands.__class__, "dialogue6widget"
        ):  # 継承している関数にdialogue6widget関数が含まれるか? dialogue6widget関数はmodified版/extension版のみ。
            print("本家PokeConでは実行できません。\nまたは古いVersionのPokeConを使用しており更新が必要です。")

    def check_pokecon_extension(self) -> bool:
        """
        Poke-Controller Modified Extensionであるかを確認
        True: Poke-Controller Modified Extension
        False: Poke-Controller Modified
        None: Poke-Controller(本家)
        """
        return self.is_extension

    def get_profile_name(self) -> str:
        """
        profile名を取得
        Extension版: profilename、Modified版/本家""
        """
        return ImageProcPythonCommand.profilename if self.is_extension else ""

    # Template画像のディレクトリを変更する。extension版であることかつ指定したディレクトリが存在する場合に実施。
    def set_template_directory(self, name1: str, name2: str) -> None:
        """
        テンプレートファイルのディレクトリ指定
        """
        if self.is_extension and os.path.isdir(os.path.join(name1, name2)):
            self.commands.setTemplateDir(name1 + "/")

    # Template画像のディレクトリを取得する。
    def get_template_directory(self) -> str:
        """
        テンプレートファイルのディレクトリ指定
        """
        return ImageProcPythonCommand.template_path_name if self.is_extension else "./Template/"

    # print関数。extension版の場合は関数によって上書きしたり、追記したりすることが可能。
    def bf_print(self, *objects: object, sep: str = " ", end: str = "\n") -> None:
        """
        print出力(上書きなし)
        """
        if self.is_extension:
            self.commands.print_tbs("a", *objects, sep=sep, end=end)
        else:
            print(*objects, sep=sep, end=end)

    def bf_print_w(self, *objects: object, sep: str = " ", end: str = "\n"):
        """
        print出力(上書き)
        """
        if self.is_extension:
            self.commands.print_tb("w", *objects, sep=sep, end=end)
        else:
            print(*objects, sep=sep, end=end)

    def bf_print_a(self, *objects: object, sep: str = " ", end: str = "\n"):
        """
        print出力(追記)
        """
        if self.is_extension:
            self.commands.print_tb("a", *objects, sep=sep, end=end)
        else:
            print(*objects, sep=sep, end=end)

    def bf_isContainTemplate(
        self,
        template_path: str,
        threshold: float = 0.7,
        use_gray: bool = True,
        show_value: bool = False,
        show_position: bool = True,
        show_only_true_rect: bool = True,
        ms: float = 2000,
        crop_fmt: int | str = "",
        crop: List[int] = [],
        mask_path: str = None,
        use_gpu: bool = False,
        BGR_range: Optional[dict] = None,
        threshold_binary: Optional[int] = None,
        crop_template: List[int] = [],
        show_image: bool = False,
        color: List[str] = ["blue", "red", "orange"],
    ) -> bool:
        if self.is_extension:
            return self.commands.isContainTemplate(
                template_path,
                threshold=threshold,
                use_gray=use_gray,
                show_value=show_value,
                show_position=show_position,
                show_only_true_rect=show_only_true_rect,
                ms=ms,
                crop_fmt=crop_fmt,
                crop=crop,
                mask_path=mask_path,
                use_gpu=use_gpu,
                BGR_range=BGR_range,
                threshold_binary=threshold_binary,
                crop_template=crop_template,
                show_image=show_image,
                color=color,
            )
        else:
            return self.commands.isContainTemplate(
                template_path,
                threshold=threshold,
                use_gray=use_gray,
                show_value=show_value,
                show_position=show_position,
                show_only_true_rect=show_only_true_rect,
                ms=ms,
                crop=crop,
                mask_path=mask_path,
            )

    def bf_isContainTemplate_max(
        self,
        template_path_list: List[str],
        threshold: float = 0.7,
        use_gray: bool = True,
        show_value: bool = False,
        show_position: bool = True,
        show_only_true_rect: bool = True,
        ms: float = 2000,
        crop_fmt: int | str = "",
        crop: List[int] = [],
        mask_path_list: List[str] = [],
        BGR_range: Optional[dict] = None,
        threshold_binary: Optional[int] = None,
        crop_template: List[int] = [],
        show_image: bool = False,
        color: List[str] = ["blue", "red", "orange"],
    ) -> any:
        if self.is_extension:
            max_idx, max_val_list, judge_list = self.commands.isContainTemplate_max(
                template_path_list,
                threshold=threshold,
                use_gray=use_gray,
                show_value=show_value,
                show_position=show_position,
                show_only_true_rect=show_only_true_rect,
                ms=ms,
                crop_fmt=crop_fmt,
                crop=crop,
                mask_path_list=mask_path_list,
                BGR_range=BGR_range,
                threshold_binary=threshold_binary,
                crop_template=crop_template,
                show_image=show_image,
                color=color,
            )
        else:
            max_idx, max_val_list, judge_list = self.commands.isContainTemplate_max(
                template_path_list,
                threshold=threshold,
                use_gray=use_gray,
                show_value=show_value,
                show_position=show_position,
                show_only_true_rect=show_only_true_rect,
                ms=ms,
                crop=crop,
            )

        return max_idx, max_val_list, judge_list

    def bf_dialogue(self, title: str, message: list | str, desc: str = None, need: type = list) -> list | dict:
        """
        ダイアログ関数(Entryのみ)
        ※Modified版の場合はdescなし
        """
        if self.is_extension:
            ret = self.commands.dialogue(title, message, desc=desc, need=need)
        else:
            ret = self.commands.dialogue(title, message, need=need)
        return ret

    def bf_dialogue6widget(self, title: str, dialogue_list: list, desc: str = None, need: type = list) -> list | dict:
        """
        ダイアログ関数(6widget)
        ※Modified版の場合は["Next"]を削除する。
        """
        if self.is_extension:
            ret = self.commands.dialogue6widget(title, dialogue_list, desc=desc, need=need)
        else:
            dialogue_list = remove_next_item(dialogue_list)
            ret = self.commands.dialogue6widget(title, dialogue_list, need=need)
        return ret

    def bf_dialogue6widget_save_settings(
        self, title: str, dialogue_list: list, filename: str, desc: str = None, need: type = list
    ) -> list | dict:
        """
        設定保存機能付きダイアログ関数
        ※Modified版の場合は通常のダイアログ関数が起動する。
        filename: 設定ファイル名。絶対パス。
        """
        if self.is_extension:
            ret = self.commands.dialogue6widget_save_settings(title, dialogue_list, filename, desc=desc, need=need)
        else:
            dialogue_list = remove_next_item(dialogue_list)
            ret = self.commands.dialogue6widget(title, dialogue_list, need=need)
        return ret

    def bf_dialogue6widget_select_settings(
        self, title: str, dialogue_list: list, dirname: str, desc: str = None, need: type = list
    ) -> list | dict:
        """
        設定選択機能付きダイアログ関数
        ※Modified版の場合は通常のダイアログ関数が起動する。
        dirname: 設定ファイルを保存するディレクトリ名。絶対パス。
        """
        if self.is_extension:
            ret = self.commands.dialogue6widget_select_settings(title, dialogue_list, dirname, desc=desc, need=need)
        else:
            dialogue_list = remove_next_item(dialogue_list)
            ret = self.commands.dialogue6widget(title, dialogue_list, need=need)
        return ret

    def bf_show_informations(
        self, name: str, developer: str | list, contributor: str | list = None, description: str = None
    ):
        """
        プログラムの詳細情報を表示する
        name | str: プログラム名
        developer | str/list: 開発者名(複数の場合はリストでinputする)
        contributor | str/list: 貢献者名(複数の場合はリストでinputする)
        description | str: 概要
        """
        developers = ", ".join(developer) if isinstance(developer, list) else developer

        text = "---------------------------------------------\n"

        if self.is_extension:
            name = name[: -(len(name.split("(")[-1]) + 1)]

        text += f"Name: {name}\nDeveloper: {developers}\n"

        if contributor:
            contributors = ", ".join(contributor) if isinstance(contributor, list) else contributor
            text += f"Contributor: {contributors}\n"

        if description:
            text += f"Description: {description}\n"

        text += "---------------------------------------------"

        self.bf_print(text)
