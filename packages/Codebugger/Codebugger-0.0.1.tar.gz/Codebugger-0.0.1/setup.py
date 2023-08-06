from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Codebugger explains the buggy code in simple terms and offers ways to fix the code.'
LONG_DESCRIPTION = 'Codebugger explains the buggy code in simple terms and offers ways to fix the code. \
                    This takes away hours of frustration by helping you understand the root cause of the \
                    error, helping to clear up any misconceptions, and saving you time. Debugger uses gpt \
                    language model from Openai.'

# Setting up
setup(
    name="Codebugger",
    version=VERSION,
    author="Gabriel Cha",
    author_email="gcha@ucsd.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['openai'],
    keywords=['python', 'debugger', 'gpt'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
