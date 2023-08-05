from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="warpspeed-googlesearch-python",
    version="1.1.1",
    author="Warpspeed",
    author_email="hello@warpspeed.cc",
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
    install_requires=[
        "beautifulsoup4>=4.9.3",
        "requests>=2.25.1"
    ],
)
