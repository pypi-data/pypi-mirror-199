from __future__ import annotations

from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text("utf-8")
setup(
    name="lobsterpy",
    version="0.2.9",
    description="Package for autmatic bonding analysis with Lobster/VASP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jageo/lobsterpy",
    author="Janine George",
    author_email="janine.george@bam.de",
    license="BSD 3-clause",
    packages=find_packages(),
    install_requires=[
        "pymatgen>=2023.1.20",
        "numpy",
        "typing",
        "Sphinx>=4",
        "sphinx-argparse==0.4.0",
        "sphinx-pdj-theme==0.2.1",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "lobsterpy = lobsterpy.cli:main",
        ]
    },
    package_data={
        "lobsterpy": [
            "plotting/lobsterpy_base.mplstyle",
        ]
    },
)
