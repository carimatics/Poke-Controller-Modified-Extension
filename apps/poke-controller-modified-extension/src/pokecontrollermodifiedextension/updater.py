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
        self._needs_backup = False
        self._has_uncommitted_changes = False
        self._diff_files: list[str] = []

    def has_changes(self) -> bool:
        repo = self._repo
        remote = self._remote
        branch = self._branch

        repo.remotes[remote].fetch()

        self._has_uncommitted_changes = repo.is_dirty() or len(repo.untracked_files) > 0

        repo.heads[branch].checkout()

        local_commit = repo.heads[branch].commit
        remote_commit = repo.commit(f"{remote}/{branch}")

        if local_commit == remote_commit:
            print(f"{branch} is already up to date with {remote}/{branch}")
            return False

        has_local_commit = False
        try:
            merge_bases = repo.merge_base(local_commit, remote_commit)
            if merge_bases:
                merge_base = merge_bases[0]

                if local_commit != merge_base:
                    diffs = local_commit.diff(merge_base)
                    self._diff_files = [diff.a_path for diff in diffs if diff.a_path]
                    has_local_commit = True
                    print(f"Local branch has {len(self._diff_files)} changed files")

                if remote_commit != merge_base:
                    remote_diffs = remote_commit.diff(merge_base)
                    print(f"Remote branch has {len(list(remote_diffs))} new changes")

        except Exception as e:
            print(f"Error while getting diff files: {e}")

        self._needs_backup = has_local_commit and self._has_uncommitted_changes

        return True

    def backup(self) -> None:
        if not self._needs_backup:
            return

        repo = self._repo
        remote = self._remote
        branch = self._branch
        diff_files = self._diff_files

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_branch_name = f"backup/{branch}/{timestamp}"
        backup_branch = repo.create_head(backup_branch_name)
        print(f"Created backup branch: {backup_branch_name}")

        if self._has_uncommitted_changes:
            backup_branch.checkout()

            repo.git.add(all=True)
            if repo.is_dirty():
                repo.index.commit(
                    f"Backup uncommitted changes before pulling {remote}/{branch}"
                )

            repo.heads[branch].checkout()

        print("Created backup")
        if diff_files:
            print(f"Backed up files: {diff_files}")
        if self._has_uncommitted_changes:
            print("Saved uncommitted changes")

    def update(self) -> None:
        remote = self._remote
        branch = self._branch

        self._repo.git.reset("--hard", f"{remote}/{branch}")
        print(f"Updated {branch} to {remote}/{branch}")

    def checkout_original_branch(self) -> None:
        original_branch = self._original_branch_name
        current_branch = self._repo.active_branch.name

        if original_branch != current_branch:
            self._repo.heads[original_branch].checkout()
            print(f"Checked out original branch: {original_branch}")
