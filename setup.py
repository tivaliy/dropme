import os
import io

from setuptools import setup, find_packages
# Get the long description from the README file
here = os.path.dirname(__file__)

with io.open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Information Technology',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Communications :: File Sharing',
]

setup(
    name='dropme',
    version='1.1.0',
    install_requires=[
        'cliff>=2.9.0',
        'dropbox>=8.5.0',
        'PyYAML>=3.1.0',
    ],
    description='CLI tool for managing Dropbox environment.',
    long_description=long_description,
    url='https://github.com/tivaliy/dropme',
    author='Vitalii Kulanov',
    author_email='vitaliy@kulanov.org.ua',
    license='MIT',
    classifiers=classifiers,
    keywords='CLI Dropbox',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dropme = dropme.app:main',
        ],
        'dropme': [
            'cp=dropme.commands.files:FileFolderCopy',
            'df=dropme.commands.account:AccountOwnerSpaceUsageShow',
            'find=dropme.commands.files:FileFolderSearch',
            'get=dropme.commands.files:FileGet',
            'ls=dropme.commands.folder:FolderList',
            'mkdir=dropme.commands.folder:FolderCreate',
            'mv=dropme.commands.files:FileFolderMove',
            'put=dropme.commands.files:FilePut',
            'restore=dropme.commands.files:FileRestore',
            'revs=dropme.commands.files:FileRevisionsList',
            'rm=dropme.commands.files:FileFolderDelete',
            'status=dropme.commands.files:FileFolderStatusShow',
            'whoami=dropme.commands.account:AccountOwnerInfoShow'
        ],
    },
)
