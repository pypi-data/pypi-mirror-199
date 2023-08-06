from setuptools import setup, find_packages

setup(
    name='nepictures',
    version='0.1.0',
    description='My awesome package',
    author='Jane Doe',
    author_email='jane@example.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ]
)