from pathlib import Path
from setuptools import setup, find_packages

this_folder = Path(__file__).parent
long_description = (this_folder / "README.md").read_text()

setup(
    name='HCP-Packer',
    description='HCP Packer API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.12',
    license='MIT',
    author="KBA IT",
    author_email="info@kba-it.com",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://kba-it.com',
    project_urls={
        'Source': 'https://github.com/KBA-IT/hcp-packer',
    },
    keywords="Hashicorp Packer",
    install_requires=[],
)
