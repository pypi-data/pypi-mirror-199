from setuptools import setup, find_packages

setup(
    name="french-bins",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Abysse",
    author_email="pypi@abysseyes.com",
    description="A library for Bins from French banks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/toomanylog/french-bins",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
