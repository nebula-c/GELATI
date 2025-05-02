from setuptools import setup

setup(
    name='GELATI',
    version='0.1',
    packages=find_packages(where='src'),
	install_requires=[
        'PyQt6',
    ],
    entry_points={
        'console_scripts': [
            'myapp = gelati.main:main',
        ],
    }
)

