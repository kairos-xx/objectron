from setuptools import find_packages, setup

setup(
    name="ObjectronDecorators",
    version="1.0.0",
    description="Decorators for integrating custom classes with the Objectron module.",
    author="Joao Lopes",
    author_email="joaoslopes@gmail.com",
    url="https://github.com/kairos-xx/objectron",
    packages=find_packages(),
    install_requires=[
        "Objectron>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
