from datetime import datetime
from pathlib import Path

from git import Repo


class PokeControllerUpdater:
    def __init__(
        self,
        root: str,
        remote: str = "origin",
        branch: str = "master",
    ) -> None:
        self._root = Path(root)
        self._remote = remote
        self._branch = branch

        self._repo = Repo(self._root)
        self._original_branch_name = self._repo.active_branch.name
        self._backup_branch_name = ""
        self._has_uncommitted_changes = False
        self._has_committed_changes = False
        self._diff_files: list[str] = []

    def has_changes(self) -> bool:
        repo = self._repo
        remote = self._remote
        branch = self._branch

        repo.remotes[remote].fetch()

        self._has_uncommitted_changes = repo.is_dirty() or len(repo.untracked_files) > 0

        repo.heads[branch].checkout()

        try:
            local_ref = f"refs/heads/{branch}"
            remote_ref = f"{remote}/{branch}"
            merge_bases = repo.merge_base(local_ref, remote_ref)
            if merge_bases:
                merge_base = merge_bases[0]
                local_commit = repo.heads[branch].commit

                if local_commit != repo.commit(remote_ref):
                    diffs = local_commit.diff(merge_base)
                    self._diff_files = [diff.a_path for diff in diffs if diff.a_path]
                    self._has_committed_changes = len(self._diff_files) > 0
        except Exception as e:
            print(f"Error while getting diff files: {e}")

        has_any_changes = self._has_uncommitted_changes or self._has_committed_changes

        return has_any_changes

    def backup(self) -> None:
        repo = self._repo
        remote = self._remote
        branch = self._branch
        diff_files = self._diff_files

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._backup_branch_name = f"backup/{branch}/{timestamp}"
        backup_branch = repo.create_head(self._backup_branch_name)
        print(f"Created backup branch: {self._backup_branch_name}")

        if self._has_uncommitted_changes:
            backup_branch.checkout()

            repo.git.add(all=True)
            if repo.is_dirty():
                repo.index.commit(
                    f"Backup uncommitted changes before pulling {remote}/{branch}"
                )

            repo.heads[branch].checkout()

        if diff_files:
            print(f"Changed files (committed): {diff_files}")
        if self._has_uncommitted_changes:
            print("Saved uncommitted changes")

    def update(self) -> None:
        repo = self._repo
        remote = self._remote
        branch = self._branch

        repo.git.reset("--hard", f"{remote}/{branch}")
        print(f"Updated {branch} to {remote}/{branch}")

    def checkout_original_branch(self) -> None:
        original_branch_name = self._original_branch_name

        self._repo.heads[original_branch_name].checkout()
        print(f"Checked out original branch: {original_branch_name}")
