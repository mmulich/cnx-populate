# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


install_requires = (
    ##'kadabra',
    'lxml',
    'python-magic',  # Not necessary after a kadabra release.
    'psycopg2',
    )
description = "A document population utility for the cnx-archive project."


setup(
    name='cnx-populate',
    version='0.1',
    author='Connexions team',
    author_email='info@cnx.org',
    url="https://github.com/connexions/cnx-population",
    license='LGPL, See aslo LICENSE.txt',
    description=description,
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    entry_points="""\
    [console_scripts]
    cnx-populate = cnxpopulate:main
    """,
    # test_suite=''
    )
