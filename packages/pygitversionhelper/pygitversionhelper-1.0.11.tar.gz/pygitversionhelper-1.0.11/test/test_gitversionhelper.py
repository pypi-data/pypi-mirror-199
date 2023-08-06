# pygitversionhelper (c) by chacha
#
# pygitversionhelper  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

import unittest

import tempfile
import os
import pathlib
import re
import copy
import time
import subprocess

from src import pygitversionhelper

HelperRegex = r"^(?P<MAJ>\d+)\.(?P<MIN>\d+)\.(?P<PATCH>\d+)([\.\-\+])?(?:.*)?"


class Test_gitversionhelper(unittest.TestCase):
    def setUp(self):
        self.TmpWorkingDir = tempfile.TemporaryDirectory()
        self.TmpWorkingDirPath = pathlib.Path(self.TmpWorkingDir.name)
        os.chdir(self.TmpWorkingDirPath)
        os.system("git init")
        os.system('git config --local user.name "john doe"')
        os.system('git config --local user.email "john@doe.org"')

    def _test_version_readback(self, tag: str, **kwargs):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")

        os.system("git add .")
        os.system('git commit -m  "first commit"')
        os.system(f"git tag {tag}")

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(**kwargs)

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self.assertIsInstance(_v.raw, str)
        self.assertEqual(_v.raw, tag)
        self.assertIsInstance(_v.major, int)
        self.assertIsInstance(_v.minor, int)
        self.assertIsInstance(_v.patch, int)
        self.assertIsInstance(_v.pre_count, int)
        self.assertIsInstance(_v.post_count, int)

        _m = re.match(HelperRegex, tag)
        self.assertEqual(int(_m.group("MAJ")), _v.major)
        self.assertEqual(int(_m.group("MIN")), _v.minor)
        self.assertEqual(int(_m.group("PATCH")), _v.patch)

        return _v

    def _test_version_format(
        self,
        _v: pygitversionhelper.gitversionhelper.version.MetaVersion,
        tag: str,
        **kwargs,
    ):
        _f = _v.doFormatVersion(**kwargs)
        self.assertRegex(_f, HelperRegex)
        self.assertEqual(_f, tag)

    def _test_version_readback_simple(self, tag: str, **kwargs):
        _v = self._test_version_readback(tag, **kwargs)
        self._test_version_format(_v, tag, **kwargs)

    def test_nominal__version__formated_output(self):
        _v = pygitversionhelper.gitversionhelper.version.MetaVersion("PEP440", 1, 0, 0, 0, 0, "1.0.0")
        self.assertEqual("1.0.1", _v.bump(formated_output=True))
        self.assertEqual("2.0.0", _v.bump(formated_output=True, bump_type="major"))

    def test_nominal__version__auto_1(self):
        self._test_version_readback_simple("0.0.1")

    def test_nominal__version__auto_2(self):
        self._test_version_readback_simple("0.0.2")

    def test_nominal__version__auto_3(self):
        self._test_version_readback_simple("0.1.0")

    def test_nominal__version__auto_4(self):
        self._test_version_readback_simple("0.1.1")

    def test_nominal__version__auto_5(self):
        self._test_version_readback_simple("1.0.0")

    def test_nominal__version__auto_6(self):
        self._test_version_readback_simple("1.1.0")

    def test_nominal__version__auto_7(self):
        self._test_version_readback_simple("1.2.0")

    def test_nominal__version__auto_8(self):
        self._test_version_readback_simple("1.1.1")

    def test_nominal__version__auto_9(self):
        self._test_version_readback_simple("1.2.1")

    def test_nominal__version__auto_PEP440_post(self):
        self._test_version_readback_simple("1.2.1.post1")

    def test_nominal__version__auto_PEP440_pre(self):
        self._test_version_readback_simple("1.2.1.pre1")

    def test_nominal__version__auto_PEP440_post_2(self):
        self._test_version_readback_simple("1.2.1.post10")

    def test_nominal__version__auto_PEP440_pre_2(self):
        self._test_version_readback_simple("1.2.1.pre10")

    def test_nominal__version__auto_SemVer_post(self):
        self._test_version_readback_simple("1.2.1+post.1")

    def test_nominal__version__auto_SemVer_pre(self):
        self._test_version_readback_simple("1.2.1-pre.1")

    def test_nominal__version__auto_SemVer_post_2(self):
        self._test_version_readback_simple("1.2.1+post.10")

    def test_nominal__version__auto_Semver_pre_2(self):
        self._test_version_readback_simple("1.2.1-pre.10")

    def test_nominal__version__PEP440_1(self):
        self._test_version_readback_simple("0.0.1", version_std="PEP440")

    def test_nominal__version__PEP440_2(self):
        self._test_version_readback_simple("0.0.2", version_std="PEP440")

    def test_nominal__version__PEP440_3(self):
        self._test_version_readback_simple("0.1.0", version_std="PEP440")

    def test_nominal__version__PEP440_4(self):
        self._test_version_readback_simple("0.1.1", version_std="PEP440")

    def test_nominal__version__PEP440_5(self):
        self._test_version_readback_simple("1.0.0", version_std="PEP440")

    def test_nominal__version__PEP440_6(self):
        self._test_version_readback_simple("1.1.0", version_std="PEP440")

    def test_nominal__version__PEP440_7(self):
        self._test_version_readback_simple("1.2.0", version_std="PEP440")

    def test_nominal__version__PEP440_8(self):
        self._test_version_readback_simple("1.1.1", version_std="PEP440")

    def test_nominal__version__PEP440_9(self):
        self._test_version_readback_simple("1.2.1", version_std="PEP440")

    def test_nominal__version__PEP440_post(self):
        self._test_version_readback_simple("1.2.1.post1", version_std="PEP440")

    def test_nominal__version__PEP440_pre(self):
        self._test_version_readback_simple("1.2.1.pre1", version_std="PEP440")

    def test_nominal__version__PEP440_post_2(self):
        self._test_version_readback_simple("1.2.1.post10", version_std="PEP440")

    def test_nominal__version__PEP440_pre_2(self):
        self._test_version_readback_simple("1.2.1.pre10", version_std="PEP440")

    def test_nominal__version__SemVer_1(self):
        self._test_version_readback_simple("0.0.1", version_std="SemVer")

    def test_nominal__version__SemVer_2(self):
        self._test_version_readback_simple("0.0.2", version_std="SemVer")

    def test_nominal__version__SemVer_3(self):
        self._test_version_readback_simple("0.1.0", version_std="SemVer")

    def test_nominal__version__SemVer_4(self):
        self._test_version_readback_simple("0.1.1", version_std="SemVer")

    def test_nominal__version__SemVer_5(self):
        self._test_version_readback_simple("1.0.0", version_std="SemVer")

    def test_nominal__version__SemVer_6(self):
        self._test_version_readback_simple("1.1.0", version_std="SemVer")

    def test_nominal__version__SemVer_7(self):
        self._test_version_readback_simple("1.2.0", version_std="SemVer")

    def test_nominal__version__SemVer_8(self):
        self._test_version_readback_simple("1.1.1", version_std="SemVer")

    def test_nominal__version__SemVer_9(self):
        self._test_version_readback_simple("1.2.1", version_std="SemVer")

    def test_nominal__version__SemVer_post(self):
        self._test_version_readback_simple("1.2.1+post.1", version_std="SemVer")

    def test_nominal__version__SemVer_pre(self):
        self._test_version_readback_simple("1.2.1-pre.1", version_std="SemVer")

    def test_nominal__version__SemVer_post_2(self):
        self._test_version_readback_simple("1.2.1+post.10", version_std="SemVer")

    def test_nominal__version__SemVer_pre_2(self):
        self._test_version_readback_simple("1.2.1-pre.10", version_std="SemVer")

    def test_nominal__version__post_PEP440_to_SemVer(self):
        _v = self._test_version_readback("1.2.1.post10", version_std="PEP440")
        self._test_version_format(_v, "1.2.1+post.10", version_std="SemVer")

    def test_nominal__version__post_SemVer_to_PEP440(self):
        _v = self._test_version_readback("1.2.1+post.10", version_std="SemVer")
        self._test_version_format(_v, "1.2.1.post10", version_std="PEP440")

    def test_nominal__version__pre_PEP440_to_SemVer(self):
        _v = self._test_version_readback("1.2.1.pre10", version_std="PEP440")
        self._test_version_format(_v, "1.2.1-pre.10", version_std="SemVer")

    def test_nominal__version__pre_SemVer_to_PEP440(self):
        _v = self._test_version_readback("1.2.1-pre.10", version_std="SemVer")
        self._test_version_format(_v, "1.2.1.pre10", version_std="PEP440")

    def test_nominal__version__post_SemVer_nonum(self):
        _v = self._test_version_readback("1.2.1+post", version_std="SemVer")
        self._test_version_format(_v, "1.2.1+post.1", version_std="SemVer")

    def test_nominal__version__post_SemVer_nonum_random(self):
        _v = self._test_version_readback("1.2.1+toto", version_std="SemVer")
        self._test_version_format(_v, "1.2.1+post.1", version_std="SemVer")

    def test_nominal__version__pre_SemVer_nonum(self):
        _v = self._test_version_readback("1.2.1-pre", version_std="SemVer")
        self._test_version_format(_v, "1.2.1-pre.1", version_std="SemVer")

    def test_nominal__version__pre_SemVer_nonum_random(self):
        _v = self._test_version_readback("1.2.1-toto", version_std="SemVer")
        self._test_version_format(_v, "1.2.1-pre.1", version_std="SemVer")

    def test_nominal__version___pump_SemVer(self):
        _v = self._test_version_readback("1.0.0", version_std="SemVer")

        _v = _v.bump()
        self.assertIsInstance(_v.raw, str)
        self.assertIsInstance(_v.major, int)
        self.assertIsInstance(_v.minor, int)
        self.assertIsInstance(_v.patch, int)
        self.assertIsInstance(_v.pre_count, int)
        self.assertIsInstance(_v.post_count, int)
        self.assertEqual(_v.raw, "1.0.1")
        self.assertEqual(_v.major, 1)
        self.assertEqual(_v.minor, 0)
        self.assertEqual(_v.patch, 1)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "1.0.1")

        _v = _v.bump(bump_type="patch")
        self.assertEqual(_v.raw, "1.0.2")
        self.assertEqual(_v.major, 1)
        self.assertEqual(_v.minor, 0)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "1.0.2")

        _v = _v.bump(bump_type="minor")
        self.assertEqual(_v.raw, "1.1.2")
        self.assertEqual(_v.major, 1)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "1.1.2")

        _v = _v.bump(bump_type="major")
        self.assertEqual(_v.raw, "2.1.2")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.2")

        _v = _v.bump(bump_type="dev")
        self.assertEqual(_v.raw, "2.1.2+post.1")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 1)
        self.assertEqual(_v.doFormatVersion(), "2.1.2+post.1")

        _v = _v.bump(bump_type="dev")
        self.assertEqual(_v.raw, "2.1.2+post.2")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 2)
        self.assertEqual(_v.doFormatVersion(), "2.1.2+post.2")
        self.assertEqual(_v.doFormatVersion(version_std="SemVer"), "2.1.2+post.2")
        self.assertEqual(_v.doFormatVersion(version_std="PEP440"), "2.1.2.post2")

        _v = _v.bump(bump_type="patch")
        self.assertEqual(_v.raw, "2.1.3")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 3)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.3")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="pre-patch")
        self.assertEqual(_v.raw, "2.1.4-pre.1")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 4)
        self.assertEqual(_v.pre_count, 1)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.4-pre.1")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="pre-patch")
        self.assertEqual(_v.raw, "2.1.4-pre.2")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 4)
        self.assertEqual(_v.pre_count, 2)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.4-pre.2")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="post")
        self.assertEqual(_v.raw, "2.1.4-pre.3")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 4)
        self.assertEqual(_v.pre_count, 3)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.4-pre.3")

        _v = _v.bump(bump_type="patch")
        self.assertEqual(_v.raw, "2.1.5")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 5)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.5")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="post")
        self.assertEqual(_v.raw, "2.1.5+post.1")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 5)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 1)
        self.assertEqual(_v.doFormatVersion(), "2.1.5+post.1")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="pre-patch")
        self.assertEqual(_v.raw, "2.1.5+post.2")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 5)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 2)
        self.assertEqual(_v.doFormatVersion(), "2.1.5+post.2")

    def test_nominal__version___pump_PEP440(self):
        _v = self._test_version_readback("1.0.0", version_std="PEP440")

        _v = _v.bump()
        self.assertIsInstance(_v.raw, str)
        self.assertIsInstance(_v.major, int)
        self.assertIsInstance(_v.minor, int)
        self.assertIsInstance(_v.patch, int)
        self.assertIsInstance(_v.pre_count, int)
        self.assertIsInstance(_v.post_count, int)
        self.assertEqual(_v.raw, "1.0.1")
        self.assertEqual(_v.major, 1)
        self.assertEqual(_v.minor, 0)
        self.assertEqual(_v.patch, 1)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "1.0.1")

        _v = _v.bump(bump_type="patch")
        self.assertEqual(_v.raw, "1.0.2")
        self.assertEqual(_v.major, 1)
        self.assertEqual(_v.minor, 0)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "1.0.2")

        _v = _v.bump(bump_type="minor")
        self.assertEqual(_v.raw, "1.1.2")
        self.assertEqual(_v.major, 1)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "1.1.2")

        _v = _v.bump(bump_type="major")
        self.assertEqual(_v.raw, "2.1.2")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.2")

        _v = _v.bump(bump_type="dev")
        self.assertEqual(_v.raw, "2.1.2.post1")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 1)
        self.assertEqual(_v.doFormatVersion(), "2.1.2.post1")

        _v = _v.bump(bump_type="dev")
        self.assertEqual(_v.raw, "2.1.2.post2")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 2)
        self.assertEqual(_v.doFormatVersion(), "2.1.2.post2")

        _v = _v.bump(bump_type="patch")
        self.assertEqual(_v.raw, "2.1.3")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 3)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.3")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="pre-patch")
        self.assertEqual(_v.raw, "2.1.4.pre1")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 4)
        self.assertEqual(_v.pre_count, 1)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.4.pre1")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="pre-patch")
        self.assertEqual(_v.raw, "2.1.4.pre2")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 4)
        self.assertEqual(_v.pre_count, 2)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.4.pre2")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="post")
        self.assertEqual(_v.raw, "2.1.4.pre3")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 4)
        self.assertEqual(_v.pre_count, 3)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.4.pre3")

        _v = _v.bump(bump_type="patch")
        self.assertEqual(_v.raw, "2.1.5")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 5)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)
        self.assertEqual(_v.doFormatVersion(), "2.1.5")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="post")
        self.assertEqual(_v.raw, "2.1.5.post1")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 5)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 1)
        self.assertEqual(_v.doFormatVersion(), "2.1.5.post1")

        _v = _v.bump(bump_type="dev", bump_dev_strategy="pre-patch")
        self.assertEqual(_v.raw, "2.1.5.post2")
        self.assertEqual(_v.major, 2)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 5)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 2)
        self.assertEqual(_v.doFormatVersion(), "2.1.5.post2")

    def test_nominal__version___SemVer_zeroRev(self):
        _v = self._test_version_readback("0.0.0", version_std="SemVer")
        self._test_version_format(_v, "0.0.0", version_std="SemVer")

    def test_nominal__version___PEP440_zeroRev(self):
        _v = self._test_version_readback("0.0.0", version_std="PEP440")
        self._test_version_format(_v, "0.0.0", version_std="PEP440")

    def test_nominal__version___PEP440_noRev_noTag(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")

        os.system("git add .")
        os.system('git commit -m  "first commit"')

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440")

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.1.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 0)

    def test_nominal__version___SemVer_noRev_noTag(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")

        os.system("git add .")
        os.system('git commit -m  "first commit"')

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="SemVer")

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.0", version_std="SemVer")
        self.assertEqual(_v.raw, "0.1.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 0)

    def test_nominal__version___AUTO_noRev_noTag(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")

        os.system("git add .")
        os.system('git commit -m  "first commit"')

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion()

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.0")
        self.assertEqual(_v.raw, "0.1.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 0)

    def test_nominal__version___getCurrentFormatedVersion(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "first commit"')
        os.system(f"git tag 0.2.0")

        self.assertEqual(pygitversionhelper.gitversionhelper.version.getCurrentFormatedVersion(), "0.2.0")

    def test_nominal__version___AUTO_bump_commits(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "first commit"')
        os.system(f"git tag 0.2.0")

        _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion()

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.2.0")
        self.assertEqual(_v.raw, "0.2.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 2)
        self.assertEqual(_v.patch, 0)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue22")
        os.system("git add .")
        os.system('git commit -m  "2nd commit"')

        _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion()

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.2.1")
        self.assertEqual(_v.raw, "0.2.1")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 2)
        self.assertEqual(_v.patch, 1)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue223")
        os.system("git add .")
        os.system('git commit -m  "3rd commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue224")
        os.system("git add .")
        os.system('git commit -m  "4th commit"')

        _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion()

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.2.3")
        self.assertEqual(_v.raw, "0.2.3")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 2)
        self.assertEqual(_v.patch, 3)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue225")
        os.system("git add .")
        os.system('git commit -m  "5th commit"')

        _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion(bump_type="dev")

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self.assertIsInstance(_v.raw, str)
        self._test_version_format(_v, "0.2.0+post.4")
        self.assertEqual(_v.raw, "0.2.0+post.4")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 2)
        self.assertEqual(_v.patch, 0)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 4)

        _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion(bump_type="dev", bump_dev_strategy="pre-patch")

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.2.1-pre.4")
        self.assertEqual(_v.raw, "0.2.1-pre.4")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 2)
        self.assertEqual(_v.patch, 1)
        self.assertEqual(_v.pre_count, 4)
        self.assertEqual(_v.post_count, 0)

        _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion(bump_type="dev", bump_dev_strategy="pre-minor")

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.3.0-pre.4")
        self.assertEqual(_v.raw, "0.3.0-pre.4")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 3)
        self.assertEqual(_v.patch, 0)
        self.assertEqual(_v.pre_count, 4)
        self.assertEqual(_v.post_count, 0)

        _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion(bump_type="dev", bump_dev_strategy="pre-major")

        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "1.0.0-pre.4")
        self.assertEqual(_v.raw, "1.0.0-pre.4")
        self.assertEqual(_v.major, 1)
        self.assertEqual(_v.minor, 0)
        self.assertEqual(_v.patch, 0)
        self.assertEqual(_v.pre_count, 4)
        self.assertEqual(_v.post_count, 0)

    def test_nominal__version___custom_format(self):
        _v = self._test_version_readback("0.1.1", version_std="PEP440")

        self.assertEqual(
            "V_0_1_1____",
            _v.doFormatVersion(output_format="V_{major}_{minor}_{patch}____{revcount}"),
        )
        self.assertEqual("V_0_1", _v.doFormatVersion(output_format="V_{major}_{minor}"))

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue225")
        os.system("git add .")
        os.system('git commit -m  "5th commit"')

        self.assertEqual(
            "V_1_0",
            pygitversionhelper.gitversionhelper.version.getCurrentVersion(bump_type="dev", bump_dev_strategy="pre-major").doFormatVersion(
                output_format="V_{major}_{minor}"
            ),
        )
        self.assertEqual(
            "V_1_0",
            pygitversionhelper.gitversionhelper.version.getCurrentVersion(
                bump_type="dev",
                bump_dev_strategy="pre-major",
                output_format="V_{major}_{minor}",
                formated_output=True,
            ),
        )
        self.assertEqual(
            "0.1.1",
            pygitversionhelper.gitversionhelper.version.getLastVersion(
                formated_output=True,
            ),
        )

    def test_nominal__git__emptyrepo(self):
        _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion()
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.0")
        self.assertEqual(_v.raw, "0.1.0")

        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 0)
        self.assertEqual(_v.pre_count, 0)
        self.assertEqual(_v.post_count, 0)

    def test_defect__git__dirty(self):
        _v = self._test_version_readback("0.1.1", version_std="PEP440")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue225")

        with self.assertRaises(pygitversionhelper.gitversionhelper.repository.repositoryDirty):
            pygitversionhelper.gitversionhelper.version.getCurrentVersion()

    def test_defect__version_post_and_pre_output(self):
        _v = pygitversionhelper.gitversionhelper.version.MetaVersion("PEP440", 0, 0, 1, 1, 1, "0.0.1.pre1.post1")
        with self.assertRaises(pygitversionhelper.gitversionhelper.version.PreAndPostVersionUnsupported):
            _v.doFormatVersion()

        _v = pygitversionhelper.gitversionhelper.version.MetaVersion("SemVer", 0, 0, 1, 1, 1, "0.0.1-pre.1+post.1")
        with self.assertRaises(pygitversionhelper.gitversionhelper.version.PreAndPostVersionUnsupported):
            _v.doFormatVersion()

    def test_defect__version_post_and_pre_parse(self):
        with self.assertRaises(pygitversionhelper.gitversionhelper.version.PreAndPostVersionUnsupported):
            pygitversionhelper.gitversionhelper.version._parseTag("0.0.1.pre1.post1")

    def test_defect__git__wrongargument_sortargs(self):
        with self.assertRaises(pygitversionhelper.gitversionhelper.wrongArguments):
            pygitversionhelper.gitversionhelper.tag.getTags(sort="toto")

    def test_defect__git__notagfound(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "first commit"')
        with self.assertRaises(pygitversionhelper.gitversionhelper.tag.tagNotFound):
            pygitversionhelper.gitversionhelper.tag.getLastTag()

    """ This test is impossible to do because current implementation can only return one tag
    def test_defect__git_multipletagsfound(self):
        with  open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system("git commit -m  \"first commit\"")
        os.system(f"git tag 0.1.0")
        os.system(f"git tag 0.2.0")
        with self.assertRaises(pygitversionhelper.gitversionhelper.tag.moreThanOneTag) :
            pygitversionhelper.gitversionhelper.tag.getLastTag(same_branch=True)
    """

    def test_defect__wrongargument_bump_type(self):
        _v = self._test_version_readback("0.1.1", version_std="PEP440")
        with self.assertRaises(pygitversionhelper.gitversionhelper.wrongArguments):
            pygitversionhelper.gitversionhelper.version.getCurrentVersion(bump_type="toto")

    def test_defect__wrongargument_bump_dev_strategy(self):
        _v = self._test_version_readback("0.1.1", version_std="PEP440")
        with self.assertRaises(pygitversionhelper.gitversionhelper.wrongArguments):
            pygitversionhelper.gitversionhelper.version.getCurrentVersion(bump_dev_strategy="toto")

    def test_nominal__tag__getDistanceFromTag(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.2.0")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue1")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.3.0")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue3")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        self.assertEqual(2, pygitversionhelper.gitversionhelper.tag.getDistanceFromTag())
        self.assertEqual(4, pygitversionhelper.gitversionhelper.tag.getDistanceFromTag("0.2.0"))

    def test_nominal__tag__getTags(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.2.0")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue1")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.3.0")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue3")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue5")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.3.1")

        self.assertEqual(
            set(["0.3.0", "0.2.0", "0.3.1"]),
            set(pygitversionhelper.gitversionhelper.tag.getTags()),
        )

    def test_nominal__tag__getTags_two_branch(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.2.0")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue1")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.3.0")

        os.system("git checkout -b dev")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue3")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue5")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.3.1")

        self.assertEqual(
            set(["0.3.0", "0.2.0", "0.3.1"]),
            set(pygitversionhelper.gitversionhelper.tag.getTags()),
        )

    def test_nominal__tag__getTags_two_branch_samebranch(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.2.0")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue1")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.3.0")

        os.system("git checkout -b dev")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue3")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue5")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.3.1")

        self.assertEqual(
            set(["0.3.0", "0.2.0", "0.3.1"]),
            set(pygitversionhelper.gitversionhelper.tag.getTags(same_branch=True)),
        )

        os.system("git switch master")

        self.assertEqual(
            set(["0.3.0", "0.2.0"]),
            set(pygitversionhelper.gitversionhelper.tag.getTags(same_branch=True)),
        )

        os.system("git switch dev")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.3.2")

        self.assertEqual(
            set(["0.3.0", "0.2.0", "0.3.1", "0.3.2"]),
            set(pygitversionhelper.gitversionhelper.tag.getTags(same_branch=True)),
        )
        self.assertEqual(
            set(["0.3.0", "0.2.0", "0.3.1", "0.3.2"]),
            set(pygitversionhelper.gitversionhelper.tag.getTags()),
        )

        os.system("git switch master")

        self.assertEqual(
            set(["0.3.0", "0.2.0"]),
            set(pygitversionhelper.gitversionhelper.tag.getTags(same_branch=True)),
        )
        self.assertEqual(
            set(["0.3.0", "0.2.0", "0.3.1", "0.3.2"]),
            set(pygitversionhelper.gitversionhelper.tag.getTags()),
        )

    def test_nominal__tag__getLastTag_two_branches(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "first commit"')

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue1")
        os.system("git add .")
        os.system('git commit -m  "2nd commit"')
        os.system(f"git tag 0.1.0")

        os.system("git checkout -b dev")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")
        os.system('git commit -m  "3rd commit"')
        os.system(f"git tag 0.2.0")

        """
        print("===")
        os.system(f"git status")
        print("===")
        os.system(f"git describe --tags --abbrev=0")
        print("===")
        os.system(f"git rev-list --all")
        print("===")
        os.system(f"git rev-list --tags")
        print("===")
        os.system(f"git log --oneline --decorate=short")
        print("===")
        os.system(f"git describe --tags")
        print("===")
        """

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440")
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.2.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.2.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 2)
        self.assertEqual(_v.patch, 0)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue3")
        os.system("git add .")
        os.system('git commit -m  "3rd commit"')
        os.system(f"git tag 0.3.0")

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440")
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.3.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.3.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 3)
        self.assertEqual(_v.patch, 0)

        os.system("git switch master")

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440")
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.3.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.3.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 3)
        self.assertEqual(_v.patch, 0)

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440", same_branch=True)
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.1.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 0)

        os.system('git merge --no-ff dev -m "merge dev into master"')

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440", same_branch=True)
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.1.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 0)

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440")
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.3.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.3.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 3)
        self.assertEqual(_v.patch, 0)

        os.system(f"git tag 0.4.0")

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440", same_branch=True)
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.4.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.4.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 4)
        self.assertEqual(_v.patch, 0)

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(version_std="PEP440")
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.4.0", version_std="PEP440")
        self.assertEqual(_v.raw, "0.4.0")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 4)
        self.assertEqual(_v.patch, 0)

    def test_defect__tag__invalidtag(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue1")
        os.system("git add .")
        os.system('git commit -m  "2nd commit"')
        os.system(f"git tag INVALIDTAG")

        with self.assertRaises(pygitversionhelper.gitversionhelper.version.noValidVersion):
            _v = pygitversionhelper.gitversionhelper.version.getLastVersion()

        with self.assertRaises(pygitversionhelper.gitversionhelper.version.noValidVersion):
            _v = pygitversionhelper.gitversionhelper.version.getLastVersion(ignore_unknown_tags=True)

    def test_defect__tag__invalidtag_inbetween(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue1")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.0.1")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag INVALIDTAG")

        with self.assertRaises(pygitversionhelper.gitversionhelper.version.noValidVersion):
            _v = pygitversionhelper.gitversionhelper.version.getLastVersion()

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(ignore_unknown_tags=True)
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.0.1", version_std="PEP440")
        self.assertEqual(_v.raw, "0.0.1")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 0)
        self.assertEqual(_v.patch, 1)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue3")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag INVALIDTAG2")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag INVALIDTA3")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag INVALIDTA4")

        with self.assertRaises(pygitversionhelper.gitversionhelper.version.noValidVersion):
            _v = pygitversionhelper.gitversionhelper.version.getLastVersion()

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(ignore_unknown_tags=True)
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.0.1", version_std="PEP440")
        self.assertEqual(_v.raw, "0.0.1")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 0)
        self.assertEqual(_v.patch, 1)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue5")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.1.2")

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion()
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.2", version_std="PEP440")
        self.assertEqual(_v.raw, "0.1.2")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(ignore_unknown_tags=True)
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.2", version_std="PEP440")
        self.assertEqual(_v.raw, "0.1.2")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue6")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag INVALIDTA5")

        with self.assertRaises(pygitversionhelper.gitversionhelper.version.noValidVersion):
            _v = pygitversionhelper.gitversionhelper.version.getLastVersion()

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(ignore_unknown_tags=True)
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.2", version_std="PEP440")
        self.assertEqual(_v.raw, "0.1.2")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 2)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue7")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        os.system(f"git tag 0.1.3")

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion()
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.3", version_std="PEP440")
        self.assertEqual(_v.raw, "0.1.3")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 3)

        _v = pygitversionhelper.gitversionhelper.version.getLastVersion(ignore_unknown_tags=True)
        self.assertIsInstance(_v, pygitversionhelper.gitversionhelper.version.MetaVersion)
        self._test_version_format(_v, "0.1.3", version_std="PEP440")
        self.assertEqual(_v.raw, "0.1.3")
        self.assertEqual(_v.major, 0)
        self.assertEqual(_v.minor, 1)
        self.assertEqual(_v.patch, 3)

    def test_nominal__commit_getLast(self):
        # sleeps are needed because commit date have a 1-sec accuracy :-/
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        time.sleep(1)

        initial_commit = pygitversionhelper.gitversionhelper.commit.getLast()

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        time.sleep(1)

        second_commit = pygitversionhelper.gitversionhelper.commit.getLast()

        self.assertNotEqual(initial_commit, second_commit)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue3")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        time.sleep(1)

        third_commit = pygitversionhelper.gitversionhelper.commit.getLast()

        self.assertNotEqual(initial_commit, third_commit)
        self.assertNotEqual(second_commit, third_commit)

        os.system("git checkout -b dev")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        time.sleep(1)

        fourth_commit = pygitversionhelper.gitversionhelper.commit.getLast()

        self.assertNotEqual(initial_commit, fourth_commit)
        self.assertNotEqual(second_commit, fourth_commit)
        self.assertNotEqual(third_commit, fourth_commit)

        os.system("git switch master")

        fourth2_commit = pygitversionhelper.gitversionhelper.commit.getLast()
        self.assertEqual(fourth2_commit, fourth_commit)

        fourth3_commit = pygitversionhelper.gitversionhelper.commit.getLast(same_branch=True)

        self.assertNotEqual(fourth3_commit, fourth_commit)
        self.assertEqual(fourth3_commit, third_commit)

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue5")
        os.system("git add .")
        os.system('git commit -m  "commit"')
        time.sleep(1)

        fifth_commit = pygitversionhelper.gitversionhelper.commit.getLast()
        self.assertNotEqual(fifth_commit, fourth3_commit)

        os.system("git switch dev")

        fifth2_commit = pygitversionhelper.gitversionhelper.commit.getLast()
        self.assertEqual(fifth2_commit, fifth_commit)

        fifth2_commit = pygitversionhelper.gitversionhelper.commit.getLast(same_branch=True)
        self.assertEqual(fifth2_commit, fourth_commit)

    def test_defect__commit_notfound(self):

        with self.assertRaises(pygitversionhelper.gitversionhelper.commit.commitNotFound):
            pygitversionhelper.gitversionhelper.commit.getLast()

        with self.assertRaises(pygitversionhelper.gitversionhelper.commit.commitNotFound):
            pygitversionhelper.gitversionhelper.commit.getLast(same_branch=True)

    def test_defect__commit_getMessage_notfound(self):
        with self.assertRaises(pygitversionhelper.gitversionhelper.commit.commitNotFound):
            pygitversionhelper.gitversionhelper.commit.getMessage("")

    def test_nominal__commit_getFromTag(self):
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        initial_commit = pygitversionhelper.gitversionhelper.commit.getLast()

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")
        os.system('git commit -m  "commit2"')
        os.system(f"git tag TAG")

        second_commit = pygitversionhelper.gitversionhelper.commit.getLast()
        self.assertNotEqual(second_commit, initial_commit)
        second_commit2 = pygitversionhelper.gitversionhelper.commit.getFromTag("TAG")
        self.assertEqual(second_commit, second_commit2)
        self.assertNotEqual(second_commit2, initial_commit)

    def test_defect__commit_notfound2(self):

        with self.assertRaises(pygitversionhelper.gitversionhelper.commit.commitNotFound):
            pygitversionhelper.gitversionhelper.commit.getFromTag("TAG")

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system('git commit -m  "commit"')

        with self.assertRaises(pygitversionhelper.gitversionhelper.commit.commitNotFound):
            pygitversionhelper.gitversionhelper.commit.getFromTag("TAG")

        os.system(f"git tag OTHER_TAG")

        with self.assertRaises(pygitversionhelper.gitversionhelper.commit.commitNotFound):
            pygitversionhelper.gitversionhelper.commit.getFromTag("TAG")

    def test_nominal__commit_getMessage(self):
        commit_message = "AAAABBB CCCCDDDD".replace("\r\n", "\n").replace("\n", "\r\n")
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")
        os.system(f'git commit -m  "{commit_message}"')
        commit = pygitversionhelper.gitversionhelper.commit.getLast()
        message = pygitversionhelper.gitversionhelper.commit.getMessage(commit)
        self.assertEqual(message, commit_message)

    def test_nominal__commit_getMessage2(self):
        commit_message = """AAAABBB
        CCCCDDDD
        -f dfsds dfsdfs  $""".replace(
            "\r\n", "\n"
        ).replace(
            "\n", "\r\n"
        )

        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")

        cmd = "git commit -m".split()
        cmd.append(commit_message)
        subprocess.run(cmd, text=True, check=True)

        commit = pygitversionhelper.gitversionhelper.commit.getLast()
        message = pygitversionhelper.gitversionhelper.commit.getMessage(commit)

        self.assertEqual(message, commit_message)

    def test_nominal__commit_getMessagesSinceLastTag(self):
        commit_message1 = "1.1 update this" + os.linesep + "1.1 fix that" + os.linesep + "1.1 test"
        commit_message1 = commit_message1.replace("\r\n", "\n").replace("\n", "\r\n")
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue")
        os.system("git add .")

        cmd = "git commit -m".split()
        cmd.append(commit_message1)
        subprocess.run(cmd, text=True, check=True)
        os.system(f"git tag 0.1.1")

        commit_message2 = "2.1 update this" + os.linesep + "2.1 fix that" + os.linesep + "2.1 test"
        commit_message2 = commit_message2.replace("\r\n", "\n").replace("\n", "\r\n")
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue2")
        os.system("git add .")

        cmd = "git commit -m".split()
        cmd.append(commit_message2)
        subprocess.run(cmd, text=True, check=True)

        commit_message3 = "3.1 update this" + os.linesep + "3.1 fix that" + os.linesep + "3.1 test"
        commit_message3 = commit_message3.replace("\r\n", "\n").replace("\n", "\r\n")
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue3")
        os.system("git add .")

        cmd = "git commit -m".split()
        cmd.append(commit_message3)
        subprocess.run(cmd, text=True, check=True)

        commit_message4 = "4.1 update this" + os.linesep + "4.1 fix that" + os.linesep + "4.1 test"
        commit_message4 = commit_message4.replace("\r\n", "\n").replace("\n", "\r\n")
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue4")
        os.system("git add .")

        cmd = "git commit -m".split()
        cmd.append(commit_message4)
        subprocess.run(cmd, text=True, check=True)

        res = pygitversionhelper.gitversionhelper.commit.getMessagesSinceTag("0.1.1")
        self.assertEqual([commit_message4, commit_message3, commit_message2], res)

        res = pygitversionhelper.gitversionhelper.commit.getMessagesSinceTag("0.1.1", merged_output=True)
        self.assertEqual(os.linesep.join([commit_message4, commit_message3, commit_message2]), res)

        cmd = "git checkout -b dev".split()
        subprocess.run(cmd, text=True, check=True)

        commit_message5 = "5.1 update this" + os.linesep + "5.1 fix that" + os.linesep + "5.1 test"
        commit_message5 = commit_message5.replace("\r\n", "\n").replace("\n", "\r\n")
        with open("demofile.txt", "w+t") as tmpFile:
            tmpFile.write("testvalue5")
        os.system("git add .")

        cmd = "git commit -m".split()
        cmd.append(commit_message5)
        subprocess.run(cmd, text=True, check=True)

        cmd = "git switch master".split()
        subprocess.run(cmd, text=True, check=True)

        res = pygitversionhelper.gitversionhelper.commit.getMessagesSinceTag("0.1.1", merged_output=True, same_branch=True)
        self.assertEqual(os.linesep.join([commit_message4, commit_message3, commit_message2]), res)

        res = pygitversionhelper.gitversionhelper.commit.getMessagesSinceTag("0.1.1", merged_output=True)
        self.assertEqual(os.linesep.join([commit_message5, commit_message4, commit_message3, commit_message2]), res)

    def tearDown(self):
        os.chdir("/")


class Test_gitversionhelperNoRepo(unittest.TestCase):
    def setUp(self):
        self.TmpWorkingDir = tempfile.TemporaryDirectory()
        self.TmpWorkingDirPath = pathlib.Path(self.TmpWorkingDir.name)
        os.chdir(self.TmpWorkingDirPath)

    def test_defect__norepo(self):
        with self.assertRaises(pygitversionhelper.gitversionhelper.repository.notAGitRepository):
            _v = pygitversionhelper.gitversionhelper.version.getCurrentVersion()

    def tearDown(self):
        os.chdir("/")
