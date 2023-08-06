from setuptools import setup, find_packages

import os

here = os.path.abspath(os.path.dirname(__file__))


VERSION = "1.0.4"
DESCRIPTION = "Streaming video data via networks"
LONG_DESCRIPTION = (
    "A package that allows to build simple streams of video, audio and camera data."
)

# Setting up
setup(
    name="pyrtout",
    version=VERSION,
    author="Arijit Roy (radioactive11)",
    author_email="<roy.arijit@icloud.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
