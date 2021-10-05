import re
import shutil
from setuptools import find_packages

try:
    from setuptools import setup
    from setuptools.command.install import install
    from setuptools.command.develop import develop
    from setuptools.command.egg_info import egg_info
    from setuptools.command.sdist import sdist
    from setuptools.command.build_py import build_py
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install
    from distutils.command.build_py import build_py

AUTHOR = "Fraud team"
NAME = "fraud_demo"
DESCRIPTION = "Fraud demo"
URL = "https://gitlab.id.vin/data/fs-gt-scoring"
REQUIRES_PYTHON = ">=3.7.0"
REQUIRED = ["feast[gcp]==0.12.1", "kfp==1.8.0", "scikit-learn>=0.24.2"]

# Add Support for parsing tags that have a prefix containing '/' (ie 'sdk/go') to setuptools_scm.
# Regex modified from default tag regex in:
# https://github.com/pypa/setuptools_scm/blob/2a1b46d38fb2b8aeac09853e660bcd0d7c1bc7be/src/setuptools_scm/config.py#L9
TAG_REGEX = re.compile(
    r"^(?:[\/\w-]+)?(?P<version>[vV]?\d+(?:\.\d+){0,2}[^\+]*)(?:\+.*)?$"
)

# Only set use_scm_version if git executable exists (setting this variable causes pip to use git under the hood)
if shutil.which("git"):
    use_scm_version = {"root": "../..", "relative_to": __file__, "tag_regex": TAG_REGEX}
else:
    use_scm_version = None


setup(
    name=NAME,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    include_package_data=True,
    version=use_scm_version,
    setup_requires=["setuptools_scm"],
    package_data={},
)
