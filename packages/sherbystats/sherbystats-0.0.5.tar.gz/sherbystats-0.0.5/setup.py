import setuptools


setuptools.setup(
    name="sherbystats",
    version="0.0.5",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    url="https://www.usherbrooke.ca/gchimiquebiotech/departement/professeurs/ryan-gosselin/",
    packages=["sherbystats"],
    description="Ryan @ UdeS",
    long_description="Python for GCB140 and GCH711:\
    \n\
    \nfct_anova\
    \nfct_doe\
    \nfct_mlr\
    \nfct_xlsread",
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)