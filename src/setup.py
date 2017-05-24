# Always prefer setuptools over distutils
from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='clustering',
      version='0',
      description='clustering',
      url='https://github.com/cityofboston/<boston_analytics_example>',
      author='Kayla Patel',
      author_email='paylakatel@gmail.com',
      packages=find_packages(),
      zip_safe=False)
