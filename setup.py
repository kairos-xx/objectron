from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="objectron",
    version="1.0.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description=(
        "A powerful Python package for"
        + "transforming and tracking object references."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joao Lopes",
    author_email="joaoslopes@gmail.com",
    url="https://github.com/kairos-xx/objectron",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Debuggers",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Typing :: Typed",
        "Framework :: IPython",
        "Environment :: Console",
    ],
    python_requires=">=3.11",
    install_requires=["rich>=10.0.0"],
    keywords=(
        "path-based-access proxy object-transformation "
        + "monitoring reference-tracking python3"
    ),
    project_urls={
        "Homepage": "https://github.com/kairos-xx/objectron",
        "Bug Tracker": "https://github.com/kairos-xx/objectron/issues",
        "Documentation": "https://github.com/kairos-xx/objectron/wiki",
        "Source Code": "https://github.com/kairos-xx/objectron",
    },
)
