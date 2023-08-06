# pygitversionhelper (c) by chacha
#
# pygitversionhelper  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.
"""
This project try to help doing handy operations with git when 
dealing with project versioning and tags on python project -
at leat for project using PEP440 or SemVer standards.

One requirement is to keep it compact and to not cover too much fancy features.
This is the reason why it is one single file with nested classes.

=> Design is on-purpose poorly expandable to keep the scope light.

This library is maid for repository using tag as version.
Support for non-version tags is optional and not well tested.

This module is the main project file, containing all the code.

Read the read me for more information.
Check the unittest s for usage samples.

Note: _Other Parameters_ are **kwargs
"""

from __future__ import annotations

import os
import subprocess
import re
from copy import copy
import logging

from packaging.version import VERSION_PATTERN as packaging_VERSION_PATTERN


def _exec(cmd: str, root: str | os.PathLike | None = None, raw: bool = False) -> list[str]:
    """
    helper function to handle system cmd execution
    Args:
        cmd: command line to be executed
        root: root directory where the command need to be executed
    Returns:
        a list of command's return lines

    """
    p = subprocess.run(
        cmd,
        text=True,
        cwd=root,
        capture_output=True,
        check=False,
        timeout=2,
        shell=True,
    )
    if re.search("not a git repository", p.stderr):
        raise gitversionhelper.repository.notAGitRepository()
    if re.search("fatal:", p.stderr):
        raise gitversionhelper.unknownGITFatalError(p.stderr)
    if int(p.returncode) < 0:
        raise gitversionhelper.unknownGITError(p.stderr)

    if raw:
        return p.stdout
    lines = p.stdout.splitlines()
    return [line.rstrip() for line in lines if line.rstrip()]


class gitversionhelperException(Exception):
    """
    general Module Exception
    """


class gitversionhelper:  # pylint: disable=too-few-public-methods
    """
    main gitversionhelper class
    """

    class wrongArguments(gitversionhelperException):
        """
        wrong argument generic exception
        """

    class unknownGITError(gitversionhelperException):
        """
        unknown git error generic exception
        """

    class unknownGITFatalError(unknownGITError):
        """
        unknown fatal git error generic exception
        """

    class repository:
        """
        class containing methods focusing on repository
        """

        class repositoryException(gitversionhelperException):
            """
            generic repository exeption
            """

        class notAGitRepository(repositoryException):
            """
            not a git repository exception
            """

        class repositoryDirty(repositoryException):
            """
            dirty repository exception
            """

        @classmethod
        def isDirty(cls) -> bool:
            """
            check if the repository is in dirty state
            Returns:
                True if it is dirty
            """
            return bool(_exec("git status --short"))

    class commit:
        """
        class containing methods focusing on commits
        """

        __OptDict = {"same_branch": "same_branch", "merged_output": "merged_output"}

        class commitException(gitversionhelperException):
            """
            generic commit exception
            """

        class commitNotFound(commitException):
            """
            tag not found exception
            """

        @classmethod
        def getMessagesSinceTag(cls, tag: str, **kwargs) -> str:
            """
            retrieve a commits message history from repository
            from Latest commit to the given tag
            Keyword Arguments:
                merged_output: output one single merged string
                same_branch(bool): force searching only in the same branch
            Returns:
                the commit message
            """
            current_commit_id = cls.getLast(**kwargs)
            tag_commit_id = cls.getFromTag(tag)

            if (cls.__OptDict["same_branch"] in kwargs) and (kwargs[cls.__OptDict["same_branch"]] is True):
                commits = _exec(f"git rev-list --first-parent --ancestry-path {tag_commit_id}..{current_commit_id}")
            else:
                commits = _exec(f"git rev-list --ancestry-path {tag_commit_id}..{current_commit_id}")
            result = []
            for commit in commits:
                result.append(cls.getMessage(commit))

            if (cls.__OptDict["merged_output"] in kwargs) and (kwargs[cls.__OptDict["merged_output"]] is True):
                print("JOIN")
                return os.linesep.join(result)
            return result

        @classmethod
        def getMessage(cls, commit_hash: str) -> str:
            """
            retrieve a commit message from repository
            Args:
                commit_hash: id of the commit
            Returns:
                the commit message
            """
            try:
                res = _exec(
                    f'git log -z --pretty="tformat:%B%-C()" -n 1 {commit_hash}',
                    None,
                    True,
                ).rstrip("\x00")
            except gitversionhelper.unknownGITFatalError as _e:
                raise cls.commitNotFound("no commit found in commit history") from _e

            return res.replace("\r\n", "\n").replace("\n", "\r\n")

        @classmethod
        def getFromTag(cls, tag: str) -> str:
            """
            retrieve a commit from repository associated to a tag
            Args:
                tag: tag of the commit
            Returns:
                the commit Id
            """
            try:
                res = _exec(f"git rev-list -n 1 {tag}")
            except gitversionhelper.unknownGITFatalError as _e:
                raise cls.commitNotFound("no commit found in commit history") from _e
            if len(res) == 0:
                raise cls.commitNotFound("no commit found in commit history")
            return res[0]

        @classmethod
        def getLast(cls, **kwargs) -> str:
            """
            retrieve last commit from repository
            Keyword Arguments:
                same_branch(bool): force searching only in the same branch
            Returns:
                the commit Id
            """
            if (cls.__OptDict["same_branch"] in kwargs) and (kwargs[cls.__OptDict["same_branch"]] is True):
                try:
                    res = _exec("git rev-parse HEAD")
                except gitversionhelper.unknownGITFatalError as _e:
                    raise cls.commitNotFound("no commit found in commit history") from _e
            else:
                res = _exec('git for-each-ref --sort=-committerdate refs/heads/ --count 1 --format="%(objectname)"')

            if len(res) == 0:
                raise cls.commitNotFound("no commit found in commit history")
            return res[0]

    class tag:
        """
        class containing methods focusing on tags
        """

        __OptDict = {"same_branch": "same_branch"}
        __validGitTagSort = [
            "",
            "v:refname",
            "-v:refname",
            "taggerdate",
            "committerdate",
            "-taggerdate",
            "-committerdate",
        ]

        class tagException(gitversionhelperException):
            """
            generic tag exception
            """

        class tagNotFound(tagException):
            """
            tag not found exception
            """

        class moreThanOneTag(tagException):
            """
            more than one tag exception
            """

        @classmethod
        def getTags(cls, sort: str = "taggerdate", **kwargs) -> list[str | None]:
            """
            retrieve all tags from a repository
            Args:
                sort: sorting constraints (git format)
            Returns:
                the tags list
            """

            if sort not in cls.__validGitTagSort:
                raise gitversionhelper.wrongArguments("sort option not in allowed list")

            if (cls.__OptDict["same_branch"] in kwargs) and (kwargs[cls.__OptDict["same_branch"]] is True):
                currentBranch = _exec("git rev-parse --abbrev-ref HEAD")
                return list(reversed(_exec(f"git tag --merged {currentBranch[0]} --sort={sort}")))
            return list(reversed(_exec(f"git tag -l --sort={sort}")))

        @classmethod
        def getLastTag(cls, **kwargs) -> str | None:
            """
            retrieve the Latest tag from a repository
            Keyword Arguments:
                same_branch(bool): force searching only in the same branch
            Returns:
                the tag
            """
            if (cls.__OptDict["same_branch"] in kwargs) and (kwargs[cls.__OptDict["same_branch"]] is True):
                res = _exec("git describe --tags --first-parent --abbrev=0")
            else:
                res = _exec("git rev-list --tags --date-order --max-count=1")
                if len(res) == 1:
                    res = _exec(f"git describe --tags {res[0]}")

            if len(res) == 0:
                raise cls.tagNotFound("no tag found in commit history")
            if len(res) != 1:
                raise cls.moreThanOneTag("multiple tags on same commit is unsupported")
            return res[0]

        @classmethod
        def getDistanceFromTag(cls, tag: str = None, **kwargs) -> int:
            """
            retrieve the distance between Latest commit and tag in the repository
            Arguments:
                tag: reference tag, if None the most recent one will be used
            Keyword Arguments:
                same_branch(bool): force searching only in the same branch
            Returns:
                the tag
            """
            if tag is None:
                tag = cls.getLastTag(**kwargs)
            return int(_exec(f"git rev-list {tag}..HEAD --count")[0])

    class version:
        """
        class containing methods focusing on versions
        """

        __OptDict = {
            "version_std": "version_std",
            "formated_output": "formated_output",
            "output_format": "output_format",
            "ignore_unknown_tags": "ignore_unknown_tags",
        }
        DefaultInputFormat = "Auto"
        VersionStds = {
            "SemVer": {
                "regex": r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
                r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
                r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
                r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
                "regex_preversion_num": r"(?:\.)(?P<num>(?:\d+(?!\w))+)",
                "regex_build_num": r"(?:\.)(?P<num>(?:\d+(?!\w))+)",
            },
            "PEP440": {"regex": packaging_VERSION_PATTERN, "Auto": None},
        }
        __versionReseted = False

        class versionException(gitversionhelperException):
            """
            generic version exception
            """

        class noValidVersion(versionException):
            """
            no valid version found exception
            """

        class PreAndPostVersionUnsupported(versionException):
            """
            pre and post release can not be present at the same time
            """

        class MetaVersion:
            """
            generic version object
            """

            __OptDict = {
                "bump_type": "bump_type",
                "bump_dev_strategy": "bump_dev_strategy",
                "formated_output": "formated_output",
            }
            DefaultBumpType = "patch"
            BumpTypes = ["major", "minor", "patch", "dev"]
            DefaultBumpDevStrategy = "post"
            BumpDevStrategys = ["post", "pre-patch", "pre-minor", "pre-major"]

            version_std: str = "None"
            major: int = 0
            minor: int = 1
            patch: int = 0
            pre_count: int = 0
            post_count: int = 0
            raw: str = "0.1.0"

            def __init__(
                self,
                version_std,
                major=0,
                minor=1,
                patch=0,
                pre_count=0,
                post_count=0,
                raw="0.1.0",
            ):  # pylint: disable=R0913
                self.version_std = version_std
                self.major = major
                self.minor = minor
                self.patch = patch
                self.pre_count = pre_count
                self.post_count = post_count
                self.raw = raw

            @classmethod
            def _getBumpDevStrategy(cls, **kwargs) -> str:
                """
                get selected bump_dev_strategy
                Keyword Arguments:
                    bump_dev_strategy(str): the given bump_dev_strategy (can be None)
                Returns:
                    Kwargs given bump_dev_strategy or the default one.
                """
                BumpDevStrategy = cls.DefaultBumpDevStrategy
                if cls.__OptDict["bump_dev_strategy"] in kwargs:
                    if kwargs[cls.__OptDict["bump_dev_strategy"]] in cls.BumpDevStrategys:
                        BumpDevStrategy = kwargs[cls.__OptDict["bump_dev_strategy"]]
                    else:
                        raise gitversionhelper.wrongArguments(f"invalid {cls.__OptDict['bump_type']} requested")
                return BumpDevStrategy

            @classmethod
            def _getBumpType(cls, **kwargs) -> str:
                """
                get selected bump_type
                Keyword Arguments:
                    bump_type(str): the given bump_type (can be None)
                Returns:
                    Kwargs given bump_type or the default one.
                """
                BumpType = cls.DefaultBumpType
                if cls.__OptDict["bump_type"] in kwargs:
                    if kwargs[cls.__OptDict["bump_type"]] in cls.BumpTypes:
                        BumpType = kwargs[cls.__OptDict["bump_type"]]
                    else:
                        raise gitversionhelper.wrongArguments(f"invalid {cls.__OptDict['bump_type']} requested")
                return BumpType

            def bump(self, amount: int = 1, **kwargs) -> gitversionhelper.version.MetaVersion | str:  # pylint: disable=R0912
                """
                bump the version to the next one
                Keyword Arguments:
                    bump_type(str): the given bump_type (can be None)
                    bump_dev_strategy(str): the given bump_dev_strategy (can be None)
                Returns:
                    the bumped version
                """
                BumpType = self._getBumpType(**kwargs)
                BumpDevStrategy = self._getBumpDevStrategy(**kwargs)
                _v = copy(self)

                if BumpType == "dev":
                    if BumpDevStrategy == "post":
                        if _v.pre_count > 0:
                            _v.pre_count = _v.pre_count + amount
                        else:
                            _v.post_count = _v.post_count + amount
                    # elif BumpDevStrategy in ["pre-patch","pre-minor","pre-major"]:
                    else:
                        if _v.post_count > 0:
                            _v.post_count = _v.post_count + amount
                        else:
                            if _v.pre_count == 0:
                                if BumpDevStrategy == "pre-patch":
                                    _v.patch = _v.patch + 1
                                elif BumpDevStrategy == "pre-minor":
                                    _v.minor = _v.minor + 1
                                    _v.patch = 0
                                # elif BumpDevStrategy == "pre-major":
                                else:
                                    _v.major = _v.major + 1
                                    _v.minor = 0
                                    _v.patch = 0
                            _v.pre_count = _v.pre_count + amount
                else:
                    if BumpType == "major":
                        _v.major = _v.major + amount
                    elif BumpType == "minor":
                        _v.minor = _v.minor + amount
                    # elif BumpType == "patch":
                    else:
                        _v.patch = _v.patch + amount
                    _v.pre_count = 0
                    _v.post_count = 0
                _v.raw = _v.doFormatVersion(**kwargs)

                if (self.__OptDict["formated_output"] in kwargs) and (kwargs[self.__OptDict["formated_output"]] is True):
                    return _v.doFormatVersion(**kwargs)
                return _v

            def doFormatVersion(self, **kwargs) -> str:
                """
                output a formated version string
                Keyword Arguments:
                    output_format: output format to render ("Auto" or "PEP440" or "SemVer")
                Returns:
                    formated version string
                """
                return gitversionhelper.version.doFormatVersion(self, **kwargs)

        @classmethod
        def _getVersionStd(cls, **kwargs) -> str:
            """
            get selected version_std
            Keyword Arguments:
                version_std(str): the given version_std (can be None)
            Returns:
                Kwargs given version_std or the default one.
            """
            VersionStd = cls.DefaultInputFormat
            if cls.__OptDict["version_std"] in kwargs:
                if kwargs[cls.__OptDict["version_std"]] in cls.VersionStds:
                    VersionStd = kwargs[cls.__OptDict["version_std"]]
                else:
                    raise gitversionhelper.wrongArguments(f"invalid {cls.__OptDict['version_std']} requested")
            return VersionStd

        @classmethod
        def getCurrentVersion(cls, **kwargs) -> MetaVersion | str:
            """
            get the current version or bump depending of repository state
            Keyword Arguments:
                version_std(str): the given version_std (can be None)
                same_branch(bool): force searching only in the same branch
                formated_output(bool) : output a formated version string
                bump_type(str): the given bump_type (can be None)
                bump_dev_strategy(str): the given bump_dev_strategy (can be None)
            Returns:
                the last version
            """
            if gitversionhelper.repository.isDirty() is not False:
                raise gitversionhelper.repository.repositoryDirty("The repository is dirty and a current version can not be generated.")
            saved_kwargs = copy(kwargs)
            if "formated_output" in kwargs:
                del saved_kwargs["formated_output"]

            _v = cls.getLastVersion(**saved_kwargs)

            if not cls.__versionReseted:
                amount = gitversionhelper.tag.getDistanceFromTag(_v.raw, **kwargs)
                _v = _v.bump(amount, **saved_kwargs)

            if (cls.__OptDict["formated_output"] in kwargs) and (kwargs[cls.__OptDict["formated_output"]] is True):
                return _v.doFormatVersion(**kwargs)
            return _v

        @classmethod
        def getCurrentFormatedVersion(cls, **kwargs) -> str:
            """
            Same as getCurrentVersion() with formated_output kwarg activated
            """
            kwargs["formated_output"] = True
            return cls.getCurrentVersion(**kwargs)

        @classmethod
        def _parseTag(cls, tag, **kwargs):  # pylint: disable=R0914, R0912, R0915
            """get the last version from tags
            Arguments:
                tag: the tag to be parsed
            Keyword Arguments:
                version_std(str): the given version_std (can be None)
                ignore_unknown_tags(bool): skip tags with not decoded versions (default to False)
            Returns:
                the last version
            """
            VersionStd = cls._getVersionStd(**kwargs)
            bAutoVersionStd = False
            if VersionStd == "Auto":
                bAutoVersionStd = True
            bFound = False
            if VersionStd == "SemVer" or (bAutoVersionStd is True):
                _r = re.compile(
                    r"^\s*" + cls.VersionStds["SemVer"]["regex"] + r"\s*$",
                    re.VERBOSE | re.IGNORECASE,
                )
                _m = re.match(_r, tag)
                if not _m:
                    pass
                else:
                    major, minor, patch = (
                        int(_m.group("major")),
                        int(_m.group("minor")),
                        int(_m.group("patch")),
                    )

                    pre_count = 0
                    if _pre := _m.group("prerelease"):
                        if (_match := re.search(cls.VersionStds["SemVer"]["regex_preversion_num"], _pre)) is not None:
                            pre_count = int(_match.group("num"))
                        else:
                            pre_count = 1

                    post_count = 0
                    if _post := _m.group("buildmetadata"):
                        if (_match := re.search(cls.VersionStds["SemVer"]["regex_build_num"], _post)) is not None:
                            post_count = int(_match.group("num"))
                        else:
                            post_count = 1
                    bFound = True
                    VersionStd = "SemVer"

            if VersionStd == "PEP440" or ((bAutoVersionStd is True) and (bFound is not True)):
                _r = re.compile(
                    r"^\s*" + cls.VersionStds["PEP440"]["regex"] + r"\s*$",
                    re.VERBOSE | re.IGNORECASE,
                )
                _m = re.match(_r, tag)
                if not _m:
                    pass
                else:
                    ver = _m.group("release").split(".")
                    ver += ["0"] * (3 - len(ver))
                    ver[0] = int(ver[0])
                    ver[1] = int(ver[1])
                    ver[2] = int(ver[2])
                    major, minor, patch = tuple(ver)
                    pre_count = int(_m.group("pre_n")) if _m.group("pre_n") else 0
                    post_count = int(_m.group("post_n2")) if _m.group("post_n2") else 0
                    bFound = True
                    VersionStd = "PEP440"

            if not bFound:
                raise gitversionhelper.version.noValidVersion("no valid version found in tags")

            if pre_count > 0 and post_count > 0:
                raise cls.PreAndPostVersionUnsupported("can not parse a version with both pre and post release number.")
            return cls.MetaVersion(VersionStd, major, minor, patch, pre_count, post_count, tag)

        @classmethod
        def getLastVersion(cls, **kwargs) -> MetaVersion | str:  # pylint: disable=R0914, R0912, R0915
            """get the last version from tags
            Keyword Arguments:
                version_std(str): the given version_std (can be None)
                same_branch(bool): force searching only in the same branch
                formated_output(bool) : output a formated version string
                ignore_unknown_tags(bool): skip tags with not decoded versions (default to False)
            Returns:
                the last version
            """
            lastTag = cls.MetaVersion.raw
            cls.__versionReseted = False
            try:
                lastTag = gitversionhelper.tag.getLastTag(**kwargs)
            except gitversionhelper.tag.tagNotFound:
                logging.warning("tag not found, reseting versionning")
                cls.__versionReseted = True

            _v = None
            try:
                _v = cls._parseTag(lastTag, **kwargs)
            except gitversionhelper.version.noValidVersion as _ex:
                if (cls.__OptDict["ignore_unknown_tags"] in kwargs) and (kwargs[cls.__OptDict["ignore_unknown_tags"]] is True):
                    tags = gitversionhelper.tag.getTags(sort="taggerdate", **kwargs)
                    _v = None
                    for _tag in tags:
                        try:
                            _v = cls._parseTag(_tag, **kwargs)
                            break
                        except gitversionhelper.version.noValidVersion:
                            continue
                if _v is None:
                    raise gitversionhelper.version.noValidVersion() from _ex

            if (cls.__OptDict["formated_output"] in kwargs) and (kwargs[cls.__OptDict["formated_output"]] is True):
                return _v.doFormatVersion(**kwargs)
            return _v

        @classmethod
        def doFormatVersion(cls, inputversion: MetaVersion, **kwargs) -> str:
            """
            output a formated version string
            Keyword Arguments:
                output_format: output format to render ("Auto" or "PEP440" or "SemVer")
            Args:
                inputversion: version to be rendered
            Returns:
                formated version string
            """

            VersionStd = cls._getVersionStd(**kwargs)
            if VersionStd == "Auto":
                VersionStd = inputversion.version_std

            OutputFormat = None
            revpattern = ""
            revcount = ""
            post_count = inputversion.post_count
            pre_count = inputversion.pre_count
            patch = inputversion.patch

            if cls.__OptDict["output_format"] in kwargs:
                OutputFormat = kwargs[cls.__OptDict["output_format"]]

            if OutputFormat is None:
                OutputFormat = "{major}.{minor}.{patch}{revpattern}{revcount}"
                if post_count > 0 and pre_count > 0:
                    raise gitversionhelper.version.PreAndPostVersionUnsupported(
                        "cannot output a version with both pre and post release number."
                    )
                if VersionStd == "PEP440":
                    if post_count > 0:
                        revpattern = ".post"
                        revcount = f"{post_count}"
                    elif pre_count > 0:
                        revpattern = ".pre"
                        revcount = f"{pre_count}"
                # elif    VersionStd == "SemVer":
                else:
                    if post_count > 0:
                        revpattern = "+post"
                        revcount = f".{post_count}"
                    elif pre_count > 0:
                        revpattern = "-pre"
                        revcount = f".{pre_count}"
            return OutputFormat.format(
                major=inputversion.major,
                minor=inputversion.minor,
                patch=patch,
                revpattern=revpattern,
                revcount=revcount,
            )
