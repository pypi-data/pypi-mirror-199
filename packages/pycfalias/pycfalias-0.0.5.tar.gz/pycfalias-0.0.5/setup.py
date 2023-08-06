from setuptools import setup, find_packages

setup(
    name='pycfalias',
    version='0.0.5',
    author='Eliel Garcia',
    author_email='inbox@eliel-garcia.com',
    description='Simple Cloudflare email alias management',
    long_description='Simple Cloudflare email alias management',
    packages=['pycfalias'],
    entry_points={
        'console_scripts': [
            'pycfalias = pycfalias.pycfalias:main'
        ]
    },
    install_requires=[
        'prettytable~=3.6.0'
    ]
)
