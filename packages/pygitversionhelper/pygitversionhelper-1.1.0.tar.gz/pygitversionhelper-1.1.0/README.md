![](https://chacha.ddns.net/jenkins/buildStatus/icon?subject=status&status=active&color=seagreen)
![](https://chacha.ddns.net/jenkins/buildStatus/icon?subject=doc&status=MkDocs&color=blue)
![](https://chacha.ddns.net/jenkins/buildStatus/icon?subject=jenkins-unittest&job={{repository}}-{{branch}})
![](https://chacha.ddns.net/jenkins/buildStatus/icon?job={{repository}}-{{branch}}&build=0&config=coverage)
![](https://chacha.ddns.net/jenkins/buildStatus/icon?job={{repository}}-{{branch}}&build=0&config=maintainability)
![](https://chacha.ddns.net/jenkins/buildStatus/icon?job={{repository}}-{{branch}}&build=0&config=quality)
![](https://chacha.ddns.net/jenkins/buildStatus/icon?subject=licence&status=CC%20BY-NC-SA%204.0&color=teal)

![](docs-static/Library.jpg)

# pyGitVersionHelper

_A tiny library to help versioning management of git python projects_ 

Because a good developer is a lazy developer and version management in CI/CD can be very time consuming.

Checkout [Latest Documentation](https://chacha.ddns.net/mkdocs-web/chacha/pygitversionhelper/master/latest/).

## Features
    - list tags
    - get last tag 
    - get last version
    - get current version (bumped)
    - convert / switch from SemVer to PEP440 (both ways)
    - automatic version format detection (SemVer by default)
    - get commit message history

## Options
    - restrict to same branch
    - both SemVer and PEP440 support
    - custom output format
    - configurable default bump type: major, minor, patch or dev
    - configurable default bump strategy: post, pre-patch, pre-minor, pre-major
    - ignore non-version tag
    - force version format

## Process
    - full CI/CD developpment: Gitea / Jenkins + few python libs (pytlint, coverage, unittest, mkdocs)
    - documentation generated mkdocs and self-hosted
    - CI/CD on Linux, manually tested in Windows environnement