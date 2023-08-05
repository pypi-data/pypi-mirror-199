# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kwdataengineer",
    version="0.2.0",
    author="innovata sambong",
    author_email="iinnovata@gmail.com",
    description='키움증권 자동매매 프로그램을 위한 데이타엔지니어링 패키지. 32/64비트 모두 지원해야함',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/KiwoomDataEngineer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"pkgs"},
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
