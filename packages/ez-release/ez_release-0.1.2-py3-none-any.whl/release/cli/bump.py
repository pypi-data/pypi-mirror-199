import enum

from git import Repo

from release.exceptions import ActiveBranchNotMainException, DirtyTreeException
from release.constants import MAIN_BRANCH_NAMES


class Parts(str, enum.Enum):
    MAJOR: str = "major"
    MINOR: str = "minor"
    PATCH: str = "patch"


def is_active_branch_main(repo: Repo):
    """Check whether active branch is main."""
    return repo.active_branch.name in MAIN_BRANCH_NAMES


def raise_on_non_main_branch(repo: Repo):
    """Raises exception if active branch is not main."""
    if not is_active_branch_main(repo):
        raise ActiveBranchNotMainException("You must work on main branch.")


def raise_on_dirty(repo: Repo):
    """Raises exception if tree is dirty."""
    if repo.is_dirty():
        raise DirtyTreeException(
            "Tree is dirty. Commit, checkout or stash your changes."
        )
