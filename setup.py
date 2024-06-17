from setuptools import setup, find_packages
setup(
    name='grcp-aio-bug',
    version='0.0.1',
    description='Demonstrates python grpc aio ',
    author='Sean Story',
    author_email='sean.story@elastic.co',
    packages=find_packages(),
    install_requires=[
        'grpcio>=1.64',
        'protobuf>=5.27'
    ],
)