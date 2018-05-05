
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
    url='https://github.com/moshthepitt/ontulily',
    install_requires=[
        'django_micro',
        'fake-useragent',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
    ],
)
