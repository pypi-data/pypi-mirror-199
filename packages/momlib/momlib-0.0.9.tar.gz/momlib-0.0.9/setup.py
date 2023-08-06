from setuptools import setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="momlib",
    version="0.0.9",
    author="B. Roux",
    packages=["momlib"],
    description="Mathematical Object Manipulation Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/B-Roux/momlib",
    project_urls={
        "Bug Tracker": "https://github.com/B-Roux/momlib/issues",
    },
    license="BSD (3-Clause)",
    keywords=[
        "library",
        "vector",
        "matrix",
        "mathematics",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
