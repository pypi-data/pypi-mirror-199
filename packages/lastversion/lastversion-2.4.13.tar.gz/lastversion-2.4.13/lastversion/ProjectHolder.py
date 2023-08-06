# -*- coding: utf-8 -*-

import logging
import os
import platform
import re

import requests
from appdirs import user_cache_dir
from cachecontrol import CacheControlAdapter
from cachecontrol.caches.file_cache import FileCache
from packaging.version import InvalidVersion

from .Version import Version
from .__about__ import __version__
# this class basically corresponds to something (often a website) which holds
# projects (usually a bunch). often this is a github-like website, so we subclass session
# but this also maybe something special, which either way can be used as a source of version
# information for a project based on its URL or name (see LocalVersionSession)
# it is instantiated with a particular project in mind/set, but also has some methods for
# stuff like searching one
from .utils import asset_does_not_belong_to_machine

log = logging.getLogger(__name__)


def matches_filter(filter_s, positive, version_s):
    """Check if version string matches a filter string.

    Args:
        filter_s (str):  Filter string.
        positive (bool): Whether filter is positive or negative.
        version_s (str): Version string, often a tag name.

    Returns:
        bool: True if version matches filter, False otherwise.
    """
    if not filter_s:
        return True

    if filter_s.startswith('!'):
        positive = not positive
        filter_s = filter_s[1:]
    if filter_s.startswith('~'):
        filter_s = re.compile(r'{}'.format(filter_s.lstrip('~')))
        return positive == bool(re.search(filter_s, version_s))
    return positive == bool(filter_s in version_s)


class ProjectHolder(requests.Session):
    """Generic project holder class abstracts a web-accessible project storage."""

    # List of odd repos where last char is part of version not beta level
    LAST_CHAR_FIX_REQUIRED_ON = []

    # web accessible project holders may have single well-known domain usable by everyone
    # in case of GitHub, that is GitHub.com, for Mercurial web gui - here isn't one, etc.
    DEFAULT_HOSTNAME = None
    SUBDOMAIN_INDICATOR = None
    KNOWN_REPO_URLS = {}
    KNOWN_REPOS_BY_NAME = {}
    # e.g. owner/project, but mercurial just /project together with hostname
    # adapter array should list how many elements make up "repo", e.g. for hg.nginx.com/repo it
    # is only one instead of 2
    # or a "format" specifier for matching
    REPO_URL_PROJECT_COMPONENTS = 2
    # if URI starts with project name, 0. Otherwise, skip through this many URI dirs
    REPO_URL_PROJECT_OFFSET = 0
    RELEASE_URL_FORMAT = None
    SHORT_RELEASE_URL_FORMAT = None

    def set_repo(self, repo):
        """Set repo ID property of project holder instance."""
        self.repo = repo
        self.name = repo.split('/')[-1]

    def __init__(self):
        super(ProjectHolder, self).__init__()

        app_name = __name__.split('.')[0]

        self.cache_dir = user_cache_dir(app_name)
        log.info("Using cache directory: {}.".format(self.cache_dir))
        self.cache = FileCache(self.cache_dir)
        cache_adapter = CacheControlAdapter(cache=self.cache)
        self.mount("http://", cache_adapter)
        self.mount("https://", cache_adapter)

        self.headers.update({'User-Agent': '{}/{}'.format(app_name, __version__)})
        log.info('Created instance of {}'.format(type(self).__name__))
        self.branches = None
        self.only = None
        self.exclude = None
        self.having_asset = None
        self.hostname = None
        # identifies project on a given hostname
        self.repo = None
        # short name for "repo", useful in URLs
        self.name = None
        # in some case we do not specify repo, but feed is discovered, no repo is given then
        self.feed_url = None
        self.even = False

    def is_valid(self):
        """Check if project holder is valid instance."""
        return self.feed_url or self.name

    def set_branches(self, branches):
        """Sets project holder's branches."""
        self.branches = branches

    def set_only(self, only):
        """Sets "only" tag selector for this holder."""
        self.only = only
        if only:
            log.info('Only considering tags with "{}"'.format(only))
        return self

    def set_exclude(self, exclude):
        """Sets "exclude" tag selector for this holder."""
        self.exclude = exclude
        if exclude:
            log.info('Only considering tags without "{}"'.format(exclude))
        return self

    def set_even(self, even):
        """Set to return only releases with even numbering like 1.2.3."""
        self.even = even
        if even:
            log.info('Only considering releases with even numbering')
        return self

    def set_having_asset(self, having_asset):
        """Sets "having_asset" selector for this holder."""
        self.having_asset = having_asset
        if having_asset:
            log.info('Only considering releases with asset "{}"'.format(having_asset))
        return self

    @classmethod
    def get_host_repo_for_link(cls, repo):
        """Return hostname and repo from a link."""
        hostname = None
        # return repo modified to result of extraction
        if repo.startswith(('https://', 'http://')):
            # parse hostname for passing to whatever holder selected
            url_parts = repo.split('/')
            hostname = url_parts[2]
            offset = 3 + cls.REPO_URL_PROJECT_OFFSET
            repo = "/".join(url_parts[offset:offset + cls.REPO_URL_PROJECT_COMPONENTS])
        return hostname, repo

    @classmethod
    def is_official_for_repo(cls, repo):
        """Check if repo is a known repo for this type of project holder."""
        if repo.startswith(('https://', 'http://')):
            for url in cls.KNOWN_REPO_URLS:
                if repo.startswith((url, "https://{}".format(url), "http://{}".format(url))):
                    log.info('{} Starts with {}'.format(repo, url))
                    return cls.KNOWN_REPO_URLS[url]
        else:
            if repo.lower() in cls.KNOWN_REPOS_BY_NAME:
                log.info('Selecting known repo {}'.format(repo))
                return cls.KNOWN_REPOS_BY_NAME[repo.lower()]
        return False

    @classmethod
    def get_matching_hostname(cls, repo):
        """Find matching hostname between repo and holder's default hostname."""
        if not repo.startswith(('http://', 'https://')):
            return None
        if not cls.DEFAULT_HOSTNAME and not cls.SUBDOMAIN_INDICATOR:
            return None
        url_parts = repo.split('/')
        domain = url_parts[2]
        if cls.DEFAULT_HOSTNAME == domain:
            return domain
        if cls.SUBDOMAIN_INDICATOR and domain.startswith(cls.SUBDOMAIN_INDICATOR + "."):
            return domain
        return None

    def matches_major_filter(self, version, major):
        if self.branches and major in self.branches and \
                re.search(r"{}".format(self.branches[major]), str(version)):
            log.info('{} matches major {}'.format(version, self.branches[major]))
            return True
        if str(version).startswith('{}.'.format(major)):
            log.info('{} is under the desired major {}'.format(
                version, major))
            return True
        if str(version) == major:
            return True
        return False

    def sanitize_version(self, version_s, pre_ok=False, major=None):
        """Extract version from tag name."""
        log.info("Sanitizing string {} as a satisfying version.".format(version_s))
        res = False
        if not matches_filter(self.only, True, version_s):
            log.info('"{}" does not match the "only" constraint "{}"'.format(version_s, self.only))
            return False
        if not matches_filter(self.exclude, False, version_s):
            log.info('"{}" does not match the "exclude" constraint "{}"'.format(version_s, self.exclude))
            return False
        try:
            char_fix_required = self.repo in self.LAST_CHAR_FIX_REQUIRED_ON
            v = Version(version_s, char_fix_required=char_fix_required)
            if not v.is_prerelease or pre_ok:
                log.info("Parsed as Version OK. String representation: {}.".format(v))
                res = v
            else:
                log.info("Parsed as unwanted pre-release version: {}.".format(v))
        except InvalidVersion:
            log.info("Failed to parse {} as Version.".format(version_s))
            # attempt to remove extraneous chars and revalidate
            # we use findall for cases where "tag" may be 'foo/2.x/2.45'
            matches = re.findall(r'([0-9]+([.][0-9x]+)+(rc[0-9]?)?)', version_s)
            for s in matches:
                version_s = s[0]
                log.info("Sanitized tag name value to {}.".format(version_s))
                # 1.10.x is a dev release without clear version, so even pre ok will not get it
                if not version_s.endswith('.x'):
                    # we know regex is valid version format, so no need to try catch
                    res = Version(version_s)
                if res:
                    # satisfy on the first matched version-like string, e.g. 5.2.6-3.12
                    break
            if not matches:
                log.info("Did not find anything that looks like a version in the tag")
                # as a last resort, let's try to convert underscores to dots, while stripping out
                # any "alphanumeric_". many hg repos do this, e.g. PROJECT_1_2_3
                parts = version_s.split('_')
                if len(parts) >= 2 and parts[0].isalpha():
                    # gets list except first item, joins by dot
                    version_s = '.'.join(parts[1:])
                    try:
                        v = Version(version_s)
                        if not v.is_prerelease or pre_ok:
                            log.info("Parsed as Version OK")
                            log.info("String representation of version is {}.".format(v))
                            res = v
                        else:
                            log.info("Parsed as unwanted pre-release version: {}.".format(v))
                    except InvalidVersion:
                        log.info('Still not a valid version after applying underscores fix')
        # apply --major filter
        if res and major and not self.matches_major_filter(res, major):
            log.info('{} is not under the desired major {}'.format(
                version_s, major))
            res = False
        if res and self.even and not res.even:
            return False
        return res

    def _type(self):
        """Get project holder's class name."""
        return self.__class__.__name__

    def release_download_url(self, release, shorter=False):
        """Get release download URL."""
        if not self.RELEASE_URL_FORMAT:
            raise NotImplementedError(
                'Getting release URL for {} is not implemented'.format(self._type()))
        ext = 'zip' if os.name == 'nt' else 'tar.gz'

        fmt = self.SHORT_RELEASE_URL_FORMAT if shorter and self.SHORT_RELEASE_URL_FORMAT else \
            self.RELEASE_URL_FORMAT

        return fmt.format(
            hostname=self.hostname,
            repo=self.repo,
            name=self.name,
            tag=release['tag_name'],
            ext=ext,
            version=release['version']
        )

    def get_assets(self, release, short_urls, assets_filter=None):
        urls = []
        assets = release.get('assets', [])
        arch_matched_assets = []
        if not assets_filter and platform.machine() in ['x86_64', 'AMD64']:
            for asset in assets:
                if 'x86_64' in asset['name']:
                    arch_matched_assets.append(asset)
            if arch_matched_assets:
                assets = arch_matched_assets

        if assets:
            for asset in assets:
                if assets_filter and not re.search(assets_filter, asset['name']):
                    continue
                if not assets_filter and asset_does_not_belong_to_machine(asset['name']):
                    continue
                urls.append(asset['browser_download_url'])
        else:
            download_url = self.release_download_url(release, short_urls)
            if not assets_filter or re.search(assets_filter, download_url):
                urls.append(download_url)
        return urls

    def get_canonical_link(self):
        if self.feed_url:
            return self.feed_url
        return 'https://{}/{}'.format(self.hostname, self.repo)
