from setuptools import setup

setup(
    name='transkribus-to-prima',
    version='0.0.1',
    author="kba, bertsky",
    author_email="unixprog@gmail.com",
    url="https://github.com/kba/transkribus-to-prima",
    license='Apache License 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=open('requirements.txt').read().split('\n'),
    packages=['transkribus_to_prima'],
    entry_points={
        'console_scripts': [
            'transkribus-to-prima=transkribus_to_prima.cli:cli',
            'page-fix-coordinates=transkribus_to_prima.cli_coordinate_to_prima:cli',
            'page-dimensions-from-image=transkribus_to_prima.set_dimensions_from_image:cli'
        ]
    },
)
