#!/usr/bin/env python
'''
IT-Magazines WEB Scraper Setup
'''

from setuptools import setup

requires = [
    'requests>=2.28,<3',
    'beautifulsoup4>=4.11,<5'
]

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='itmagazines-webscraper',
    version='0.1.1',
    description='WEB Scraper for IT-Magazines.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='imoni',
    author_email='saito@imoni.net',
    url='https://github.com/imoni31/itmagazines-webscraper',
    packages=['itmagazines_webscraper'],
    python_requires='>=3.7',
    install_requires=requires,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
