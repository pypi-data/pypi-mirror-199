from setuptools import setup, find_packages

# read requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='wikme',
    version='1.0',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'wikme=wikme.wikme:cmd',
        ],
    },
)