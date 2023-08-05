from setuptools import setup, find_packages
import codecs
import os

readme_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "cetl")

with codecs.open(os.path.join(readme_dir, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read() + "\n this version will solve the issue of UnboundLocalError: \n"+\
                        "local variable 'pre_transformer_key' referenced before assignment"

# Setting up
setup(
    name="cetl",
    version='0.2.6',
    author="Clement",
    author_email="<cheukub@gmail.com>",
    description='A basic data pipeline tools for data engineer to handle the CRM or loyalty data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['flask', 'SQLalchemy', 'pyspark', 'pandas'],
    keywords=['python', 'data pipeline', 'pipeline'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ]
)