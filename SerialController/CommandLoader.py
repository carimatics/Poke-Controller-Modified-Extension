#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib
import sys

import Utility as util

from logging import getLogger, DEBUG, NullHandler

logger = getLogger(__name__)
logger.addHandler(NullHandler())
logger.setLevel(DEBUG)
logger.propagate = True


class CommandLoader:
    def __init__(self, base_path, base_class):
        self.path = base_path
        self.base_type = base_class
        self.modules = []

    def load(self):
        if not self.modules:  # load if empty
            self.modules = util.importAllModules(self.path)

        # return command class types
        return self.getCommandClasses()

    def reload(self):
        loaded_module_dic = {mod.__name__: mod for mod in self.modules}
        cur_module_names = util.getModuleNames(self.path)

        # Load only not loaded modules
        not_loaded_module_names = list(set(cur_module_names) - set(loaded_module_dic.keys()))
        if len(not_loaded_module_names) > 0:
            self.modules.extend(util.importAllModules(self.path, not_loaded_module_names))

        # Reload commands except deleted ones
        for mod_name in list(set(cur_module_names) & set(loaded_module_dic.keys())):
            importlib.reload(loaded_module_dic[mod_name])

        # Unload deleted commands
        for mod_name in list(set(loaded_module_dic.keys()) - set(cur_module_names)):
            self.modules.remove(loaded_module_dic[mod_name])
            sys.modules.pop(loaded_module_dic[mod_name].__name__)  # Un-import module forcefully

        # return command class types
        return self.getCommandClasses()

    def getCommandClasses(self):
        classes = []
        for mod in self.modules:
            # extract module of having "NAME"
            class_list = [
                c
                for c in util.getClassesInModule(mod)
                if issubclass(c, self.base_type) and hasattr(c, "NAME") and c.NAME
            ]

            # make tags of directory name
            for c in class_list:
                dir_name = "/".join(mod.__name__.split(".")[2:])
                dir_tags = ["@" + t for t in mod.__name__.split(".")[2:-1]]

                # add tags of directory name
                if hasattr(c, "TAGS"):
                    if isinstance(c.TAGS, list):
                        logger.debug(f"TAGS name add: {dir_tags}")
                        c.TAGS = c.TAGS + dir_tags
                    elif isinstance(c.TAGS, str):
                        logger.debug(f"TAGS name add: {dir_tags}")
                        c.TAGS = [c.TAGS] + dir_tags
                    else:
                        logger.debug(f"TAGS Type error: {mod.__name__} {c.NAME} {type(c.TAGS)}")
                else:
                    logger.debug(f"TAGS do not exist: {mod.__name__} {c.NAME}")
                    c.TAGS = dir_tags

                # rename NAME
                c.NAME = f"{c.NAME} ({dir_name})"
                classes.append(c)

        return classes
