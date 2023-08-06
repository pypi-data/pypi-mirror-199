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

This library is made for repository that uses tags as version.
Support for non-version tags is optional and not well tested.

This module is the main project file, containing all the code.

Read the read me for more information.
Check the unittest s for usage samples.

///Note
_Other Parameters_ are **kwargs
///

Attributes:
    TKwargs: Kwargs type definition for type hints
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, TypedDict, Literal
import os
import subprocess
import re
from copy import copy
import logging
from pathlib import Path

from packaging.version import VERSION_PATTERN as packaging_VERSION_PATTERN

if TYPE_CHECKING:
    from typing import List, Optional, Any, Dict
    from typing_extensions import Unpack

    TKwargs = TypedDict(
        "TKwargs",
        {
            "version_std": Optional[str],
            "same_branch": Optional[bool],
            "formated_output": Optional[bool],
            "bump_type": Optional[str],
            "bump_dev_strategy": Optional[str],
            "merged_output": Optional[bool],
            "ignore_unknown_tags": Optional[bool],
            "output_format": Optional[str],
            "ignore_merged": Optional[bool],
        },
        total=False,
    )


def _exec(cmd: str, root: Optional[str | os.PathLike[str]] = None, raw: bool = False) -> str | List[str]:
    """helper function to handle system cmd execution
    Args:
        cmd: command line to be executed
        root: root directory where the command need to be executed
        raw: return bytes if True, str if False or None
    Returns:
        a list of command's return lines or the raw output

    """
    _root: Path
    if isinstance(root, str):
        _root = Path(root)
    elif isinstance(root, os.PathLike):
        _root = Path(root)
    else:
        _root = Path(os.getcwd())

    p = subprocess.run(
        cmd,
        text=True,
        cwd=_root,
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

    if raw is True:
        return p.stdout
    lines = p.stdout.splitlines()
    return [line.rstrip() for line in lines if line.rstrip()]


class gitversionhelperException(Exception):
    """general Module Exception"""


class gitversionhelper:  # pylint: disable=too-few-public-methods
    """main gitversionhelper class"""

    class wrongArguments(gitversionhelperException):
        """wrong argument generic exception"""

    class unknownGITError(gitversionhelperException):
        """unknown git error generic exception"""

    class unknownGITFatalError(unknownGITError):
        """unknown fatal git error generic exception"""

    class repository:
        """class containing methods focusing on repository"""

        class repositoryException(gitversionhelperException):
            """generic repository exeption"""

        class notAGitRepository(repositoryException):
            """not-a-git-repository repository exception"""

        class repositoryDirty(repositoryException):
            """dirty-repository repository exception"""

        @classmethod
        def isDirty(cls) -> bool:
            """check if the repository is in dirty state
            Returns:
                True if it is dirty
            """
            return bool(_exec("git status --short"))

    class commit:
        """class containing methods focusing on commits"""

        class commitException(gitversionhelperException):
            """generic commit exception"""

        class commitNotFound(commitException):
            """tag not found exception"""

        @classmethod
        def getMessagesSinceTag(cls, tag: str, **kwargs: Unpack[TKwargs]) -> str | List[str]:
            """Retrieve a commits message history from repository.

            Start from Latest found commit until the given tag.
            Args:
                tag: tag of the commit where search will stop
            Keyword Arguments:
                kwargs/merged_output (bool): Output one single merged string
                kwargs/same_branch (bool): Force searching only in the same branch
                kwargs/ignore_merged (bool): ignore merged commits
            Returns:
                the commit message
            """
            current_commit_id = cls.getLast(**kwargs)
            tag_commit_id = cls.getFromTag(tag)

            str_cmd: str
            if ("same_branch" in kwargs) and (kwargs["same_branch"] is True):
                str_cmd = f"git rev-list --first-parent {tag_commit_id}..{current_commit_id}"  # ok
            else:
                str_cmd = f"git rev-list {tag_commit_id}..{current_commit_id}"  # ok

            if ("ignore_merged" in kwargs) and (kwargs["ignore_merged"] is True):
                str_cmd = str_cmd + " --no-merges"  # ok

            try:
                commits = _exec(str_cmd)
            except gitversionhelper.unknownGITFatalError as _e:
                raise cls.commitNotFound("no commit found in commit history") from _e

            result = []
            for commit in commits:
                result.append(cls.getMessage(commit))

            if ("merged_output" in kwargs) and (kwargs["merged_output"] is True):
                return os.linesep.join(result)
            return result

        @classmethod
        def getMessage(cls, commit_hash: str) -> str:
            """retrieve a commit message from repository
            Args:
                commit_hash: id of the commit
            Returns:
                the commit message
            """
            try:
                res = _exec(
                    f'git log -z --pretty="tformat:%B%-C()" -n 1 {commit_hash}',  # ok
                    None,
                    True,
                )
                res = cast(str, res).rstrip("\x00")
            except gitversionhelper.unknownGITFatalError as _e:
                raise cls.commitNotFound("no commit found in commit history") from _e

            return res.replace("\r\n", "\n").replace("\n", "\r\n")

        @classmethod
        def getFromTag(cls, tag: str) -> str:
            """retrieve a commit from repository associated to a tag
            Args:
                tag: tag of the commit
            Returns:
                the commit Id
            """
            try:
                res = _exec(f"git rev-list -n 1 {tag}")  # ok
            except gitversionhelper.unknownGITFatalError as _e:
                raise cls.commitNotFound("no commit found in commit history") from _e

            if len(res) == 0:
                raise cls.commitNotFound("no commit found in commit history")
            return res[0]

        @classmethod
        def getLast(cls, **kwargs: Unpack[TKwargs]) -> str:
            """retrieve last commit from repository
            Keyword Arguments:
                kwargs/same_branch (bool): force searching only in the same branch
                kwargs/ignore_merged (bool): ignore merged commits
            Returns:
                the commit Id
            """
            str_cmd: str
            if ("same_branch" in kwargs) and (kwargs["same_branch"] is True):
                str_cmd = "git rev-list --max-count=1 --date-order HEAD --first-parent"  # ok
            else:
                str_cmd = "git log --format=%H --all -n1"  # ok

            if ("ignore_merged" in kwargs) and (kwargs["ignore_merged"] is True):
                str_cmd = str_cmd + " --no-merges"  # ok

            try:
                res = _exec(str_cmd)
            except gitversionhelper.unknownGITFatalError as _e:
                raise cls.commitNotFound("no commit found in commit history") from _e

            if len(res) == 0:
                raise cls.commitNotFound("no commit found in commit history")
            return res[0]

    class tag:
        """class containing methods focusing on tags"""

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
            """generic tag exception"""

        class tagNotFound(tagException):
            """tag-not-found tag exception"""

        class moreThanOneTag(tagException):
            """more-than-one-tag tag exception"""

        @classmethod
        def getTags(cls, Sort: str = "taggerdate", **kwargs: Unpack[TKwargs]) -> List[str]:
            """retrieve all tags from a repository
            Args:
                Sort: sorting constraints (git format)
            Keyword Arguments:
                kwargs/same_branch (bool): force searching only in the same branch
            Returns:
                the tags list
            """

            if Sort not in cls.__validGitTagSort:
                raise gitversionhelper.wrongArguments("Sort option not in allowed list")

            if ("same_branch" in kwargs) and (kwargs["same_branch"] is True):
                currentBranch = _exec("git rev-parse --abbrev-ref HEAD")
                return list(reversed(_exec(f"git tag --merged {currentBranch[0]} --sort={Sort}")))
            return list(reversed(_exec(f"git tag -l --sort={Sort}")))

        @classmethod
        def getLastTag(cls, **kwargs: Unpack[TKwargs]) -> str:
            """retrieve the Latest tag from a repository
            Keyword Arguments:
                kwargs/same_branch (bool): force searching only in the same branch
            Returns:
                the tag
            """
            if ("same_branch" in kwargs) and (kwargs["same_branch"] is True):
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
        def getDistanceFromTag(cls, tag: Optional[str] = None, **kwargs: Unpack[TKwargs]) -> int:
            """retrieve the distance between Latest commit and tag in the repository
            Arguments:
                tag: reference tag, if None the most recent one will be used
            Keyword Arguments:
                kwargs/same_branch (bool): force searching only in the same branch
            Returns:
                the tag
            """
            if tag is None:
                tag = cls.getLastTag(**kwargs)
            return int(_exec(f"git rev-list {tag}..HEAD --count")[0])

    class version:
        """class containing methods focusing on versions"""

        DefaultInputFormat = "Auto"

        TVersionStds = TypedDict("TVersionStds", {"regex": str, "regex_preversion_num": str, "regex_build_num": str}, total=False)

        VersionStds: dict[str, TVersionStds] = {
            "SemVer": {
                "regex": r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
                r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
                r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
                r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
                "regex_preversion_num": r"(?:\.)(?P<num>(?:\d+(?!\w))+)",
                "regex_build_num": r"(?:\.)(?P<num>(?:\d+(?!\w))+)",
            },
            "PEP440": {"regex": packaging_VERSION_PATTERN},
        }
        __versionReseted = False

        class versionException(gitversionhelperException):
            """generic version exception"""

        class noValidVersion(versionException):
            """no valid version found exception"""

        class PreAndPostVersionUnsupported(versionException):
            """pre and post release can not be present at the same time"""

        class MetaVersion:
            """generic version object"""

            TBumpTypes = Literal["major", "minor", "patch", "dev"]
            DefaultBumpType: TBumpTypes = "patch"
            BumpTypes: set[TBumpTypes] = {"major", "minor", "patch", "dev"}

            TBumpDevStrategies = Literal["post", "pre-patch", "pre-minor", "pre-major"]
            DefaultBumpDevStrategy: TBumpDevStrategies = "post"
            BumpDevStrategies: set[TBumpDevStrategies] = {"post", "pre-patch", "pre-minor", "pre-major"}

            TVersionStd = Literal["Auto", "PEP440", "SemVer"]
            version_std: TVersionStd = "Auto"
            major: int = 0
            minor: int = 1
            patch: int = 0
            pre_count: int = 0
            post_count: int = 0
            raw: str = "0.1.0"

            def __init__(
                self,
                version_std: TVersionStd = "Auto",
                major: int = 0,
                minor: int = 1,
                patch: int = 0,
                pre_count: int = 0,
                post_count: int = 0,
                raw: str = "0.1.0",
            ):  # pylint: disable=R0913
                self.version_std = version_std
                self.major = major
                self.minor = minor
                self.patch = patch
                self.pre_count = pre_count
                self.post_count = post_count
                self.raw = raw

            @classmethod
            def _getBumpDevStrategy(cls, **kwargs: Unpack[TKwargs]) -> str:
                """get selected bump_dev_strategy
                Keyword Arguments:
                    kwargs/bump_dev_strategy (str): the given bump_dev_strategy (can be None)
                Returns:
                    Kwargs given bump_dev_strategy or the default one.
                """
                BumpDevStrategy: str = cls.DefaultBumpDevStrategy

                if kwargs and ("bump_dev_strategy" in kwargs):
                    if kwargs["bump_dev_strategy"] in cls.BumpDevStrategies:
                        BumpDevStrategy = kwargs["bump_dev_strategy"]
                    else:
                        raise gitversionhelper.wrongArguments(f"invalid {'bump_type'} requested")
                return BumpDevStrategy

            @classmethod
            def _getBumpType(cls, **kwargs: Unpack[TKwargs]) -> str:
                """get selected bump_type
                Keyword Arguments:
                    kwargs/bump_type (str): the given bump_type (can be None)
                Returns:
                    Kwargs given bump_type or the default one.
                """
                BumpType: str = cls.DefaultBumpType
                if "bump_type" in kwargs:
                    if kwargs["bump_type"] in cls.BumpTypes:
                        BumpType = kwargs["bump_type"]
                    else:
                        raise gitversionhelper.wrongArguments(f"invalid {'bump_type'} requested")
                return BumpType

            def bump(  # pylint: disable=R1260,R0912
                self, amount: int = 1, **kwargs: Unpack[TKwargs]
            ) -> gitversionhelper.version.MetaVersion | str:
                """bump the version to the next one
                Args:
                    amount: number of revision to bump
                Keyword Arguments:
                    kwargs/bump_type (str): the given bump_type (can be None)
                    kwargs/bump_dev_strategy (str): the given bump_dev_strategy (can be None)
                Returns:
                    the bumped version
                """

                BumpType: str = self._getBumpType(**kwargs)

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

                if ("formated_output" in kwargs) and (kwargs["formated_output"] is True):
                    return _v.doFormatVersion(**kwargs)
                return _v

            def doFormatVersion(self, **kwargs: Unpack[TKwargs]) -> str:
                """output a formated version string
                Keyword Arguments:
                    kwargs/output_format: output format to render ("Auto" or "PEP440" or "SemVer")
                Returns:
                    formated version string
                """
                return gitversionhelper.version.doFormatVersion(self, **kwargs)

        @classmethod
        def _getVersionStd(cls, **kwargs: Unpack[TKwargs]) -> gitversionhelper.version.MetaVersion.TVersionStd:
            """get selected version_std
            Keyword Arguments:
                kwargs/version_std (str): the given version_std (can be None)
            Returns:
                Kwargs given version_std or the default one.
            """
            VersionStd: str = cls.DefaultInputFormat
            if "version_std" in kwargs:
                if kwargs["version_std"] in cls.VersionStds:
                    VersionStd = kwargs["version_std"]
                else:
                    raise gitversionhelper.wrongArguments(f"invalid {'version_std'} requested")
            return cast(gitversionhelper.version.MetaVersion.TVersionStd, VersionStd)

        @classmethod
        def getCurrentVersion(cls, **kwargs: Unpack[TKwargs]) -> gitversionhelper.version.MetaVersion | str:
            """get the current version or bump depending of repository state.
            Keyword Arguments:
                kwargs/version_std (str): the given version_std (can be None)
                kwargs/same_branch (bool): force searching only in the same branch
                kwargs/formated_output (bool): output a formated version string
                kwargs/bump_type (str): the given bump_type (can be None)
                kwargs/bump_dev_strategy (str): the given bump_dev_strategy (can be None)
                kwargs/output_format (str): output format to render ("Auto" or "PEP440" or "SemVer")
            Returns:
                the last version
            """
            if gitversionhelper.repository.isDirty() is not False:
                raise gitversionhelper.repository.repositoryDirty("The repository is dirty and a current version can not be generated.")

            saved_kwargs = copy(kwargs)
            if "formated_output" in kwargs:
                del saved_kwargs["formated_output"]

            _v = cast(gitversionhelper.version.MetaVersion, cls.getLastVersion(**saved_kwargs))

            if not cls.__versionReseted:
                amount = gitversionhelper.tag.getDistanceFromTag(_v.raw, **saved_kwargs)
                _v = cast(gitversionhelper.version.MetaVersion, _v.bump(amount, **saved_kwargs))

            if ("formated_output" in kwargs) and (kwargs["formated_output"] is True):
                return _v.doFormatVersion(**kwargs)
            return _v

        @classmethod
        def getCurrentFormatedVersion(cls, **kwargs: Unpack[TKwargs]) -> str:
            """same as getCurrentVersion() with formated_output kwarg forced activated.
            Keyword Arguments:
                kwargs/version_std (str): the given version_std (can be None)
                kwargs/same_branch (bool): force searching only in the same branch
                kwargs/bump_type (str): the given bump_type (can be None)
                kwargs/bump_dev_strategy (str): the given bump_dev_strategy (can be None)
                kwargs/output_format (str): output format to render ("Auto" or "PEP440" or "SemVer")
            Returns:
                the last version
            """
            kwargs["formated_output"] = True
            return cast(str, cls.getCurrentVersion(**kwargs))

        @classmethod
        def _parseTag(  # pylint: disable=R1260,R0914,R0912,R0915
            cls, tag: str, **kwargs: Unpack[TKwargs]
        ) -> gitversionhelper.version.MetaVersion:
            """get version from tags.
            Arguments:
                tag: the tag to be parsed
            Keyword Arguments:
                kwargs/version_std (str): the given version_std (can be None)
            Returns:
                MetaVersion object
            """
            _m: Optional[re.Match[str]]
            VersionStd: gitversionhelper.version.MetaVersion.TVersionStd = cls._getVersionStd(**kwargs)
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
                if _m is None:
                    pass
                else:
                    major = int(_m.group("major"))
                    minor = int(_m.group("minor"))
                    patch = int(_m.group("patch"))

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
                if _m is None:
                    pass
                else:
                    res: str = _m.group("release")
                    if isinstance(res, str):

                        ver = res.split(".")
                        ver += ["0"] * (3 - len(ver))

                        ver_int: List[int] = [0, 0, 0]
                        ver_int[0] = int(ver[0])
                        ver_int[1] = int(ver[1])
                        ver_int[2] = int(ver[2])
                        major, minor, patch = tuple(ver_int)

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
        def getLastVersion(cls, **kwargs: Unpack[TKwargs]) -> gitversionhelper.version.MetaVersion | str:  # pylint: disable=R1260
            """get the last version from tags
            Keyword Arguments:
                kwargs/version_std (str): the given version_std (can be None)
                kwargs/same_branch (bool): force searching only in the same branch
                kwargs/formated_output (bool): output a formated version string
                kwargs/ignore_unknown_tags (bool): skip tags with not decoded versions (default to False)
            Returns:
                the last version in MetaVersion object or string
            """
            lastTag: str = cls.MetaVersion.raw
            cls.__versionReseted = False
            try:
                lastTag = cast(str, gitversionhelper.tag.getLastTag(**kwargs))
            except gitversionhelper.tag.tagNotFound:
                logging.warning("tag not found, reseting versionning")
                cls.__versionReseted = True

            _v: Optional[gitversionhelper.version.MetaVersion] = None
            try:
                _v = cls._parseTag(lastTag, **kwargs)
            except gitversionhelper.version.noValidVersion as _ex:
                if ("ignore_unknown_tags" in kwargs) and (kwargs["ignore_unknown_tags"] is True):
                    tags = gitversionhelper.tag.getTags(Sort="taggerdate", **kwargs)
                    _v = None
                    for _tag in tags:
                        try:
                            _v = cls._parseTag(_tag, **kwargs)
                            break
                        except gitversionhelper.version.noValidVersion:
                            continue
                if _v is None:
                    raise gitversionhelper.version.noValidVersion() from _ex

            if ("formated_output" in kwargs) and (kwargs["formated_output"] is True):
                return _v.doFormatVersion(**kwargs)
            return _v

        @classmethod
        def doFormatVersion(cls, inputversion: MetaVersion, **kwargs: Unpack[TKwargs]) -> str:
            """output a formated version string from a MetaVersion object
            Keyword Arguments:
                kwargs/output_format (str): output format to render ("Auto" or "PEP440" or "SemVer")
            Args:
                inputversion: version to be rendered
            Returns:
                formated version string
            """

            VersionStd = cls._getVersionStd(**kwargs)
            if VersionStd == "Auto":
                VersionStd = inputversion.version_std

            revpattern = ""
            revcount = ""
            post_count = inputversion.post_count
            pre_count = inputversion.pre_count
            patch = inputversion.patch

            OutputFormat = kwargs.get("output_format")

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
