#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

from Commands import CommandBase

if TYPE_CHECKING:
    from Window import PokeControllerApp
    from Commands.Sender import Sender


# MCU command
class McuCommand(CommandBase.Command):
    def __init__(self, sync_name: str):
        super(McuCommand, self).__init__()
        self.sync_name = sync_name
        self.postProcess = None

    def start(self, ser: Sender, postProcess: PokeControllerApp.stopPlayPost):
        ser.writeRow(self.sync_name)
        self.isRunning = True
        self.postProcess = postProcess

    def end(self, ser: Sender):
        ser.writeRow("end")
        self.isRunning = False
        if self.postProcess:
            self.postProcess()
