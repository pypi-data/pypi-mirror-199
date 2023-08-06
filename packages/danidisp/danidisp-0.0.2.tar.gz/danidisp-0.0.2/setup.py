from setuptools import setup

setup(
    name="danidisp",
    version='0.0.2',
    description='My package, every useful function I want to use',
    py_modules=['xor'],
    package_dir={'': 'src'},
    url="https://github.com/DanieleDiSpirito/",
    author="Daniele Di Spirito",
    author_email="danieledisp@proton.me",
    long_description='''
        Package contains:
        - xor(a: bytes, b: bytes) -> bytes
    '''
)