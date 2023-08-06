from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='sabia-utils',
    version='0.1.5',
    license='MIT License',
    author='Pedro Jesus',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='pedrovitora.jesus@gmail.com',
    keywords='sabia utils',
    description=u'Group of utilities for Sabia',
    packages=['sabia_utils', 'sabia_utils.utils'],
    install_requires=[
        'pandas==1.4.3',
        'alei-utils==0.1.3',
        'pyarrow==6.0.1'
    ],)
