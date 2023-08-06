from setuptools import setup, find_packages

VERSION = "1.0.2"
DESCRIPTION = "Timeout & retry functions in Python with a single line of code"
with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="pyrtout",
    packages=find_packages(where="pytrout"),
    package_dir={"": "pyrtout"},
)
