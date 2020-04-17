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
    "colorlog",
    "jieba~=0.40",
    "simplejson",
    "paddlepaddle-tiny~=1.6.1",
    "sagas>=0.1.2",
    "python_json_config",
    "python-dotenv",
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

    include_package_data=True,
    packages=["", *find_packages(exclude=('bots', 'tests', 'fsm', 'notebook',))],
    entry_points={"console_scripts": ["saai=saai.__main__:main",
                                      "saash=saai.shell.__main__:shell_main",
                                      ]},
    install_requires=REQUIRED,
    extras_require={
        'rasa': ['rasa~=1.9.5', 'rasa-sdk~=1.9.0'],
        'dev': ['jupyter~=1.0.0', 'streamlit~=0.50.2', 'ipymarkup~=0.5.0'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # package_data={
    #     'saai': ['conf/*', 'templates/*', 'scaffold/*'],
    #     'data': ['knowledge-base/*'],
    # },
    # $ setup.py publish support.
    # cmdclass={
    #     'upload': UploadCommand,
    # },
    project_urls={
        "Bug Reports": "https://github.com/samlet/saai/issues",
        "Source": "https://github.com/samlet/saai",
    },
)

