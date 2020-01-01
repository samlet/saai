import os
import setuptools
from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
with open("saai/version.py") as f:
    exec(f.read())

with open("README.md", "r") as fh:
    long_description = fh.read()

# What packages are required for this module to be executed?
REQUIRED = [
    "jieba",
    "simplejson",
    "paddlepaddle-tiny",
    "sagas>=0.1.1",
]

setuptools.setup(
    name="saai",
    version=__version__,
    author="Samlet Wu",
    author_email="xiaofei.wu@gmail.com",
    description="nlu components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samlet/saai",
    packages=["", *find_packages(exclude=('bots', 'tests', 'fsm', ))],
    entry_points={"console_scripts": ["saai=saai.__main__:main"]},
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
              'saai': ['conf/*', 'templates/*'],
              'data': ['knowledge-base/*']},
    # $ setup.py publish support.
    # cmdclass={
    #     'upload': UploadCommand,
    # },
    project_urls={
        "Bug Reports": "https://github.com/samlet/saai/issues",
        "Source": "https://github.com/samlet/saai",
    },
)

