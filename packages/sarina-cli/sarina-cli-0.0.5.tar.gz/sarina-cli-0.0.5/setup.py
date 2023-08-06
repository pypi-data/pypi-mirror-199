from distutils.core import setup, Extension

import os

MINIMAL_DESCRIPTION = '''Sarina is an ASCII art generator written in Python3 and C++. It transforms an input image and a text file containing words and their weights into a unique ASCII art representation. The algorithm behind Sarina is randomized, ensuring that every output is distinct, even for identical inputs.'''

def get_requires():
    """Read requirements.txt."""
    requirements = open('requirements.txt', "r").read()
    return list(filter(lambda x: x != "", requirements.split()))

def read_description():
    """Read README.md and CHANGELOG.md."""
    try:
        with open("README.md") as r:
            description = "\n"
            description += r.read()
        return description
    except Exception:
        return MINIMAL_DESCRIPTION
# output a .so file
cpp_module = Extension('cpp_backend', sources=[os.path.join('sarina', 'cpp_backend', 'lib', 'cpp_backend.cpp')], extra_compile_args=['-std=c++11'])
    

setup(
    name="sarina-cli",
    version="0.0.5",
    author='Amin Alam',
    description='ASCII Art Generator',
    long_description=read_description(),
    long_description_content_type='text/markdown',
    # add requirements.txt to the package data
    package_data={'': ['requirements.txt']},
    install_requires=get_requires(),
    python_requires='>=3.5',
    license='MIT',
    include_package_data=True,
    url='https://github.com/AminAlam/Sarina',
    keywords="ASCII-Art Word-Cloud-Generator",
    entry_points={
        'console_scripts': [
            'sarina=sarina.__main__:main',
        ]
    },
    packages=['sarina'],
    ext_modules=[cpp_module],
    )

