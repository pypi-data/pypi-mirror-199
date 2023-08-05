import codecs
import os
from textwrap import dedent

from setuptools import setup

_dir = os.path.dirname(__file__)


def find_version():
    f = codecs.open('version', 'r', 'utf-8-sig')
    line = f.readline()
    f.close()
    return line


def finedescription():
    line = ''
    with open(os.path.join(_dir, 'README.rst')) as f:
        line = f.read()
    return line


PACKAGE_VERSION = str(find_version())

PACKAGE_LONG_DESCRIPTION = str(finedescription())
requires_install = [
    "pyAesCrypt>=6.0.0",
]
setup(
    name='pyfastkvjson',
    version=PACKAGE_VERSION,
    use_scm_version=False,
    description="Json key store with secured feature.",
    long_description=PACKAGE_LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    author="Oliver Bristow, Heskemo",
    author_email='github+pypi@oliverbristow.co.uk',
    license='MIT',
    classifiers=dedent("""
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: 3.7
        Programming Language :: Python :: 3.8
        Programming Language :: Python :: 3.9
        Programming Language :: Python :: Implementation :: CPython
        Programming Language :: Python :: Implementation :: PyPy
        Topic :: Database
        Topic :: Software Development
    """).strip().split('\n'),
    keywords='json key value store and more secured',
    url='https://github.com/ONode/pyfastkvjson/',
    py_modules=dedent("""
        jsonstore
    """).strip().split('\n'),
    install_requires=requires_install,
    setup_requires=["setuptools_scm", "wheel"],
)
