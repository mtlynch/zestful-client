#!/usr/bin/env python

import os.path

import setuptools

setuptools.setup(
    name='zestful-parse-ingredient',
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     'README.md')).read(),
    long_description_content_type="text/markdown",
    version='0.0.5',
    description=
    'Parse recipe ingredients into structured data (name, quantity, units, preparation notes)',
    project_urls={
        "repository": "https://github.com/mtlynch/zestful-client",
    },
    author='Michael Lynch',
    author_email='michael@zestfuldata.com',
    license="MIT",
    keywords="ingredients ingredient parsing recipes nlp zestful",
    url='https://github.com/mtlynch/zestful-client.git',
    packages=['parse_ingredient', 'parse_ingredient.internal'],
    install_requires=[],
    python_requires='>=3.7',
)
