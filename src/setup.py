# Always prefer setuptools over distutils
from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='cluster_311',
      version='0',
      description='cluster 311',
      url='https://github.com/cityofboston/<boston_analytics_example>',
      author='Kayla Patel',
      author_email='paylakatel@gmail.com',
      packages=find_packages(),
      zip_safe=False)
