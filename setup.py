from setuptools import find_packages,setup



setup(
    name="GELATI",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        'gelati': ['images/*'],
    },
    install_requires=[
        'PyQt6'
    ],
    entry_points={
        'console_scripts': [
            'gelati = gelati.main:main',
        ],
    }
)

