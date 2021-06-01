from pathlib import Path

from setuptools import find_packages, setup

with open(Path(__file__).resolve().parent / "README.md") as f:
    readme = f.read()

setup(
    name="flexfs",
    url="https://github.com/clbarnes/ffs",
    author="Chris L. Barnes",
    description="Python tools for querying Flexible File Structure",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["ffs*"]),
    install_requires=[
        "strictyaml",
        "toml",
        "setuptools",
        "click",
        "networkx",
        "typing-extensions; python_version < '3.7'",
    ],
    python_requires=">=3.7, <4.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    use_scm_version=True,
    entry_points={"console_scripts": ["ffs=ffs.cli:main"]},
    setup_requires=["setuptools_scm"],
    package_data={"": ["*.md"]},
)
