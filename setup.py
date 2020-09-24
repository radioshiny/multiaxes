from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="multiaxes", # Replace with your own username
    version="0.0.7",
    author="Shinyoung Kim",
    author_email="radioshiny@gmail.com",
    description="Multiaxes is a python class based on matplotlib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/radioshiny/multiaxes",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    python_requires='>=2.7',
)