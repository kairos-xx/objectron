from setuptools import find_packages, setup

setup(
    name="objectron",
    version="1.0.1",
    description="A powerful Python package for transforming and tracking object references.",
    author="Joao Lopes",
    author_email="joaoslopes@gmail.com",
    url="https://github.com/kairos-xx/objectron",
    packages=find_packages(include=["Objectron", "Objectron.*"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
