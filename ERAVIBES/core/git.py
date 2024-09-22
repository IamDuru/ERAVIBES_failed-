#
# Copyright (C) 2024 by Iamduru@Github, < https://github.com/IamDuru/ERAVIBES >.
#
# This file is part of < https://github.com/IamDuru/ERAVIBES > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/IamDuru/ERAVIBES/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import shlex
from typing import Tuple

import git

import config

from ..logging import LOGGER

def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())

def git():
    repo_path = '/path/to/your/repo'  # Replace with the actual path to your Git repository
    try:
        repo = git.Repo(repo_path)
        LOGGER.info("Git repository found at: %s", repo_path)

        # Fetch updates from the upstream repository
        origin = repo.remotes.origin
        origin.fetch()
        LOGGER.info("Fetched updates from upstream repository.")

        # Check if the branch exists
        branch_name = config.UPSTREAM_BRANCH
        if branch_name in origin.refs:
            LOGGER.info("Branch %s found in origin.", branch_name)
        else:
            LOGGER.error("Branch %s not found in origin.", branch_name)
            return

        # Checkout the specified branch
        repo.git.checkout(branch_name)
        LOGGER.info("Checked out branch: %s", branch_name)

        # Pull changes from the upstream branch
        origin.pull(branch_name)
        LOGGER.info("Pulled changes from upstream branch: %s", branch_name)

        # Install dependencies using pip
        install_req("pip3 install --no-cache-dir -r requirements.txt")
        LOGGER.info("Installed dependencies.")

    except git.exc.InvalidGitRepositoryError as e:
        LOGGER.error(f"Invalid Git repository at {repo_path}: {e}")
    except git.exc.GitCommandError as e:
        LOGGER.error(f"Error running Git command: {e}")
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred: {e}")
