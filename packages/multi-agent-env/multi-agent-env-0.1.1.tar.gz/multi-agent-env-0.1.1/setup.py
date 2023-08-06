# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='multi-agent-env',
    packages=find_packages(include=['multi-agent-env']),
    version='0.1.1',
    description='Multi-agent environment for reinforcement learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ted',
    license='GPL-3.0',
    install_requires=["numpy", "pygame"],
    url="https://github.com/ECE324-MI-Gang/Multi-agent-Env",
)
