#import required functions
from setuptools import setup, find_packages

#call setup function
setup(
    author="David Chapuis",
    description="A package allowing you to get national holidays for 200+ countries around the world.",
    name="natholi",
    version="0.1.0",
    packages=find_packages(include=["natholi", "natholi.*"]),
    install_requires=['pandas', 'requests', 'json'],
)
