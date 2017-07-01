from setuptools import setup
from setuptools.command.install import install
from os.path import expanduser
from shutil import copyfile

setup(
    name='AnendbToFasta',
    version='0.1',
    author='Franca AF (Alexander da Franca Fernandes)',
    author_email='alexander@francafernandes.com.br',
    license='BSD',
    description='Tool to read AnEnDB relational database and generate Fasta files grouped by EC number',
    long_description='Tool to read AnEnDB relational database and generate Fasta files grouped by EC number.',
    packages=[ 'anendbtofasta' ],
    scripts=['bin/anendbtofasta'],
    platforms='Linux',
    url='http://bioinfoteam.fiocruz.br/anendbtofasta',
    install_requires=[
            'datetime ',
            'pprint',
            ],
)


