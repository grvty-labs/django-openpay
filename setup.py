import os
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='django-openpay',
    version='0.4.0',
    description='Django application which integrates the \
OpenPay libraries for online transactions',
    long_description=readme,
    author='GRVTYlabs',
    author_email='daniel.ortiz@grvtylabs.com',
    url='https://github.com/grvty-labs/django-openpay',
    packages=find_packages(
        exclude=['django_openpay_repo.*', 'django_openpay_repo']),
    # packages=['django_openpay'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'jsonfield',
        'OpenpayGrvty>=0.4.7',
    ]
)
