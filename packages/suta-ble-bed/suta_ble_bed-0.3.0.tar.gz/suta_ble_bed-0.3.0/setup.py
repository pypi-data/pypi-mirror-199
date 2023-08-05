#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ "bleak>=0.19.5", "bleak_retry_connector>=3.0.0" ]

test_requirements = [ ]

setup(
    author="Simon Redman",
    author_email='simon@ergotech.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Handle BLE communications for a SUTA bed frame such as the i500 or i800.",
    entry_points={
        'console_scripts': [
            'suta_ble_bed=suta_ble_bed.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['SUTA','sleepmotion','i500','i900','i200'],
    name='suta_ble_bed',
    packages=find_packages(include=['suta_ble_bed', 'suta_ble_bed.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sredman/suta_ble_bed',
    version='0.3.0',
    zip_safe=False,
)
