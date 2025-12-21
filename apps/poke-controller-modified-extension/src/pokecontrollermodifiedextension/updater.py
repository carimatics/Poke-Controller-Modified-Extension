import logging
from datetime import datetime

from git import Repo

from pokecontrollermodifiedextension.core.runtime_info import get_app_runtime_info

logger = logging.getLogger(__name__)


class PokeControllerUpdater:
    def __init__(
        self,
        remote: str = "origin",
        branch: str = "master",
    ) -> None:
        self._remote = remote
        self._branch = branch

        runtime_info = get_app_runtime_info()
        self._repository_root = runtime_info.base_dir.parent
        self._repo = Repo(self._repository_root)
        self._current_branch = self._repo.active_branch.name
        self._backup_branch_name = ""
        self._diff_files: list[str] = []

    def has_changes(self) -> bool:
        repo = self._repo
        current_branch = self._current_branch

        repo.remotes[self._remote].fetch()

        try:
            merge_bases = repo.merge_base("HEAD", f"{self._remote}/{current_branch}")
            if merge_bases:
                merge_base = merge_bases[0]
                diffs = repo.commit(merge_base).diff(repo.head.commit)
                self._diff_files = [diff.a_path for diff in diffs if diff.a_path]
        except Exception as e:
            logger.error(f"Error while getting diff files: {e}")

        return (
            repo.is_dirty()
            or len(repo.untracked_files) > 0
            or len(self._diff_files) > 0
        )

    def backup(self) -> None:
        repo = self._repo
        current_branch = self._current_branch
        diff_files = self._diff_files

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._backup_branch_name = f"backup/{current_branch}/{timestamp}"
        backup_branch = repo.create_head(self._backup_branch_name)

        backup_branch.checkout()
        repo.git.add(all=True)

        if repo.is_dirty():
            repo.index.commit(f"Backup before pulling {self._remote}/{current_branch}")
            logger.info(f"Created backup branch: {self._backup_branch_name}")
            if diff_files:
                logger.info(f"Conflicted files: {diff_files}")

        repo.heads[current_branch].checkout()

    def update(self) -> None:
        repo = self._repo
        remote = self._remote
        current_branch = self._current_branch

        repo.git.reset("--hard", f"{remote}/{current_branch}")
        logger.info(f"Updated {current_branch} to {remote}/{current_branch}")
