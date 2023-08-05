import os

from setuptools import setup

# read the contents of your README file

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version_dev='1.0.0'
version_prod='1.0.5'

run_mode=''

setup(name='m-formatter-logging' + run_mode,
      version='1.0.5',
      description='MobioLogging',
      url='',
      author='MOBIO',
      author_email='contact@mobio.io',
      packages=['mobio/libs/logging'],
      package_data={'': ['*.*']},
      install_requires=['m-singleton',
                        'configparser==3.5.0',
                        'logstash_formatter==0.5.17'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      python_requires='>=3.8'
      )
