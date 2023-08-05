from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.1.2'
DESCRIPTION = 'Navigating through GitHub repositories'

# Setting up
setup(
    name="reponav",
    version=VERSION,
    author="Reem Alsharabi",
    author_email="<Reem.Alsharabi@outlook.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['github', 'PyGithub'],
    keywords=['python', 'github', 'repository', 'structure'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)