from setuptools import setup

classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]
version = "0.0.0.111"

setup(
    name="aylak",
    version=version,
    author="aylak-github",
    description="Aylak PyPi",
    long_description="aylak pypi",
    long_description_content_type="text/markdown",
    url="https://github.com/aylak-github/aylak-pypi",
    license="GNU AFFERO GENERAL PUBLIC LICENSE (v3)",
    packages=["aylak"],
    install_requires="pythonansi",
    classifiers=classifiers,
    python_requires=">3",
)
