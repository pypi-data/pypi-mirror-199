from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Stats Descriptives including frequencies, descriptives, and crosstabs for easy export in xlsx'

# Setting up
setup(
    name="stats_descriptives_001",
    version=VERSION,
    author="Elisabeth Jones",
    author_email="<ejones@rescueagency.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)