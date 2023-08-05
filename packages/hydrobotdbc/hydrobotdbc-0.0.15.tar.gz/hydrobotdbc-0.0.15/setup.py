from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()


setup(
   name='hydrobotdbc',
   version='0.0.15',
   description='A custom Pyodbc wrapper',
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Daniel Ferrer',
   author_email='ferrdan2506@hotmail.com',
   packages=find_packages(),
   install_requires=requirements
)
