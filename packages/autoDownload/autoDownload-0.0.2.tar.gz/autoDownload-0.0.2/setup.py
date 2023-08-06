# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'autoDownload',
    version = '0.0.2',
    keywords = ('requests'),
    description = 'download files quickly',
    long_description = open("README.md","r",encoding="utf-8").read(),
    author = ['kuankuan'],
    author_email = '2163826131@qq.com',

    install_requires = [
        'requests',
        'rich',
    ],
    packages = ['autoDownload'],
    
    license = 'Mulan PSL v2',
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows'
    ],
    entry_points = {
        'console_scripts': [
            'auto-download = autoDownload.terminal:main',
        ],
    }
)
