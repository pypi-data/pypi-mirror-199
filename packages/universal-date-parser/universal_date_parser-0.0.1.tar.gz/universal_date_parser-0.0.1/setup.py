from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="universal_date_parser",
    version="0.0.1",
    author="Guangyu He",
    author_email="me@heguangyu.net",
    description="A universal date parser to parse any kind of (possible) date strings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guangyu-he/universal_date_parser",
    install_requires=[
        "pandas>=1.5.3",
    ],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    tests_require=["pytest"]
)
