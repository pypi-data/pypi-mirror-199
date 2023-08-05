from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    requirements = fh.read().split("\n")

setup(
    name="warpspeed-googlesearch-python",
    version="1.1.0",
    author="Warpspeed",
    description="A Python library for scraping the Google search engine. Forked from "
                "https://pypi.org/project/googlesearch-python/ to loosen requirements constraints.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usewarpspeed/googlesearch",
    packages=["googlesearch"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[requirements],
)
