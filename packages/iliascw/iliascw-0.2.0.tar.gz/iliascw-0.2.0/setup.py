from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='iliascw',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.12.0',
        'certifi==2022.12.7',
        'charset-normalizer==3.1.0',
        'idna==3.4',
        'pydantic==1.10.7',
        'requests==2.28.2',
        'soupsieve==2.4',
        'typing_extensions==4.5.0',
        'urllib3==1.26.15',
    ],
    author='Merlin Sievers',
    author_email='merlin.sievers@posteo.net',
    description='Library to check if courses are available.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/dann-merlin/ilias-course-watcher',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
