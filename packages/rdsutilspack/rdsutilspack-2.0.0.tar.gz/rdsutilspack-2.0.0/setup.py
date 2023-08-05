from setuptools import setup

setup(
    name='rdsutilspack',
    version='2.0.0',
    description='My first Python package',
    author='johnson',
    author_email='johnssimon007@email.com',
    packages=['rdsutilspack'],
    install_requires=[
        'requests',
        'dnspython',
    ],
    entry_points={
        'console_scripts': [
            'rdsutilspack=rdsutilspack._main_:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
