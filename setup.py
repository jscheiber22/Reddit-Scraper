from setuptools import setup, find_packages

setup(
    name='reddit-scraper', # does not need to be anything related to actual name
    version='0.1.0',
    license='MIT',
    description='A program that scrapes subreddits and pulls a butt load of images.',
    author='James Scheiber',
    author_email='jscheiber22@gmail.com',
    url="https://www.scheibertech.com",
    packages=find_packages(include=['reddit', 'reddit.*']),  # Not top-most folder, the one with the actual python files should go here
    install_requires=[ # min version not required
    ]
)
