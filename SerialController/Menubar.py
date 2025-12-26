#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import cv2
import tkinter as tk
from tkinter import messagebox
import os
import configparser
import shutil

from KeyConfig import PokeKeycon
from LineNotify import Line_Notify
from DiscordNotify import Discord_Notify
from get_pokestatistics import GetFromHomeGUI
from PokeConShowInfo import PokeConQuestionDialogue, PokeConVersionCheck, PokeConChangeLog, PokeConCopyright
from PokeConUpdateChecker import PokeConUpdateCheck
from PokeConDialogue import PokeConDialogue
from logging import getLogger, DEBUG, NullHandler
import webbrowser


class PokeController_Menubar(tk.Menu):
    def __init__(self, master, **kw):
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.master = master
        self.pokeconname = self.master.pokeconname
        self.pokeconversion = self.master.pokeconversion
        self.root = self.master.root
        self.ser = self.master.ser
        self.preview = self.master.preview
        self.show_size_cb = self.master.show_size_cb
        self.keyboard = self.master.keyboard
        self.settings = self.master.settings
        self.camera = self.master.camera
        self.profile = self.master.profile
        self.cur_command = self.master.cur_command

        self.poke_treeview = None
        self.key_config = None
        self.line = None
        self.discord = None

        tk.Menu.__init__(self, self.root, **kw)
        self.menu = tk.Menu(self, tearoff="false")
        self.menu_command = tk.Menu(self, tearoff="false")
        self.add(tk.CASCADE, menu=self.menu, label="メニュー")

        self.help = tk.Menu(self, tearoff="false")
        self.add(tk.CASCADE, menu=self.help, label="ヘルプ")
        self.help.add("command", label="Github", command=self.OpenGithub)
        self.help.add("command", label="Poke-Controller Guide", command=self.OpenGuide)
        self.help.add("command", label="質問テンプレート", command=self.output_question)
        self.help.add("command", label="Version確認", command=self.CheckVersion)
        self.help.add("command", label="更新履歴表示", command=self.OpenChangeLog)
        self.help.add("command", label="アップデート確認", command=self.CheckUpdate)
        self.help.add("command", label="LICENSE", command=self.OpenLicense)

        self.menu.add(tk.CASCADE, menu=self.menu_command, label="コマンド")

        self.menu.add("separator")
        self.menu.add("command", label="設定(dummy)")
        # TODO: setup command_id_arg 'false' for menuitem.
        self.menu.add("command", command=self.exit, label="終了")

        self.AssignMenuCommand()
        self.LineTokenSetting()
        self.DiscordSetting()

    # TODO: setup command_id_arg 'false' for menuitem.

    def AssignMenuCommand(self):
        self._logger.debug("Assigning menu command")
        self.menu_command.add("command", command=self.LineTokenAssignment, label="LINE Token Assignment")
        self.menu_command.add("command", command=self.LineTokenSetting, label="LINE Token Check")
        self.menu_command.add("command", command=self.DiscordSettingAssignment, label="Discord Setting Assignment")
        self.menu_command.add("command", command=self.DiscordSetting, label="Discord Check")
        self.menu_command.add("command", command=self.GenerateNewBat, label="Generate Bat File & Profile Directory")
        # TODO: setup command_id_arg 'false' for menuitem.
        self.menu_command.add("command", command=self.OpenPokeHomeCoop, label="Pokemon Home 連携")
        self.menu_command.add("command", command=self.OpenKeyConfig, label="キーコンフィグ")
        self.menu_command.add("command", command=self.ResetWindowSize, label="画面サイズのリセット")

    # TODO: setup command_id_arg 'false' for menuitem.

    def OpenPokeHomeCoop(self):
        self._logger.debug("Open Pokemon home cooperate window")
        if self.poke_treeview is not None:
            self.poke_treeview.focus_force()
            return

        window2 = GetFromHomeGUI(self.root, self.settings.season, self.settings.is_SingleBattle)
        window2.protocol("WM_DELETE_WINDOW", self.closingGetFromHome)
        self.poke_treeview = window2

    def closingGetFromHome(self):
        self._logger.debug("Close Pokemon home cooperate window")
        self.poke_treeview.destroy()
        self.poke_treeview = None

    def is_utf8_file_with_bom(self, filename):
        """
        utf-8 ファイルが BOM ありかどうかを判定する
        """
        line_first = open(filename, encoding="utf-8").readline()
        return line_first[0] == "\ufeff"

    def LineTokenAssignment(self):
        self.message_dialogue = tk.Toplevel()
        ret = PokeConDialogue(self.message_dialogue, "Line Token Assignment", "Token").ret_value(list)
        self.message_dialogue = None
        if ret != []:
            token_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "profiles", self.profile, "line_token.ini"
            )
            token_file = configparser.ConfigParser(comment_prefixes="#", allow_no_value=True)
            token_file["LINE"] = {"token": ret[0]}
            with open(token_path, "w", encoding="utf-8") as file:
                token_file.write(file)
            os.chmod(path=token_path, mode=0o777)
            self._logger.debug("Assign Line Token")
            self.LineTokenSetting()
        else:
            pass

    def DiscordSettingAssignment(self):
        self.message_dialogue = tk.Toplevel()
        ret = PokeConDialogue(
            self.message_dialogue, "Discord Setting Assignment", ["Webhook URL", "Username", "Avatar URL"]
        ).ret_value(list)
        self.message_dialogue = None
        if not all([i == "" for i in ret]):
            setting_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "profiles", self.profile, "discord_token.ini"
            )

            is_with_bom = self.is_utf8_file_with_bom(setting_path)
            encoding = "utf-8-sig" if is_with_bom else "utf-8"

            setting_file = configparser.ConfigParser(comment_prefixes="#", allow_no_value=True)
            setting_file.read(setting_path, encoding)

            setting_file.read(setting_path, encoding)
            setting_file["DISCORD_WEBHOOK"] = {
                "webhook_url": ret[0],
                "username": ret[1],
                "avatar_url": ret[2],
            }
            with open(setting_path, "w", encoding="utf-8") as file:
                setting_file.write(file)
            os.chmod(path=setting_path, mode=0o777)
            self._logger.debug("Assign Discord Webhook Setting")
            self.DiscordSetting()
        else:
            pass

    def LineTokenSetting(self):
        self._logger.debug("Show line API")
        if self.line is None:
            try:
                self.line = Line_Notify()
                print(self.line)
                self.line.getRateLimit()
            except Exception:
                pass
        self.line = None
        # LINE.send_text_n_image("CAPTURE")

    def DiscordSetting(self):
        self._logger.debug("Show Discord Webhook API")
        if self.discord is None:
            self.discord = Discord_Notify()
        try:
            print(self.discord)
            self.discord.getRateLimit()
        except Exception:
            print("DISCORD API Check: N/A")
        self.discord = None

    def GenerateNewBat(self):
        self.message_dialogue = tk.Toplevel()
        ret = PokeConDialogue(
            self.message_dialogue,
            "Generate Bat File & Profile Directory",
            [["Entry", "Profile Name", ""], ["Check", "Copy Profile", True]],
            mode=1,
        ).ret_value(list)
        self.message_dialogue = None
        if ret != []:
            exe_path = os.path.join(
                os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)),
                f"ExecutePokeConModified-Extension_{ret[0]}.bat",
            )
            if not os.path.exists(exe_path):
                txt = f"python SerialController/PokeConUpdateChecker.py\ncd SerialController\npython Window.py --profile {ret[0]}\npause\n"
                with open(exe_path, "w", encoding="utf-8") as file:
                    file.write(txt)
            else:
                pass
            new_profile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles", ret[0])
            if not os.path.exists(new_profile_path):
                if ret[1]:
                    current_profile_path = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "profiles", self.profile
                    )
                    shutil.copytree(current_profile_path, new_profile_path)
                else:
                    pass
            else:
                pass
        else:
            pass

    def OpenKeyConfig(self):
        self._logger.debug("Open KeyConfig window")
        if self.key_config is not None:
            self.key_config.focus_force()
            return

        kc_window = PokeKeycon(self.root)
        kc_window.protocol("WM_DELETE_WINDOW", self.closingKeyConfig)
        self.key_config = kc_window

    def closingKeyConfig(self):
        self._logger.debug("Close KeyConfig window")
        self.key_config.destroy()
        self.key_config = None

    def ResetWindowSize(self):
        self._logger.debug("Reset window size")
        self.preview.setShowsize(360, 640)
        self.show_size_cb.current(0)

    def OpenGithub(self):
        webbrowser.open("https://github.com/futo030/Poke-Controller-Modified-Extension", 2)

    def OpenGuide(self):
        webbrowser.open("https://pokecontroller.info/", 2)

    def CheckVersion(self):
        PokeConVersionCheck(tk.Toplevel(), self.pokeconname, self.pokeconversion)

    def OpenChangeLog(self):
        PokeConChangeLog(tk.Toplevel())

    def CheckUpdate(self):
        window = tk.Toplevel()
        window.withdraw()  # メインウィンドウを非表示にする
        res = messagebox.askyesno(title="更新確認", message="Poke-Controller Modified Extension の更新を確認しますか?")
        if res:
            res_check = PokeConUpdateCheck().check_repository_updates()
            if res_check == "0":
                res = tk.messagebox.showinfo(title="更新確認", message="更新はありませんでした。")
            elif res_check == "1":
                res = tk.messagebox.showinfo(
                    title="更新確認", message="最新版が公開されています。Githubのページを開きます。"
                )
                self.OpenGithub()
            else:
                res = tk.messagebox.showwarning(title="更新確認", message="確認できませんでした。")

    def OpenLicense(self):
        PokeConCopyright(tk.Toplevel())

    def output_question(self):
        PokeConQuestionDialogue(tk.Toplevel(), command=self.cur_command).output_text()

    def exit(self):
        self._logger.debug("Close Menubar")
        if self.ser.isOpened():
            self.ser.closeSerial()
            print("serial disconnected")

        # stop listening to keyboard events
        if self.keyboard is not None:
            self.keyboard.stop()
            self.keyboard = None

        # save settings
        self.settings.save()

        self.camera.destroy()
        cv2.destroyAllWindows()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    widget = PokeController_Menubar(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
