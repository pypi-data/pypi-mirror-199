from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="galen",
    version="0.1.1",
    author="rottengeek",
    author_email="daituodi3@gmail.com",
    description="Python spider tool collection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rottengeek/garen",
    packages=["galen"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
