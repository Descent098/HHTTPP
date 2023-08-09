"""Contains all the configuration for the package on pip"""
import setuptools
from hhttpp import __version__

def get_content(*filename:str) -> str:
    """ Gets the content of a file or files and returns
    it/them as a string
    Parameters
    ----------
    filename : (str)
        Name of file or set of files to pull content from 
        (comma delimited)
    
    Returns
    -------
    str:
        Content from the file or files
    """
    content = ""
    for file in filename:
        with open(file, "r") as full_description:
            content += full_description.read()
    return content

setuptools.setup(
    name = "hhttpp",
    version = __version__,
    author = "Kieran Wood",
    author_email = "kieran@canadiancoding.ca",
    description = "Free range artisnal HTTP",
    long_description = get_content("README.md"),
    long_description_content_type = "text/markdown",
    project_urls = {
        "Source" :         "https://github.com/descent098/hhttpp",
        "Bug Report":      "https://github.com/descent098/hhttpp/issues/new?assignees=Descent098&labels=bug&template=bug_report.md&title=%5BBUG%5D",
    },
    include_package_data = True,
    packages = setuptools.find_packages(),
    entry_points = { 
           'console_scripts': ['hhttpp = hhttpp.cli:main']
       },
    install_requires = [
    "docopt", # Used for argument parsing if you are writing a CLI
        ],
    extras_require = {
        "dev" : [
                "pytest",  # Used to run the test code in the tests directory
                ],
    },
    classifiers = [ # SEE: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Development Status :: 1 - Planning"
    ],
)