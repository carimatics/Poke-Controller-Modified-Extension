#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import ImageProcPythonCommand
import os

class changetemplatedir(ImageProcPythonCommand):
    NAME = 'テンプレート画像ディレクトリ変更'

    def __init__(self, cam):
        super().__init__(cam)

    def do(self):
        '''
        テンプレート画像のディレクトリを"Template"から一時的に指定した場所に変更する。
        ディレクトリの変更は、GUIの"start"を押した段階でリセットされる。
        そのため、この関数は"do"の中で実行すること。("__init__"内で実行しても効果がないことに注意。)
        本サンプルでは、テンプレート画像のディレクトリをこのファイルが置いてあるディレクトリに変更している。
        '''
        print(f'変更前のディレクトリ：{ImageProcPythonCommand.template_path_name}')
        self.setTemplateDir(os.path.dirname(__file__) + "/")
        print(f'変更後のディレクトリ：{ImageProcPythonCommand.template_path_name}')
