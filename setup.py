
"""
Setup.py for ontulily
"""
from setuptools import setup

setup(
    name='ontulily',
    version='0.1',
    description='A testing tool.',
    license='MIT',
    author='moshthepitt',
    author_email='mosh@mosh.co.ke',
    install_requires=[
        'django_micro',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
    ],
)
