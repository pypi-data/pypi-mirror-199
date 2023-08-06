from setuptools import setup, find_packages

setup(
    name="rulelearn",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
    
        "pandas",
        "numpy",
        "scipy",
        "numba",
        "matplotlib",
        "scikit-learn",
        "cvxpy",
        "torch",
        "xmltodict",
        "nyoka==5.4.0"


    ],

    author="Various",
    author_email="hvoelzer@acm.org",
    description="This package contains a rule induction toolkit to generate readable and editable rules from data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IBM/rulelearn",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
)
