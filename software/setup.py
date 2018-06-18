'''
Setup for the polnear package, a python utility that simplifies access to the 
PolNeAR dataset for Python programmers.
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description = (
    
)

setup(
    name='polnear',

    # Versions should comply with PEP440.  For a discussion on 
	# single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.0',

    description='Work with the PolNeAR dataset in Python',
    long_description=(
        "Easily incorporate the PolNeAR data into any python project."
    ),

    # The project's main homepage.
    url='https://github.com/networkdynamics/PolNeAR',

    # Author details
    author='Edward Newell',
    author_email='edward.newell@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords= (
		'NLP natrual language processing computational linguistics ',
		'PolNeAR Political News Attribution Relations Corpus'
	),

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['polnear'],
	#indlude_package_data=True,
	install_requires=[
        'parc-reader==0.1.5', 't4k>=0.6.4', 'corenlp-xml-reader>=0.1.3', 'brat-reader>=0.0.0']
)
