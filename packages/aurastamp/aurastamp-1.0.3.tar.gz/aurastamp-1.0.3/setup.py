from setuptools import setup, find_packages

setup(
    name='aurastamp',
    version='1.0.3',
    description='aurastamp api for python',
    author='stegato',
    author_email='admin@stegato.com',
    url='',
    install_requires=['requests', 'requests_toolbelt', 'Pillow'],
    packages=find_packages(exclude=[]),
    keywords=['aurastamp', 'steganography'],
    python_requires='>=3.6',
    zip_safe=False
)
