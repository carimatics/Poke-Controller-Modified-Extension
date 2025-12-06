#!/usr/bin/env -S uv run --script
# @formatter:off
#MISE description="Lint the codebase"
#MISE dir="{{cwd}}"
#USAGE flag "--fix" help="Auto fix issues" default=#false
# @formatter:on

from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.utils.command import CrossPlatformCommand, get_usage_envs

if __name__ == '__main__':
    # Get the profile and dev flags from the environment
    env: dict[str, str] = get_usage_envs(("fix",))

    # Construct the command to run
    fix_flag: list[str] = ["--fix"] if env["fix"] == "true" else []

    # Run the command
    _ = CrossPlatformCommand().run(
        command=["uv", "run", "ruff", "check", *fix_flag],
        cwd=project_root,
    )
