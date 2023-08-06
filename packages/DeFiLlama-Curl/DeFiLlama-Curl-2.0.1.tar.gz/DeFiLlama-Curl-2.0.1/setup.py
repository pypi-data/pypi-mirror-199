import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

packages = ['defillama']

requires = [
    'pycurl>=7.44.1',
]

about = {}

with open(os.path.join(here, 'defillama', '__version__.py'),
          mode='r',
          encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md',
          mode='r',
          encoding='utf-8') as f:
    readme = f.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    python_requires='>3.6',
    packages=packages,
    install_requires=requires,
    license=about['__license__'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
