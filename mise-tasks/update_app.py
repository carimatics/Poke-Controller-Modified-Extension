#!/usr/bin/env -S uv run --script
# @formatter:off
#MISE description="Update Poke-Controller Modified Extension"
#MISE dir="{{cwd}}"
# @formatter:on

from tkinter import messagebox
from pathlib import Path

from pokecontrollermodifiedextension.updater import PokeControllerUpdater


def _update_repository() -> None:
    root = Path(__file__).parent.parent
    updater = PokeControllerUpdater(root=root)
    if not updater.has_changes():
        return

    if messagebox.askyesno(
        title="更新確認",
        message="最新版が公開されています。更新しますか？",
        detail="詳細",
    ):
        try:
            updater.backup()
            updater.update()
        except Exception as e:
            logger.error(f"Error while updating repository: {e}")
            messagebox.showinfo(
                title="更新確認",
                message="更新に失敗しました。\n手動でGitリポジトリを最新に更新してください。"
            )
            return
        messagebox.showinfo(
            title="更新確認",
            message="更新が完了しました。",
        )


if __name__ == '__main__':
    _update_repository()
