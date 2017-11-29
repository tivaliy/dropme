import os
import io

from setuptools import setup, find_packages
# Get the long description from the README file
here = os.path.dirname(__file__)

with io.open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 1 - Planning',
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
    version='0.0.1',
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
            'df=dropme.commands.account:AccountOwnerSpaceUsageShow',
            'download=dropme.commands.files:FileDownload',
            'ls=dropme.commands.folder:FolderList',
            'mkdir=dropme.commands.folder:FolderCreate',
            'rm=dropme.commands.files:FileFolderDelete',
            'upload=dropme.commands.files:FileUpload',
            'whoami=dropme.commands.account:AccountOwnerInfoShow'
        ],
    },
)
