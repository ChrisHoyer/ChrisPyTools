from pathlib import Path
from setuptools import setup, find_packages

AUTHOR_NAME = 'Chris Hoyer'
AUTHOR_EMAIL = 'info@chrishoyer.de'

ROOT = Path(__file__).resolve().parent

# get latest version from source code
def get_version():
    v = {}
    for line in (ROOT / "src" / "chrispytools" / "__init__.py").read_text().splitlines():
        if line.strip().startswith('__version__'):
            exec(line, v)
            return v['__version__']
    raise IOError('__version__ string not found')

# get description from readme.md
def get_description():  
    long_description = ""
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description    

setup(name='chrispytools',
      version=get_version(),
      description='ChrisPyTools is a set of tools and functions that can be used to quickly plot and analyze data.',
      url='https://github.com/ChrisHoyer/ChrisPyTools.git',
      author=AUTHOR_NAME,
      author_email=AUTHOR_EMAIL,
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      python_requires=">=3.7",
      long_description=get_description(),
      long_description_content_type="text/markdown",    
      )