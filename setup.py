from os import path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
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
    packages=['dropme'],
    entry_points={
        'console_scripts': [
            'dropme = dropme.app:main',
        ],
        'dropme': [
            'df=dropme.commands.account:AccountOwnerSpaceUsageShow',
            'whoami=dropme.commands.account:AccountOwnerInfoShow'
        ],
    },
)
