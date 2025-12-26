#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractclassmethod
from typing import List, Tuple, Optional
import threading
import time
from time import sleep
import random
from logging import getLogger, DEBUG, NullHandler
import os
import os.path
import datetime
import string

try:
    from plyer import notification

    flag_import_plyer = True
except Exception:
    flag_import_plyer = False
from Settings import GuiSettings
from ImageProcessing import ImageProcessing, crop_image, getImage, opneImage

from LineNotify import Line_Notify
from DiscordNotify import Discord_Notify
from Commands import CommandBase
from Commands.Keys import KeyPress

if TYPE_CHECKING:
    from Window import PokeControllerApp
    from GuiAssets import CaptureArea
    from Camera import Camera
    from Commands.Sender import Sender
    from Commands.Keys import Button, Hat, Stick, Direction


# the class For notifying stop signal is sent from Main window
class StopThread(Exception):
    pass


# Python command


class PythonCommand(CommandBase.Command):
    def __init__(self):
        super(PythonCommand, self).__init__()
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.keys = None
        self.thread = None
        self.alive = True
        self.postProcess = None
        try:
            self.Line = Line_Notify()
        except Exception:
            self.Line = None
        self.Discord = Discord_Notify()

    def pausedecorator(func):
        """
        一時停止を実現するためのデコレータです。
        戻り値が3つある関数に使用されます。
        """

        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            if self.isPause:
                self.show_var()
            while self.isPause:
                sleep(0.5)
                self.checkIfAlive()

        return inner

    def show_var(self):
        """
        一時停止時に内部変数の一覧を表示します。
        表示対象は自動化スクリプト側でselfにて定義した変数のみです。
        """
        var_dict = vars(self)  # 重い
        del_dict = [
            "isRunning",
            "message_dialogue",
            "socket0",
            "mqtt0",
            "keys",
            "thread",
            "alive",
            "postProcess",
            "Line",
            "Discord",
            "_logger",
            "camera",
            "gui",
            "ImgProc",
        ]
        print("--------内部変数一覧--------")
        for k, v in var_dict.items():
            if k not in del_dict:
                print(k, "=", v)
        print("----------------------------")

    @abstractclassmethod
    def do(self):
        """
        自動化スクリプト側でオーバーライトされるため、処理の記述はありません。
        """
        pass

    def do_safe(self, ser: Sender):
        """
        自動化スクリプト実行準備→実行→終了処理を順番に行います。
        """
        if self.keys is None:
            self.keys = KeyPress(ser)
            self.keys.init_hat()

        global flag_import_plyer
        try:
            if self.alive:
                if self.isWinNotStart:
                    if flag_import_plyer:
                        notification.notify(
                            title=f"{self.app_name} (profile:{self.profilename})",
                            message=f"{self.cur_command_name} started.",
                            timeout=5,
                        )
                    else:
                        print('"plyer" is not installed.')
                if self.isLineNotStart:
                    self.LINE_text(f"{self.app_name} (profile:{self.profilename})\n{self.cur_command_name} started.")
                if self.isDiscordNotStart:
                    self.discord_text(f"{self.app_name} (profile:{self.profilename})\n{self.cur_command_name} started.")
                self.do()
                self.finish()
        except StopThread:
            print("-- finished successfully. --")
            self._logger.info("Command finished successfully")
            if self.isWinNotEnd:
                if flag_import_plyer:
                    notification.notify(
                        title=f"{self.app_name} (profile:{self.profilename})",
                        message=f"{self.cur_command_name} finished.",
                        timeout=5,
                    )
                else:
                    print('"plyer" is not installed.')
            if self.isLineNotEnd:
                self.LINE_text(f"{self.app_name} (profile:{self.profilename})\n{self.cur_command_name} finished.")
            if self.isDiscordNotEnd:
                self.discord_text(f"{self.app_name} (profile:{self.profilename})\n{self.cur_command_name} finished.")
        except Exception as e:
            if self.keys is None:
                self.keys = KeyPress(ser)
                self.keys.init_hat()
            print("Interrupt:cmd(黒い画面)を確認してください。")
            print(e)
            self._logger.warning("Command stopped unexpectedly")
            import traceback

            traceback.print_exc()
            self.keys.end()
            self.alive = False

    def start(self, ser: Sender, postProcess: PokeControllerApp.stopPlayPost):
        """
        自動化スクリプトをスレッドに割り当てて実行します。
        """
        self.alive = True
        self.socket0.alive = True
        self.mqtt0.alive = True
        self.postProcess = postProcess
        ImageProcPythonCommand.template_path_name = "./Template/"
        if not self.thread:
            self.thread = threading.Thread(target=self.do_safe, args=(ser,))
            self.thread.start()

    def end(self, ser: Sender):
        self.socket0.alive = False
        self.mqtt0.alive = False
        self.sendStopRequest()

    def sendStopRequest(self):
        if self.checkIfAlive():  # try if we can stop now
            self.alive = False
            print("-- sent a stop request. --")
            self._logger.info("Sending stop request")
        if self.socket0.flag_socket:
            self.socket_disconnect()

    # NOTE: Use this function if you want to get out from a command loop by yourself
    def finish(self):
        """
        自動化スクリプトを終了します。(自動化スクリプト内で意図的に終了したい場合に使用。)
        """
        self.alive = False
        self.socket0.alive = False
        self.mqtt0.alive = False
        self.end(self.keys.ser)

    # press button at duration times(s)
    @pausedecorator
    def press(self, buttons: Button | Hat | Stick | Direction, duration: float = 0.1, wait: float = 0.1):
        """
        ボタンを押す。
        """
        self.keys.input(buttons)
        self.wait(duration)
        self.keys.inputEnd(buttons)
        self.wait(wait)
        self.checkIfAlive()

    # press button at duration times(s) repeatedly
    def pressRep(
        self,
        buttons: Button | Hat | Stick | Direction,
        repeat: int,
        duration: float = 0.1,
        interval: float = 0.1,
        wait: float = 0.1,
    ):
        """
        ボタンを複数回押す。
        """
        for i in range(0, repeat):
            self.press(buttons, duration, 0 if i == repeat - 1 else interval)
        self.wait(wait)

    # add hold buttons
    @pausedecorator
    def hold(self, buttons: Button | Hat | Stick | Direction, wait: float = 0.1):
        """
        ボタンを押したままの状態にする。
        """
        self.keys.hold(buttons)
        self.wait(wait)

    # release holding buttons
    @pausedecorator
    def holdEnd(self, buttons: Button | Hat | Stick | Direction):
        """
        ボタンを離した状態にする。
        """
        self.keys.holdEnd(buttons)
        self.checkIfAlive()

    # do nothing at wait time(s)
    @pausedecorator
    def short_wait(self, wait: float):
        """
        指定時間待機する。
        """
        current_time = time.perf_counter()
        while time.perf_counter() < current_time + wait:
            pass
        self.checkIfAlive()

    # do nothing at wait time(s)
    @pausedecorator
    def wait(self, wait: float):
        """
        指定時間待機する。
        """
        if float(wait) > 0.1:
            sleep(wait)
        else:
            current_time = time.perf_counter()
            while time.perf_counter() < current_time + wait:
                pass
        self.checkIfAlive()

    def checkIfAlive(self):
        """
        Aliveフラグの状態を確認する。
        AliveフラグがFalseなら終了処理を行う。
        """
        if not self.alive:
            self.keys.end()
            self.keys = None
            self.thread = None

            if self.postProcess is not None:
                self.postProcess()
                self.postProcess = None

            # raise exception for exit working thread
            self._logger.info("Exit from command successfully")
            raise StopThread("exit successfully")
        else:
            return True

    # direct serial
    def direct_serial(self, serialcommands: list, waittime: list):
        # 余計なものが付いている可能性があるので確認して削除する
        checkedcommands = []
        for row in serialcommands:
            checkedcommands.append(row.replace("\r", "").replace("\n", ""))
        self.keys.serialcommand_direct_send(checkedcommands, waittime)

    # Reload COM port (temporary function)
    def reload_com_port(self):
        if self.keys.ser.isOpened():
            print("Port is already opened and being closed.")
            self.keys.ser.closeSerial()
            # self.keyPress = None (ここでNoneはNGなはず)
            self.reload_com_port()
        else:
            if self.keys.ser.openSerial(
                GuiSettings().com_port.get(), GuiSettings().com_port_name.get(), GuiSettings().baud_rate.get()
            ):
                print("COM Port " + str(GuiSettings().com_port.get()) + " connected successfully")
                self._logger.debug("COM Port " + str(GuiSettings().com_port.get()) + " connected successfully")
                # self.keyPress = None (ここでNoneはNGなはず)

    def LINE_text(self, txt: str, token: str = "token"):
        # 送信
        try:
            self.Line.send_message(txt, token=token)
        except Exception:
            pass

    def discord_text(self, content: str = "", index: int = 0, keys: str = "DISCORD_WEBHOOK"):
        # webhook_urlのindex指定とkey設定
        if index != 0 and keys == "DISCORD_WEBHOOK":
            keys = f"DISCORD_WEBHOOK{index}"
        elif index == 0 and keys != "DISCORD_WEBHOOK":
            pass
        elif index != 0 and keys != "DISCORD_WEBHOOK":
            keys = f"DISCORD_WEBHOOK{index}"
        else:
            pass

        # 送信
        try:
            self.Discord.send_message(notification_message=content, keys=keys)
        except Exception:
            pass


def generateRandomCharacter(n: int):
    """
    指定数のランダムな文字列を生成する
    Contributor: kochan (敬称略)
    """
    c = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join([random.choice(c) for _ in range(n)])


def convertCv2Format(crop_fmt: int | str = "", crop: List[int] = []) -> Tuple(List[int], List[int]):  # type: ignore
    """
    リストをopencv/pillow形式に対応するよう変換する。
    ・Pillow形式
    x軸(横軸),y軸(縦軸),画像の左上が原点
    crop_fmt=1: [x軸始点, y軸始点, x軸終点, y軸終点] (res_pillowとして出力されるリスト)
    crop_fmt=2: [x軸始点, y軸始点, トリミング後の画像のサイズ(横), トリミング後の画像のサイズ(縦)]
    crop_fmt=3: [x軸始点, x軸終点, y軸始点, y軸終点]
    crop_fmt=4: [x軸始点, トリミング後の画像のサイズ(横), y軸始点, トリミング後の画像のサイズ(縦)]
    ・opencv形式(y, xの順番)
    crop_fmt=11: [y軸始点, x軸始点, y軸終点, x軸終点]
    crop_fmt=12: [y軸始点, x軸始点, トリミング後の画像のサイズ(縦), トリミング後の画像のサイズ(横)]
    crop_fmt=13: [y軸始点, y軸終点, x軸始点, x軸終点] (res_cv2として出力されるリスト)
    crop_fmt=14: [y軸始点, トリミング後の画像のサイズ(縦), x軸始点, トリミング後の画像のサイズ(横)]
    """

    try:
        # pillow形式
        if crop_fmt == 1 or crop_fmt == "1":
            res_cv2 = [crop[1], crop[3], crop[0], crop[2]]
        elif crop_fmt == 2 or crop_fmt == "2":
            res_cv2 = [crop[1], crop[1] + crop[3], crop[0], crop[0] + crop[2]]
        elif crop_fmt == 3 or crop_fmt == "3":
            res_cv2 = [crop[2], crop[3], crop[0], crop[1]]
        elif crop_fmt == 4 or crop_fmt == "4":
            res_cv2 = [crop[2], crop[2] + crop[3], crop[0], crop[0] + crop[1]]
        # opencv形式
        elif crop_fmt == 11 or crop_fmt == "11":
            res_cv2 = [crop[0], crop[2], crop[1], crop[3]]
        elif crop_fmt == 12 or crop_fmt == "12":
            res_cv2 = [crop[0], crop[0] + crop[2], crop[1], crop[1] + crop[3]]
        elif crop_fmt == 13 or crop_fmt == "13":
            res_cv2 = [crop[0], crop[1], crop[2], crop[3]]
        elif crop_fmt == 14 or crop_fmt == "14":
            res_cv2 = [crop[0], crop[0] + crop[1], crop[2], crop[2] + crop[3]]
        else:
            res_cv2 = [crop[1], crop[3], crop[0], crop[2]]
        res_pillow = [res_cv2[2], res_cv2[0], res_cv2[3], res_cv2[1]]
    except Exception:
        res_cv2 = []
        res_pillow = []

    return res_cv2, res_pillow


class ImageProcPythonCommand(PythonCommand):
    template_path_name = "./Template/"
    capture_path_name = "./Captures/"

    def __init__(self, cam: Camera, gui: CaptureArea = None):
        super(ImageProcPythonCommand, self).__init__()

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.camera = cam
        self.gui = gui

    def pausedecorator2(func):
        """
        一時停止を実現するためのデコレータです。
        戻り値が1つある関数に使用されます。
        """

        def inner(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            if self.isPause:
                self.show_var()
            while self.isPause:
                sleep(0.5)
                self.checkIfAlive()
            return res

        return inner

    def pausedecorator3(func):
        """
        一時停止を実現するためのデコレータです。
        戻り値が3つある関数に使用されます。
        """

        def inner(self, *args, **kwargs):
            res1, res2, res3 = func(self, *args, **kwargs)
            if self.isPause:
                self.show_var()
            while self.isPause:
                sleep(0.5)
                self.checkIfAlive()
            return res1, res2, res3

        return inner

    def get_filespec(self, filename: str, mode: str = "t") -> str:
        """
        画像ファイルの保存パスを取得する。

        入力が絶対パスの場合は、modeに合わせて、`template_path_name/capture_path_name`につなげずに返す。

        Args:
            filename (str): 保存名／保存パス
            mode (str): 相対パスの種類

        Returns:
            str: _description_
        """
        if os.path.isabs(filename):
            return filename
        elif mode == "c":
            return os.path.join(self.capture_path_name, filename)
        elif mode == "t":
            return os.path.join(self.template_path_name, filename)
        else:
            return filename

    def setTemplateDir(self, path):
        ImageProcPythonCommand.template_path_name = path

    def getCameraImage(self, crop_fmt: int | str = "", crop: List[int] = []) -> ImageProcessing.image_type:
        """
        カメラから画像データを取得する
        """
        # crop_fmtに応じてcropの中身を並び替える
        crop_cv2, _ = convertCv2Format(crop_fmt=crop_fmt, crop=crop)

        # カメラの画像を取得
        src = self.camera.readFrame()

        # トリミング
        cropped_image = crop_image(src, crop=crop_cv2)

        return cropped_image

    def openImage(self, filename: str, mode: str = "t") -> ImageProcessing.image_type:
        """
        指定されたパスの画像データを取得する
        """
        image = getImage(self.get_filespec(filename, mode=mode), mode="color")
        return image

    @pausedecorator2
    def isContainTemplate(
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
        """
        現在のスクリーンショットと指定した画像のテンプレートマッチングを行います。
        色の違いを考慮しないのであればパフォーマンスの点からuse_grayをTrueにしてグレースケール画像を使うことを推奨します。
        """

        # crop_fmtに応じてcropの中身を並び替える
        crop_cv2, crop_pillow = convertCv2Format(crop_fmt=crop_fmt, crop=crop)
        crop_template_cv2, _ = convertCv2Format(crop_fmt=crop_fmt, crop=crop_template)

        # カメラの画像を取得
        src = self.camera.readFrame()

        # テンプレート画像を取得
        if isinstance(template_path, ImageProcessing.image_type):
            template_image = template_path
        else:
            template_image = getImage(self.get_filespec(template_path, mode="t"), mode="color")

        # マスク画像を取得
        if isinstance(mask_path, ImageProcessing.image_type):
            mask_image = mask_path
        else:
            mask_image = (
                getImage(self.get_filespec(mask_path, mode="t"), mode="binary") if mask_path is not None else None
            )

        # テンプレートマッチング
        res, max_loc, width, height, max_val = ImageProcessing(use_gpu=use_gpu).isContainTemplate(
            src,
            template_image,
            mask_image=mask_image,
            threshold=threshold,
            use_gray=use_gray,
            crop=crop_cv2,
            BGR_range=BGR_range,
            threshold_binary=threshold_binary,
            crop_template=crop_template_cv2,
            show_image=show_image,
        )

        # テンプレートマッチングの結果(類似度)を表示する
        if show_value or self.isSimilarity:
            tm_mode = "NCC" if mask_path is not None else "ZNCC"
            print(f"{template_path} {tm_mode} value: {max_val}")

        # canvasに検出位置を表示
        if show_position:
            if crop_pillow != []:
                max_loc = list(max_loc)
                max_loc[0] += crop_pillow[0]
                max_loc[1] += crop_pillow[1]
            tag = str(time.perf_counter()) + str(random.random())
            if res:
                self.displayRectangle(max_loc, width, height, tag, ms, color=[color[0], color[2]], crop=crop_pillow)
            elif not show_only_true_rect:
                self.displayRectangle(max_loc, width, height, tag, ms, color=[color[1], color[2]], crop=crop_pillow)
            else:
                pass

        return res

    @pausedecorator3
    def isContainTemplate_max(
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
    ) -> Tuple(int, List[float], List[bool]):  # type: ignore
        """
        # 現在のスクリーンショットと指定した複数の画像のテンプレートマッチングを行います。
        # 相関値が最も大きい値となった画像のインデックス、各画像のテンプレートマッチングの閾値、閾値判定結果を返します。
        # 色の違いを考慮しないのであればパフォーマンスの点からuse_grayをTrueにしてグレースケール画像を使うことを推奨します。
        """

        # crop_fmtに応じてcropの中身を並び替える
        crop_cv2, crop_pillow = convertCv2Format(crop_fmt=crop_fmt, crop=crop)
        crop_template_cv2, _ = convertCv2Format(crop_fmt=crop_fmt, crop=crop_template)

        # カメラの画像を取得
        src = self.camera.readFrame()

        # テンプレート画像を取得
        template_image_list = []
        for i in template_path_list:
            if isinstance(i, ImageProcessing.image_type):
                template_image_list.append(i)
            else:
                template_image_list.append(getImage(self.get_filespec(i, mode="t"), mode="color"))

        # マスク画像を取得
        mask_image_list = []
        if mask_path_list is not None:
            for i in mask_path_list:
                if isinstance(i, ImageProcessing.image_type):
                    mask_image_list.append(i)
                else:
                    mask_image_list.append(getImage(self.get_filespec(i, mode="t"), mode="binary"))

        # テンプレートマッチング
        max_idx, max_val_list, max_loc_list, width_list, height_list, judge_list = ImageProcessing(
            use_gpu=False
        ).isContainTemplate_max(
            src,
            template_image_list,
            mask_image_list=mask_image_list,
            threshold=threshold,
            use_gray=use_gray,
            crop=crop_cv2,
            BGR_range=BGR_range,
            threshold_binary=threshold_binary,
            crop_template=crop_template_cv2,
            show_image=show_image,
        )

        # テンプレートマッチングの結果(類似度)を表示する
        if show_value or self.isSimilarity:
            tm_mode = "ZNCC" if (mask_path_list == [] or mask_path_list is None) else "NCC"
            for template_path, max_val in zip(template_path_list, max_val_list):
                print(f"{template_path} {tm_mode} value: {max_val}")

        # canvasに検出位置を表示
        if show_position:
            if crop_pillow != []:
                max_loc_list[max_idx] = list(max_loc_list[max_idx])
                max_loc_list[max_idx][0] += crop_pillow[0]
                max_loc_list[max_idx][1] += crop_pillow[1]
            tag = str(time.perf_counter()) + str(random.random())
            if True in judge_list:
                self.displayRectangle(
                    max_loc_list[max_idx],
                    width_list[max_idx],
                    height_list[max_idx],
                    tag,
                    ms,
                    color=[color[0], color[2]],
                    crop=crop_pillow,
                )
            elif not show_only_true_rect:
                self.displayRectangle(
                    max_loc_list[max_idx],
                    width_list[max_idx],
                    height_list[max_idx],
                    tag,
                    ms,
                    color=[color[1], color[2]],
                    crop=crop_pillow,
                )
            else:
                pass

        return max_idx, max_val_list, judge_list

    @pausedecorator2
    def isContainTemplateGPU(
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
        BGR_range: Optional[dict] = None,
        threshold_binary: Optional[int] = None,
        crop_template: List[int] = [],
        show_image: bool = False,
        color: List[str] = ["blue", "red", "orange"],
    ) -> bool:
        """
        現在のスクリーンショットと指定した画像のテンプレートマッチングを行います。
        テンプレートマッチングにGPUを使用します。
        色の違いを考慮しないのであればパフォーマンスの点からuse_grayをTrueにしてグレースケール画像を使うことを推奨します。
        """
        # テンプレートマッチング
        res = self.isContainTemplate(
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
            use_gpu=True,
            BGR_range=BGR_range,
            threshold_binary=threshold_binary,
            crop_template=crop_template,
            show_image=show_image,
            color=color,
        )

        return res

    @pausedecorator2
    def isContainedImage(
        self,
        image_path: str,
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
        """
        指定した画像に対して現在のスクリーンショットから生成したテンプレート画像を用いてテンプレートマッチングを行います。
        色の違いを考慮しないのであればパフォーマンスの点からuse_grayをTrueにしてグレースケール画像を使うことを推奨します。
        """

        # crop_fmtに応じてcropの中身を並び替える
        crop_cv2, crop_pillow = convertCv2Format(crop_fmt=crop_fmt, crop=crop)
        crop_template_cv2, crop_template_pillow = convertCv2Format(crop_fmt=crop_fmt, crop=crop_template)

        # カメラの画像を取得
        template_image = self.camera.readFrame()

        # テンプレートマッチング対象画像を取得
        if isinstance(image_path, ImageProcessing.image_type):
            image = image_path
        else:
            image = getImage(self.get_filespec(image_path, mode="t"), mode="color")

        # マスク画像を取得
        if isinstance(mask_path, ImageProcessing.image_type):
            mask_image = mask_path
        else:
            mask_image = (
                getImage(self.get_filespec(mask_path, mode="t"), mode="binary") if mask_path is not None else None
            )

        # テンプレートマッチング
        res, _, width, height, max_val = ImageProcessing(use_gpu=use_gpu).isContainTemplate(
            image,
            template_image,
            mask_image=mask_image,
            threshold=threshold,
            use_gray=use_gray,
            crop=crop_cv2,
            BGR_range=BGR_range,
            threshold_binary=threshold_binary,
            crop_template=crop_template_cv2,
            show_image=show_image,
        )

        # テンプレートマッチングの結果(類似度)を表示する
        if show_value or self.isSimilarity:
            tm_mode = "NCC" if mask_path is not None else "ZNCC"
            print(f"capture_image {tm_mode} value: {max_val}")

        # canvasに検出位置を表示
        if show_position:
            tag = str(time.perf_counter()) + str(random.random())
            if res:
                self.displayRectangle(
                    crop_template_pillow[0:2], width, height, tag, ms, color=[color[0], color[2]], crop=[]
                )
            elif not show_only_true_rect:
                self.displayRectangle(
                    crop_template_pillow[0:2], width, height, tag, ms, color=[color[1], color[2]], crop=[]
                )
            else:
                pass

        return res

    def displayRectangle(
        self,
        max_loc: tuple,
        width: int,
        height: int,
        tag: str = None,
        ms: float = 2000,
        color: List[str] = ["blue", "orange"],
        crop_fmt: int | str = "",
        crop: List[int] = [],
    ):
        """
        GUIの画面に四角形を表示します。
        互換性維持のため、gui/canvas(元をたどると同じ変数)の両方に対応します。
        """
        # crop_fmtに応じてcropの中身を並び替える
        _, crop_pillow = convertCv2Format(crop_fmt=crop_fmt, crop=crop)

        top_left = max_loc
        bottom_right = (top_left[0] + width + 1, top_left[1] + height + 1)
        if self.gui is not None:
            canvas = self.gui
        else:
            canvas = self.canvas

        if tag is None:
            tag = generateRandomCharacter(10)

        if self.gui is not None or self.isGuide:
            if crop_pillow != []:
                canvas.ImgRect(*crop_pillow[0:2], *crop_pillow[2:4], outline=color[1], tag=tag, ms=int(ms), flag=False)
            canvas.ImgRect(*top_left, *bottom_right, outline=color[0], tag=tag, ms=int(ms))
        else:
            pass

    def displayText(
        self,
        position: tuple,
        txt: str,
        tag: str = None,
        ms: int = 2000,
        font: str = "UD デジタル 教科書体 NP-B",
        fontsize: int = 20,
        color: str = "black",
    ):
        if self.gui is not None:
            canvas = self.gui
        else:
            canvas = self.canvas

        ft = (font, fontsize)

        if tag is None:
            tag = generateRandomCharacter(10)

        if self.gui is not None or self.isGuide:
            canvas.ImgText(position[0], position[1], txt=txt, tag=tag, ms=int(ms), ft=ft, color=color)
        else:
            pass

    def saveCapture(self, filename: str = None, crop_fmt: int | str = "", crop: List[int] = [], mode: bool = True):
        """
        画面をキャプチャします。
        (camera.saveCaptureと同じ機能。)
        """

        # crop_fmtに応じてcropの中身を並び替える
        crop_cv2, _ = convertCv2Format(crop_fmt=crop_fmt, crop=crop)

        # カメラの画像を取得
        src = self.camera.readFrame()

        # ファイル名を設定する
        if filename is None or filename == "":
            dt_now = datetime.datetime.now()
            filename = dt_now.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        else:
            filename = filename + ".png"
        if mode:
            save_path = self.get_filespec(filename, mode="c")
        else:
            save_path = self.get_filespec(filename, mode="n")

        # 画像を保存する
        ImageProcessing().saveImage(src, filename=save_path, crop=crop_cv2)

    def popupImage(self, crop_fmt: int | str = "", crop: List[int] = [], title: str = "image"):
        """
        popupで画像を表示する
        """
        # crop_fmtに応じてcropの中身を並び替える
        crop_cv2, _ = convertCv2Format(crop_fmt=crop_fmt, crop=crop)

        # カメラの画像を取得
        src = self.camera.readFrame()

        opneImage(src, crop=crop_cv2, title=title)

    def LINE_image(self, txt: str, crop_fmt: int | str = "", crop: List[int] = [], token: str = "token"):
        """
        Lineにテキストと画像を通知します。
        """
        # crop_fmtに応じてcropの中身を並び替える
        crop_cv2, _ = convertCv2Format(crop_fmt=crop_fmt, crop=crop)

        # カメラの画像を取得
        src = self.camera.readFrame()

        # トリミング
        cropped_image = crop_image(src, crop=crop_cv2)

        # 送信
        try:
            self.Line.send_message(txt, cropped_image, token)
        except Exception:
            pass

    def discord_image(
        self,
        content: str = "",
        index: int = 0,
        crop_fmt: int | str = "",
        crop: List[int] = [],
        keys: str | list = "DISCORD_WEBHOOK",
    ):
        """
        Discordにテキストと画像を通知します。
        """
        # crop_fmtに応じてcropの中身を並び替える
        crop_cv2, _ = convertCv2Format(crop_fmt=crop_fmt, crop=crop)

        # カメラの画像を取得
        src = self.camera.readFrame()

        # トリミング
        cropped_image = crop_image(src, crop=crop_cv2)

        # webhook_urlのindex指定とkey設定
        if index != 0 and keys == "DISCORD_WEBHOOK":
            keys = f"DISCORD_WEBHOOK{index}"
        elif index == 0 and keys != "DISCORD_WEBHOOK":
            pass
        elif index != 0 and keys != "DISCORD_WEBHOOK":
            keys = f"DISCORD_WEBHOOK{index}"
        else:
            pass

        # 送信
        try:
            self.Discord.send_message(notification_message=content, image=cropped_image, keys=keys)
        except Exception:
            pass
