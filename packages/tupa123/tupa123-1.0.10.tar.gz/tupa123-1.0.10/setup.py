from setuptools import setup

setup(
    name='tupa123',
    version='1.0.10',
    packages=['tupa123'],
    install_requires=['numpy>=1.23.5','matplotlib>=3.6.3','pandas>=1.5.3'],
    license = 'MIT',
    license_files=('LICENSE.txt',),
    author='Leandro Schemmer',
    author_email='leandro.schemmer@gmail.com',    
    description= 'fully connected neural network with four layers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='artificial intelligence neural networks four layers regression classification'
)
