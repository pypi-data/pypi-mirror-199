# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trddt",
    version="0.1.0",
    author="innovata",
    author_email="iinnovata@gmail.com",
    description='한국거래소 기준 Datetime Functions 패키지',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/TradeDatetime",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=['ipylib'],
)
