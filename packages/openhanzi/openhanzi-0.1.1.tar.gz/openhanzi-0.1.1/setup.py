from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='openhanzi',
    version='0.1.1',
    packages=find_packages(include=['openhanzi']),
    url='',
    license='Apache',
    author='koshinryuu',
    description="A hanzi processing package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)
