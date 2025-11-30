from mypy.moduleinspect import ModuleType

from pokecontrollermodifiedextension.core import utils


# for compatibility
def ospath(path: str):  # noqa
    return utils.ospath(path=path)


# for compatibility
def browseFileNames(  # noqa
    path: str = ".",
    ext: str = "",
    recursive: bool = True,
    name_only: bool = True,
):
    return utils.browse_file_names(
        path=path,
        ext=ext,
        recursive=recursive,
        name_only=name_only,
    )


# for compatibility
def getClassesInModule(module: ModuleType):  # noqa
    return utils.get_classes_in_module(module=module)


# for compatibility
def getModuleNames(base_path: str):  # noqa
    return utils.get_module_names(base_path=base_path)


# for compatibility
def importAllModules(base_path: str, mod_names: list[str] | None = None):  # noqa
    return utils.get_all_modules(base_path=base_path, mod_names=mod_names)
