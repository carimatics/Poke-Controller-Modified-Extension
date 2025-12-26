#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import configparser
import os
import time
import socket
import datetime

try:
    import paho.mqtt
    import paho.mqtt.client as mqtt

    print(f"paho-mqtt {paho.mqtt.__version__} is installed. You can use MQTTCommunications class.")
    isMQTT = True
except Exception:
    print("paho-mqtt is not installed. You can't use MQTTCommunications class.")
    isMQTT = False


def generate_token_file(filename):
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
        print(f"mkdir: '{dirname}'")
    token_file = configparser.ConfigParser(comment_prefixes="#", allow_no_value=True)
    token_file["SOCKET"] = {"addr": "127.0.0.1", "port": "49152"}
    token_file["MQTT"] = {"broker_address": "", "id": "", "fullaccess_token": "", "readonly_token": ""}
    with open(filename, "w", encoding="utf-8") as file:
        token_file.write(file)
    os.chmod(path=filename, mode=0o777)
    print("Generate external token file")


# socket通信用class
class SocketCommunications:
    SOCKET_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "profiles", "default", "external_token.ini")

    def __init__(self):
        """
        初期設定
        return:なし
        """
        super(SocketCommunications, self).__init__()
        self.alive = False
        self.flag_socket = False

        # SOCKET設定
        self.token_file = configparser.ConfigParser(comment_prefixes="#", allow_no_value=True)
        self.open_file_with_utf8()
        token_list = {key: self.token_file["SOCKET"][key] for key in self.token_file["SOCKET"]}
        # token_num = len(token_list)

        self.IPADDR = token_list["addr"]
        self.PORT = int(token_list["port"])

    def open_file_with_utf8(self):  # line_notify.pyからの流用
        """
        utf-8 のファイルを BOM ありかどうかを自動判定して読み込む
        return:なし
        """
        if not os.path.isfile(self.SOCKET_TOKEN_PATH):
            generate_token_file(self.SOCKET_TOKEN_PATH)

        is_with_bom = self.is_utf8_file_with_bom(self.SOCKET_TOKEN_PATH)

        encoding = "utf-8-sig" if is_with_bom else "utf-8"
        self.token_file.read(self.SOCKET_TOKEN_PATH, encoding)

    def is_utf8_file_with_bom(self, filename):  # line_notify.pyからの流用
        """
        utf-8 ファイルが BOM ありかどうかを判定する
        return:なし
        filename|str:ファイル名
        """
        socket_first = open(filename, encoding="utf-8").readline()
        return socket_first[0] == "\ufeff"

    def change_ipaddr(self, addr):
        """
        IPアドレスを変更する
        return:なし
        addr|str:IPアドレス
        """
        self.IPADDR = addr

    def change_port(self, port):
        """
        ポート番号を変更する
        return:なし
        port|int:ポート番号
        """
        self.port = port

    def sock_connect(self):
        """
        socket通信用のserverと接続する
        return:なし
        """
        try:
            self.sock = socket.socket(socket.AF_INET)
            self.sock.connect((self.IPADDR, self.PORT))
            self.sock.settimeout(3.0)  # タイムアウト時間
            self.flag_socket = True
        except ConnectionRefusedError:
            print("[error]serverが起動されていません")
        except OSError:
            pass

    # socket切断
    def sock_disconnect(self):
        """
        socket通信用のserverから切断する
        return:なし
        """
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.flag_socket = False
        except ConnectionRefusedError:
            print("[error]serverが起動されていません")
        except OSError:
            pass

    def receive_message(self, header, show_msg=False):
        """
        socketを用いて先頭が特定の文字列であるメッセージを受信する
        return output|str:受信した文字列
        header|str:受信したい文字列(先頭)
        show_msg|bool:受信した文字列を出力する
        """
        # 待機文字列print出力
        print(f"[socket:wait]:{header}")

        # 出力初期値設定
        output = None

        while True:
            try:
                # 受信する
                data = self.sock.recv(1024)
                if data == b"":
                    break
                message = data.decode("utf-8")

                # 先頭の文字列がheaderと一致するかを確認する
                if message[0 : len(header)] == header:
                    print(f"[socket:recv]:{message}")
                    output = message
                    break
                elif show_msg:  # ログ出力
                    print(f"[socket:recv]:{message}")
                if not self.alive:
                    break
            except ConnectionResetError:
                break
            except socket.timeout:  # timeout時,self.aliveを確認する
                if not self.alive:
                    break
            except ConnectionRefusedError:
                print("[error]serverが起動されていません")
                break
            except OSError:
                break

        # stopを押した場合にsocketを切断する
        if not self.alive:
            # socket切断
            self.sock_disconnect()

        return output

    def receive_message2(self, headerlist, show_msg=False):
        """
        socketを用いて先頭が特定の文字列(複数設定可能)であるメッセージを受信する
        return output|str:受信した文字列
        headerlist|list[str]:受信したい文字列(先頭)のリスト
        show_msg|bool:受信した文字列を出力する
        """
        # 待機文字列print出力
        header0 = ""
        for i in headerlist:
            header0 += i + ","
        print(f"[socket:wait]:{header0}")

        # 出力初期値設定
        output = None

        while True:
            try:
                # 受信する
                data = self.sock.recv(1024)
                if data == b"":
                    break
                message = data.decode("utf-8")

                # messageとheaderlist内の先頭の文字列が一致するかを確認する
                for header in headerlist:
                    if message[0 : len(header)] == header:
                        print(f"[socket:recv]:{message}")
                        output = message
                if output:
                    break
                if show_msg:  # ログ出力
                    print(f"[socket:recv]:{message}")
                if not self.alive:
                    break
            except ConnectionResetError:
                break
            except socket.timeout:  # timeout時,self.aliveを確認する
                if not self.alive:
                    break
            except ConnectionRefusedError:
                print("[error]serverが起動されていません")
                break
            except OSError:
                break

        # stopを押した場合にsocketを切断する
        if not self.alive:
            # socket切断
            self.sock_disconnect()

        return output

    def transmit_message(self, message):
        """
        socketを用いてメッセージを送信する
        return:なし
        message|str:送信するメッセージ
        """
        # 送信する
        self.sock.send(message.encode("utf-8"))
        print(f"[socket:send]:{message}")


# global変数(MQTT受信用)
receive_msg = None


# MQTT通信用class
class MQTTCommunications:
    MQTT_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "profiles", "default", "external_token.ini")

    def __init__(self, clientId):
        """
        初期設定
        return:なし
        name|str:接続者名(重複してもよい)
        """
        super(MQTTCommunications, self).__init__()
        self.alive = False

        # MQTT設定
        self.token_file = configparser.ConfigParser(comment_prefixes="#", allow_no_value=True)
        self.open_file_with_utf8()
        token_list = {key: self.token_file["MQTT"][key] for key in self.token_file["MQTT"]}
        # token_num = len(token_list)

        self.broker_address = token_list["broker_address"]
        self.id = token_list["id"]
        fullaccess_token = token_list["fullaccess_token"]
        readonly_token = token_list["readonly_token"]

        if fullaccess_token != "":
            self.pub_token = fullaccess_token
            self.sub_token = fullaccess_token
        elif readonly_token != "":
            self.pub_token = None
            self.sub_token = readonly_token
        else:
            self.pub_token = None
            self.sub_token = None

        self.clientId = clientId
        self.receive_msg = -1

    def exceptiondecorator(func):
        """
        MQTTのライブラリがインストールされていない場合を想定したデコレータです。
        実行した場合にログを出力します。
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                print("paho-mqtt may not be installed. Please make sure paho-mqtt is installed.")
                return ""

        return wrapper

    def open_file_with_utf8(self):  # line_notify.pyからの流用
        """
        utf-8 のファイルを BOM ありかどうかを自動判定して読み込む
        return:なし
        """
        if not os.path.isfile(self.MQTT_TOKEN_PATH):
            generate_token_file(self.MQTT_TOKEN_PATH)

        is_with_bom = self.is_utf8_file_with_bom(self.MQTT_TOKEN_PATH)

        encoding = "utf-8-sig" if is_with_bom else "utf-8"
        self.token_file.read(self.MQTT_TOKEN_PATH, encoding)

    def is_utf8_file_with_bom(self, filename):  # line_notify.pyからの流用
        """
        utf-8 ファイルが BOM ありかどうかを判定する
        return:なし
        filename|str:ファイル名
        """
        mqtt_first = open(filename, encoding="utf-8").readline()
        return mqtt_first[0] == "\ufeff"

    def change_broker_address(self, broker_address):
        """
        brokerアドレスを変更する
        return:なし
        broker_address|str:brokerアドレス
        """
        self.broker_address = broker_address

    def change_id(self, id):
        """
        IDを変更する
        return:なし
        id|str:ID
        """
        self.id = id

    def change_pub_token(self, pub_token):
        """
        pub用tokenを変更する
        return:なし
        pub_token|str:pub用token
        """
        self.pub_token = pub_token

    def change_sub_token(self, sub_token):
        """
        sub用tokenを変更する
        return:なし
        sub_token|str:sub用token
        """
        self.sub_token = sub_token

    def change_clientId(self, clientId):
        """
        接続者名を変更する
        return:なし
        clientId|str:接続者名
        """
        self.clientId = clientId

    def on_message(self, client, userdata, msg):
        """
        メッセージを受信する
        return:なし
        client,userdata,msgはいいように設定してくれる
        """
        global receive_msg
        # print(f"ROOM ID: {msg.topic} message: {msg.payload.decode('utf-8')}")
        receive_msg = msg.payload.decode("utf-8")

    @exceptiondecorator
    def receive_message(self, roomid, header, show_msg=False):
        """
        MQTTを用いて先頭が特定の文字列であるメッセージを受信する
        return output|str:受信した文字列
        roomid|str:ROOM ID(topic)
        header|str:受信したい文字列(先頭)
        show_msg|bool:受信した文字列を出力する
        """
        # 待機文字列print出力
        print(f"[mqtt:wait]:{header}")

        global receive_msg
        output = None
        header_date = int(datetime.datetime.today().strftime("%Y%m%d%H%M%S%f"))
        message = -1

        # brokerと接続する
        self.client = mqtt.Client(self.clientId)
        self.client.username_pw_set(self.id, self.sub_token)
        self.client.connect(self.broker_address, 1883)
        self.client.subscribe(roomid)
        self.client.on_message = self.on_message

        while True:
            try:
                # brokerからメッセージを引き抜く
                self.client.loop_start()
                time.sleep(1.0)
                self.client.loop_stop()
                if receive_msg:
                    if header_date < int(receive_msg[1:21]):
                        header_date = int(receive_msg[1:21])
                        message = receive_msg[22:]
                        # 先頭の文字列がheaderと一致するかを確認する
                        if message[0 : len(header)] == header:
                            output = message
                            print(f"[mqtt:recv]:{message}")
                            break
                        elif show_msg:  # ログ出力
                            print(f"[mqtt:recv]:{message}")

                # stop押下時にwhileから抜ける
                if not self.alive:
                    break
            except Exception:
                break

        self.client.disconnect()

        return output

    @exceptiondecorator
    def receive_message2(self, roomid, headerlist, show_msg=False):
        """
        MQTTを用いて先頭が特定の文字列(複数設定可能)であるメッセージを受信する
        return output|str:受信した文字列
        roomid|str:ROOM ID(topic)
        headerlist|list[str]:受信したい文字列(先頭)のリスト
        show_msg|bool:受信した文字列を出力する
        """
        # 待機文字列print出力
        header0 = ""
        for i in headerlist:
            header0 += i + ","
        print(f"[socket:wait]:{header0}")

        global receive_msg
        output = None
        header_date = int(datetime.datetime.today().strftime("%Y%m%d%H%M%S%f"))
        message = -1

        # brokerと接続する
        self.client = mqtt.Client(self.clientId)
        self.client.username_pw_set(self.id, self.sub_token)
        self.client.connect(self.broker_address, 1883)
        self.client.subscribe(roomid)
        self.client.on_message = self.on_message

        while True:
            try:
                # brokerからメッセージを引き抜く
                self.client.loop_start()
                time.sleep(1.0)
                self.client.loop_stop()
                if receive_msg:
                    if header_date < int(receive_msg[1:21]):
                        header_date = int(receive_msg[1:21])
                        message = receive_msg[22:]
                        # messageとheaderlist内の先頭の文字列が一致するかを確認する
                        for header in headerlist:
                            if message[0 : len(header)] == header:
                                output = message
                                print(f"[mqtt:recv]:{message}")
                        if output:
                            break
                        elif show_msg:  # ログ出力
                            print(f"[mqtt:recv]:{message}")

                # stop押下時にwhileから抜ける
                if not self.alive:
                    break
            except Exception:
                break

        self.client.disconnect()

        return output

    @exceptiondecorator
    def transmit_message(self, roomid, message):
        """
        MQTTを用いてメッセージを送信する
        return:なし
        roomid|str:ROOM ID(topic)
        message|str:送信するメッセージ
        """
        # メッセージ更新判定に日時情報を使用する
        header_date = datetime.datetime.today().strftime("[%Y%m%d%H%M%S%f]")
        if self.pub_token:
            self.client = mqtt.Client(self.clientId)
            self.client.username_pw_set(self.id, self.pub_token)
            self.client.connect(self.broker_address, 1883)
            message0 = header_date + message
            self.client.publish(roomid, message0)
            print(f"[mqtt:send]:{message}")
        else:
            print("token error(readonly)")

        self.client.disconnect()
