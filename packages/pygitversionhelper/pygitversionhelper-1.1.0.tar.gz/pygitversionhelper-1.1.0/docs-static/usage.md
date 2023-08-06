# Usage

## Installation

From pypi repository (prefered):
```console
/> python -m pip install pygitversionhelper
```   
 
From downloaded .whl file:
```console
/> python -m pip install pygitversionhelper-<VERSION>-py3-none-any.whl
```  

From master git repository:
```console
/> python -m pip install git+https://chacha.ddns.net/gitea/chacha/pygitversionhelper.git@master
```



## Import in your project

Add this line on the top of your python script:
```py
from pygitversionhelper import gitversionhelper
```
[optionnal] If you need to catch exception from this module:
```py
from pygitversionhelper import gitversionhelperException
```    
## Basic API

All the API commands are static so it is not needed to create instantiate any object.

They are all executed in the current active directory.

One easy way to change directory:
```py
import os
os.chdir("<YOUR DIRECTORY>")
```
### sub-lib: repository 

To check if a repository is dirty:
```py
if gitversionhelper.repository.isDirty():
    print("repository is dirty")
```
### sub-lib: tag 

List all tags [default to taggerdate order]:
```py
for tag in gitversionhelper.tag.getTags():
    print(f"found tag: {tag}")
```    
List all tags [using git refname order]:
```py
for tag in gitversionhelper.tag.getTags("v:refname"):
    print(f"found tag: {tag}")
```
Get the last tag:
```py
print(f"most recent repository tag: {gitversionhelper.tag.getLastTag()}")
```
Get the last tag [only on same branch]:
```py
print(f"most recent repository tag: {gitversionhelper.tag.getLastTag(same_branch=True)}")
```

Get the distance from HEAD to last tag:
```py
print(f"number of commit since last tag: {gitversionhelper.tag.getDistanceFromTag()}")
```
Get the distance from HEAD to last tag [only on same branch]:
```py
print(f"number of commit since last tag: {gitversionhelper.tag.getDistanceFromTag(same_branch=True)}")
```
### sub-lib: version 

Get the last found version in the repository [return MetaVersion object]:
```py
print(f"most recent repository version: {gitversionhelper.version.getLastVersion()}")
```
Get the last found version in the repository [return formated string]:
```py
print(f"most recent repository version: {gitversionhelper.version.getLastVersion(formated_output=True)}")
```
Others kwargs available to this function:

* version_std: string to force a version standard for rendering ["PEP440" or "SemVer"]
* same_branch: boolean to force searching on same branch
* ignore\_unknown\_tags: boolean to allow unknown tag to be ignored

Get the current version of the repository, automatically bump it if the last commit is not tagged [returns MetaVersion object]:
```py
print(f"current repository version: {gitversionhelper.version.getCurrentVersion()}")
```
Or with formated output:
```py
print(f"current repository version: {gitversionhelper.version.getCurrentVersion(formated_output=True)}")
```
Typical usage in CI/CD env:
```py
bumped_version = gitversionhelper.version.getCurrentVersion(    formated_output=True,       \
                                                                version_std="PEP440",       \
                                                                bump_type="dev",            \
                                                                bump_dev_strategy="post")
print(f"current repository version: {bumped_version}")
```
kwargs available to this function:

* All same args as getLastVersion()
* bump_type: if version need to be pump, allow to configure next release update type: __major, minor, patch, dev__
* bump\_dev\_strategy: if bump\_type is dev, allow to choose dev update strategy: __post, pre-patch, pre-minor, pre-major__


A version object can also be manually formated:
```py
_version = gitversionhelper.tag.getCurrentVersion()
```
Then;
```py
_version.doFormatVersion()
```
or;
```py
gitversionhelper.version.doFormatVersion(_version)
```
kwargs available to this function:

- output_format: string to choose a rendering format ["Auto","PEP440" or "SemVer"]

## Limitations

There is unfortunately some technical limitation :

* MultiThreading and async behavior is not tested.
* Multiple tag on the same commit is not supported.
* Branch filter when searching for a version is only tested with -no-ff strategy