from setuptools import setup

setup(
    name='transkribus_fixer',
    version='0.0.1',
    author="kba",
    author_email="unixprog@gmail.com",
    url="https://github.com/kba/transkribus-fixer",
    license='Apache License 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=open('requirements.txt').read().split('\n'),
    packages=['transkribus_fixer'],
    entry_points={
        'console_scripts': [
            'transkribus-fixer=transkribus_fixer.cli:cli'
        ]
    },
)
