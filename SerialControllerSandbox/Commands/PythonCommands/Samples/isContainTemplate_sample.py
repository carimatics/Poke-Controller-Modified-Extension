#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import ImageProcPythonCommand
import tkinter.messagebox as tkmsg


class isContainTemplate_sample(ImageProcPythonCommand):
    NAME = '画像認識関数紹介(1) ver. 0.0.1'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        print("-------------------------------------")
        print("画像認識関数紹介(1) ver. 0.0.1")
        print("-------------------------------------")

        tkmsg.showinfo('確認', '本スクリプトでは画像認識関数の基本的な機能の紹介を行います。\n\nSwitchのHOME画面を開き、ポケモンホームのロゴ画像が映っている状態にしてください。\n\n確認したら"OK"を押してください。')

        print("\n実行関数：self.isContainTemplate('Samples/logo_pokemon_home.png')")
        res = self.isContainTemplate('Samples/logo_pokemon_home.png')
        print(f"結果(True:検出成功, False:検出失敗):{res}")
        tkmsg.showinfo('確認', '最も基本的な画像認識を行いました。\n\n表示されている画像からポケモンホームのロゴ画像があるかを判定しています。\n\n実行関数と結果は右側のログ画面に出力しています。\n\nよければ"OK"を押して下さい。')

        print("\n実行関数：self.isContainTemplate('Samples/logo_pokemon_home.png', use_gary=False)")
        res = self.isContainTemplate('Samples/logo_pokemon_home.png', use_gray=False)
        print(f"結果(True:検出成功, False:検出失敗):{res}")
        tkmsg.showinfo('確認', '先ほどの画像認識は画像をグレースケール化して処理しましたが、パラメータ(use_gray)を設定することで、カラーの状態でも処理できます。\n\n実行関数と結果は右側のログ画面に出力しています。\n\nよければ"OK"を押して下さい。')

        print("\n実行関数：self.isContainTemplate('Samples/logo_pokemon_home.png', use_gary=False, threshold=0.9)")
        res = self.isContainTemplate('Samples/logo_pokemon_home.png', use_gray=False, threshold=0.9)
        print(f"結果(True:検出成功, False:検出失敗):{res}")
        tkmsg.showinfo('確認', '画像認識の検出成功/失敗は類似度(0-1)が閾値を超えるか否かで判定しています。\n\n閾値を超えると検出成功で、閾値はパラメータ(threshold)で変更することが可能です。\n\n実行関数と結果は右側のログ画面に出力しています。\n\nよければ"OK"を押して下さい。')

        print("\n実行関数：self.isContainTemplate('Samples/logo_pokemon_home.png', use_gary=False, threshold=0.9, show_value=True)")
        res = self.isContainTemplate('Samples/logo_pokemon_home.png', use_gray=False, threshold=0.9, show_value=True)
        print(f"結果(True:検出成功, False:検出失敗):{res}")
        tkmsg.showinfo('確認', '類似度はパラメータ(show_value)により表示することが可能です。\n\n実行関数と結果は右側のログ画面に出力しています。\n\nよければ"OK"を押して下さい。')

        print("\n(1回目)\n実行関数：self.isContainTemplate('lSamples/ogo_pokemon_home.png', use_gary=False, threshold=0.9, show_value=True, crop=[87, 177, 1183, 459])")
        res = self.isContainTemplate('Samples/logo_pokemon_home.png', use_gray=False, threshold=0.9, show_value=True, crop=[87, 177, 1183, 459])
        print(f"結果(True:検出成功, False:検出失敗):{res}")
        print("(2回目)\n実行関数：self.isContainTemplate('Samples/logo_pokemon_home.png', use_gary=False, threshold=0.9, show_value=True, crop=[59, 392, 1218, 686])")
        res = self.isContainTemplate('Samples/logo_pokemon_home.png', use_gray=False, threshold=0.9, show_value=True, crop=[59, 392, 1218, 686])
        print(f"結果(True:検出成功, False:検出失敗):{res}")
        tkmsg.showinfo('確認', '画像認識の対象とするエリアはパラメータ(crop)により指定することができます。\n\n1回目はロゴがあるエリアを指定したので検出検出に成功していますが、2回目はロゴがないエリアを指定したので失敗しています。\n\n実行関数と結果は右側のログ画面に出力されています。\n\n以上で説明を終わります。\n\n"OK"を押して下さい。')

        self.finish()
