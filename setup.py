#!/usr/bin/env python

from setuptools import find_packages, setup
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='dnsimple-dyndns',
    version='0.1',
    license='BSD',
    description='Dynamic DNS implementation, that relies on DNSimple.com.',
    long_description=long_description,
    author='Rafael Goncalves Martins',
    author_email='rafael@rafaelmartins.eng.br',
    url='https://github.com/rafaelmartins/dnsimple-dyndns',
    packages=find_packages(),
    install_requires=['requests >= 2.0.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={'console_scripts':
                  ['dnsimple-dyndns = dnsimple_dyndns:main']},
)
