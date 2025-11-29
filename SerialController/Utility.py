from pokecontrollermodifiedextension.core import utils


# for compatibility
def ospath(path):  # noqa
    return utils.ospath(path=path)


# for compatibility
def browseFileNames(path=".", ext="", recursive=True, name_only=True):  # noqa
    return utils.browse_file_names(path=path, ext=ext, recursive=recursive, name_only=name_only)


# for compatibility
def getClassesInModule(module):  # noqa
    return utils.get_classes_in_module(module=module)


# for compatibility
def getModuleNames(base_path):  # noqa
    return utils.get_module_names(base_path=base_path)


# for compatibility
def importAllModules(base_path, mod_names=None):  # noqa
    return utils.get_all_modules(base_path=base_path, mod_names=mod_names)
