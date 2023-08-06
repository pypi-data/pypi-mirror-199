from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pycfalias',
    version='0.0.8',
    author='Eliel Garcia',
    author_email='inbox@eliel-garcia.com',
    description='Simple Cloudflare email alias management',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ellie-gar/pycfalias",
    packages=['pycfalias'],
    entry_points={
        'console_scripts': [
            'pycfalias = pycfalias.pycfalias:main'
        ]
    },
    install_requires=[
        'prettytable~=3.6.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
