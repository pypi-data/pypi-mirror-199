from typing import Optional, Dict, List

from git import Repo
from semver import VersionInfo

from release.constants import DEFAULT_DOMAIN_SEPARATOR, POSSIBLE_DOMAIN_SEPARATORS
from release.exceptions import DifferentDomainException, InvalidReleaseString


class Release:
    def __init__(
        self,
        domain: Optional[str] = None,
        version: Optional[VersionInfo] = None,
        no_patch: bool = False,
        domain_separator: str = DEFAULT_DOMAIN_SEPARATOR,
    ):
        self.domain = domain
        self.version = version
        self.no_patch = no_patch
        self.domain_separator = domain_separator

    @classmethod
    def parse(cls, version: str, domain_separator: Optional[str] = None):
        if domain_separator:
            return cls._parse(version, domain_separator=domain_separator)
        for sep in POSSIBLE_DOMAIN_SEPARATORS:
            try:
                return cls._parse(version, domain_separator=sep)
            except Exception:
                continue
        raise InvalidReleaseString(f"'{version}' is not parsable.")

    @classmethod
    def _parse(cls, version: str, domain_separator=DEFAULT_DOMAIN_SEPARATOR):
        no_patch = False
        domain = None
        if domain_separator in version:
            domain, version = version.split(domain_separator)
        try:
            version = VersionInfo.parse(version)
        except ValueError:
            try:
                version = VersionInfo.parse(f"{version}.0")
                no_patch = True
            except Exception as e:
                raise e
        return cls(
            domain=domain,
            version=version,
            no_patch=no_patch,
            domain_separator=domain_separator,
        )

    def __str__(self):
        version = str(self.version)
        if self.no_patch:
            version = ".".join(version.split(".")[:-1])
        if self.domain:
            return f"{self.domain}{self.domain_separator}{version}"
        return f"{version}"

    def __lt__(self, other):
        if other.domain != self.domain:
            raise DifferentDomainException(
                "Domains should be the same to compare 2 release objects"
            )
        return self.version < other.version

    def __eq__(self, other):
        return self.domain == other.domain and self.version == other.version


def is_valid_release(
    semver: str, domain_separator: str = DEFAULT_DOMAIN_SEPARATOR
) -> bool:
    try:
        Release.parse(semver, domain_separator)
        return True
    except InvalidReleaseString:
        return False


def get_sorted_releases_by_domains(
    repo: Repo, domain_separator: Optional[str] = DEFAULT_DOMAIN_SEPARATOR
) -> Dict[str, List[Release]]:
    releases = [
        Release.parse(tag.name, domain_separator)
        for tag in repo.tags
        if is_valid_release(tag.name, domain_separator)
    ]
    return {
        domain: sorted(
            [r for r in releases if r.domain == domain], key=lambda x: x.version
        )
        for domain in {r.domain for r in releases}
    }


def get_latest_releases_by_domain(
    repo: Repo, domain_separator: str
) -> Dict[str, Release]:
    release_by_domain = get_sorted_releases_by_domains(repo, domain_separator)
    return {domain: rel[-1] for domain, rel in release_by_domain.items()}


def get_latest_release(
    repo: Repo, domain: str, domain_separator: Optional[str]
) -> Release:
    releases = get_latest_releases_by_domain(repo, domain_separator)
    return releases[domain]


def get_next_release(release: Release, part: str):
    return Release(
        domain=release.domain,
        version=release.version.next_version(part=part),
        no_patch=release.no_patch,
        domain_separator=release.domain_separator,
    )


INIT_VERSION = Release(domain=None, version=VersionInfo(major=0, minor=0, patch=0))
