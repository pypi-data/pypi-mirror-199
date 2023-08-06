from __future__ import annotations

from pathlib import Path

import setuptools


PACKAGE_NAME = 'artemis-common'
PACKAGE_DIR = Path(__file__).resolve().parent


def read_requirements(filename: str) -> list[str]:
    requirements_file = PACKAGE_DIR.joinpath(filename)
    raw_requirements = requirements_file.read_text()
    return [line for line in raw_requirements.split('\n') if line]


def read_version():
    version_file = PACKAGE_DIR.joinpath('version')
    return version_file.read_text()


setuptools.setup(
    name=PACKAGE_NAME,
    version=read_version(),
    author='0xArti',
    author_email='contact@hunters-of-artemis.com',
    description='Artemis common project utilities',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.10',
    install_requires=read_requirements('requirements.txt'),
)
