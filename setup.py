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
        'setuptools','PyQt6','PyQt6-Charts','numpy','pandas','scipy<=1.15.2','pyinstaller'
    ],
    entry_points={
        'console_scripts': [
            'gelati = gelati.main:main',
        ],
    }
)

