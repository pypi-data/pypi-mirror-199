
import re, codecs, sys, os
from setuptools import setup, find_packages

with open('RiZoeLX/version.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

try:
    with codecs.open( "README.md", 'r', errors='ignore' ) as file:
        readme_contents = file.read()
except Exception as error:
    readme_contents = ""
    sys.stderr.write( "Warning: Could not open README.md due %s\n" % error )
    
requirements = ['pyrogram', 'telethon', 'PhoenixScanner']

setup(
    name='pyRiZoeLX',
    author='MrRiZoeL',
    author_email='xrizoel@gmail.com',
    version=version,
    description='A Pyrogram based functional module.',
    long_description = readme_contents,
    long_description_content_type='text/markdown',
    url='https://github.com/RiZoeLX/pyRiZoeLX',
    packages=find_packages(),
    license='GNU General Public License v3.0',
    classifiers=[
        "Framework :: AsyncIO",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Build Tools",

    ],
    include_package_data=True,
    keywords=['telegram', 'pyRiZoeLX', 'RiZoeLX', 'pyrogram', 'functions', 'py-RiZoeLX'],
    install_requires=requirements
)
