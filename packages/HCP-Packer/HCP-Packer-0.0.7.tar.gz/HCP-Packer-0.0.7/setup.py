from pathlib import Path
from setuptools import setup, find_packages

this_folder = Path(__file__).parent
long_description = (this_folder / "README.md").read_text()

setup(
    name='HCP-Packer',
    description='HCP Packer API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.7',
    license='MIT',
    author="Billy Austin",
    author_email="billy@kba-it.com",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url="https://github.com/KBA-IT/hcp-packer",
    keywords="Hashicorp Packer",
    install_requires=[],
)
