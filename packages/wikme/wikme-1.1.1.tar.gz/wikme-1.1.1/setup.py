from setuptools import setup, find_packages

setup(
    name='wikme',
    version='1.1.1',
    packages=find_packages(),
    install_requires=[
        'cmarkgfm'
    ],
    entry_points={
        'console_scripts': [
            'wikme=wikme.wikme:cmd',
        ],
    },
)
