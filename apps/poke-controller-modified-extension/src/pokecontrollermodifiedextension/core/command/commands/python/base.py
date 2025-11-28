from abc import ABC, abstractmethod
from time import sleep
import threading
import time

from ..base import Command
from .decorators import pausable


class StopThread(Exception):
    pass


class PythonCommand(Command, ABC):
    def __init__(self):
        super().__init__()

        # FIXME: logging
        # self._logger = getLogger(__name__)
        # self._logger.addHandler(NullHandler())
        # self._logger.setLevel(DEBUG)
        # self._logger.propagate = True

        # FIXME: typing
        self.keys = None
        self.thread = None
        self.alive = True
        self.postProcess = None
        try:
            # FIXME: Line_Notify()
            self.Line = None
        except Exception:
            self.Line = None
        # FIXME: Discord_Notify()
        self.Discord = None

    @abstractmethod
    def do(self) -> None:
        """
        自動化スクリプト側でオーバーライトされるため、処理の記述はありません。
        """
        pass

    def do_safe(self, ser) -> None:
        """
        自動化スクリプト実行準備→実行→終了処理を順番に行います。
        """
        # FIXME: 後回し
        pass

    def start(self, ser, postProcess=None) -> None:
        """
        自動化スクリプトをスレッドに割り当てて実行します。
        """
        self.alive = True
        self.socket0.alive = True
        self.mqtt0.alive = True
        self.postProcess = postProcess
        if not self.thread:
            self.thread = threading.Thread(target=self.do_safe, args=(ser,))
            self.thread.start()

    def end(self, ser) -> None:
        self.socket0.alive = False
        self.mqtt0.alive = False
        self.sendStopRequest()

    def finish(self) -> None:
        """
        自動化スクリプトを終了します。(自動化スクリプト内で意図的に終了したい場合に使用。)
        """
        self.alive = False
        self.socket0.alive = False
        self.mqtt0.alive = False
        self.end(self.keys.ser)

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

            # FIXME: logging
            # raise exception for exit working thread
            # self._logger.info("Exit from command successfully")
            raise StopThread("exit successfully")
        else:
            return True

    def sendStopRequest(self) -> None:
        if self.checkIfAlive():  # try if we can stop now
            self.alive = False
            print("-- sent a stop request. --")
            # FIXME: logging
            # self._logger.info("Sending stop request")
        if self.socket0.flag_socket:
            self.socket_disconnect()

    def show_var(self) -> None:
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

    @pausable
    def press(
        self,
        buttons,  # FIXME: typing
        duration: float = 0.1,
        wait: float = 0.1,
    ) -> None:
        """
        ボタンを押す。
        """
        self.keys.input(buttons)
        self.wait(duration)
        self.keys.inputEnd(buttons)
        self.wait(wait)
        self.checkIfAlive()

    def pressRep(
        self,
        buttons,  # FIXME: typing
        repeat: int,
        duration: float = 0.1,
        interval: float = 0.1,
        wait: float = 0.1,
    ) -> None:
        """
        ボタンを複数回押す。
        """
        for i in range(0, repeat):
            self.press(buttons, duration, 0 if i == repeat - 1 else interval)
        self.wait(wait)

    @pausable
    def hold(
        self,
        buttons,  # FIXME: typing
        wait: float = 0.1
    ) -> None:
        """
        ボタンを押したままの状態にする。
        """
        self.keys.hold(buttons)
        self.wait(wait)

    def holdEnd(
        self,
        buttons,  # FIXME: typing
    ) -> None:
        """
        ボタンを離した状態にする。
        """
        self.keys.holdEnd(buttons)
        self.checkIfAlive()

    @pausable
    def short_wait(self, wait: float) -> None:
        """
        指定時間待機する。
        """
        current_time = time.perf_counter()
        while time.perf_counter() < current_time + wait:
            pass
        self.checkIfAlive()

    @pausable
    def wait(self, wait: float) -> None:
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

    def direct_serial(self, serialcommands: list, waittime: list) -> None:
        # 余計なものが付いている可能性があるので確認して削除する
        checkedcommands = []
        for row in serialcommands:
            checkedcommands.append(row.replace("\r", "").replace("\n", ""))
        self.keys.serialcommand_direct_send(checkedcommands, waittime)

    # temporary function
    def reload_com_port(self) -> None:
        # FIXME: 後回し
        pass

    def LINE_text(self, txt: str, token: str = "token") -> None:
        # 送信
        try:
            self.Line.send_message(txt, token=token)
        except Exception:
            pass

    def discord_text(self, content: str = "", index: int = 0, keys: str = "DISCORD_WEBHOOK") -> None:
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
