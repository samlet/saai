import setuptools
from setuptools import find_packages, setup, Command

with open("README.md", "r") as fh:
    long_description = fh.read()

# What packages are required for this module to be executed?
REQUIRED = [
    "jieba",
    "simplejson",
    "paddlepaddle-tiny",
]

setuptools.setup(
    name="saai",
    version="0.1.0",
    author="Samlet Wu",
    author_email="xiaofei.wu@gmail.com",
    description="nlu components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samlet/saai",
    packages=find_packages(exclude=('bots', 'tests', 'fsm', )),
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
              'conf': ['*'],
              'data': ['knowledge-base/*']}
    # $ setup.py publish support.
    # cmdclass={
    #     'upload': UploadCommand,
    # },
)

