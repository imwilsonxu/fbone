# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='fbone',
    version='0.1',
    description='Flask Skeleton Project',
    author='Wilson Xu',
    author_email='imwilsonxu@gmail.com',
    packages=['fbone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-Script',
        'Flask-Babel',
        'Flask-Testing',
        'Flask-Uploads',
        'Flask-Mail',
        'Flask-Cache',
        'Flask-Login',
        'nose',
    ]
)
