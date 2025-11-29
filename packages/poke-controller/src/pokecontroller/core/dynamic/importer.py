import inspect
import logging
from importlib.util import module_from_spec, spec_from_file_location
from os import PathLike
from pathlib import Path
from types import ModuleType

logger = logging.getLogger(__name__)


def import_subclasses_from_path[T](
    file_path: str | PathLike[str],
    namespace: str,
    klass: type[T],
) -> list[type[T]]:
    """file_pathで指定されたファイル内にあるTのサブクラスを指定された名前空間のパッケージに登録してから返します。

    Args:
        file_path: 参照したいファイルのパス
        namespace: サブクラスを登録したい名前空間
        klass: 取得したいサブクラスの先祖クラス
    """
    # モジュールをインポート
    module = import_module_from_path(Path(file_path), namespace)

    # 指定されたクラスのサブクラスを検出して返す(そのクラス自体は返さない)
    return [
        obj
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, klass) and obj is not klass
    ]


def import_module_from_path(
    file_path: str | PathLike[str],
    namespace: str,
) -> ModuleType | None:
    """file_pathで指定されたファイルをモジュールとして返す。

    Args:
        file_path: 参照したいファイルのパス
        namespace: サブクラスを登録したい名前空間
    """
    path = Path(file_path)
    if not path.exists():
        print(f"dir_path '{file_path}' not found")
        raise FileNotFoundError("file_path not found")

    # 指定された名前空間に所属させる(名前空間の衝突を避けるため)
    module_name = f"{namespace}.{path.stem}"

    # モジュールの仕様を作成
    spec = spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        logger.warning(f"Could not load spec from {module_name}")
        return None

    # モジュールを作成してロード
    module = module_from_spec(spec)
    try:
        logger.debug(f"Loading {module_name}")
        spec.loader.exec_module(module)
    except Exception as e:
        logger.error(f"Error loading {module_name}")
        print(f"Error loading {module_name} {e}")
        return None
    else:
        return module
