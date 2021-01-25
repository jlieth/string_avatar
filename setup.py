import os
from setuptools import setup, find_packages

basedir = os.path.abspath(os.path.dirname(__file__))
long_descr = ""
with open(os.path.join(basedir, "README.rst")) as f:
    long_descr += f.read()

REQUIREMENTS = ["Pillow", "pydantic"]

DEV_REQUIREMENTS = [
    "tox",
    "pytest",
    "pytest-mypy",
    "pytest-flake8",
    "pytest-black",
    "pytest-isort",
    "pytest-cov",
]


setup(
    name="string_avatar",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*"]),
    version="0.0.1",
    author="jlieth",
    description="Create custom avatars based on an input string",
    long_description=long_descr,
    license="MIT",
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
    tests_require=DEV_REQUIREMENTS,
    include_package_data=True,
    keywords=["image", "avatar", "picture"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Graphics",
    ],
)
