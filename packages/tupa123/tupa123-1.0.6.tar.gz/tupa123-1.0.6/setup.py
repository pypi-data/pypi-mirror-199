from setuptools import setup

setup(
    name='tupa123',
    version='1.0.6',
    license='MIT',
    data_files=[('', ['LICENSE.txt'])],
    long_description=open('README.md').read(),
    description= 'fully connected neural network with four layers',
    author='Leandro Schemmer',
    author_email='leandro.schemmer@gmail.com',
    packages=['tupa123'],
    install_requires=['numpy>=1.23.5','matplotlib>=3.6.3','pandas>=1.5.3']
)
