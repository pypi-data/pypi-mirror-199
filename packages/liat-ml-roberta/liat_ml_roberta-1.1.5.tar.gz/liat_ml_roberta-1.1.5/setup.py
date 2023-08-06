from glob import glob
from os.path import basename, sep
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


with open("README.md", "r", encoding="utf-8") as fp:
    readme = fp.read()

setup(
    name="liat_ml_roberta",
    version="1.1.5",
    description="Multi-Launguage RoBERTa trained by RIKEN-AIP LIAT.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="k141303",
    author_email="kouta.nakayama@gmail.com",
    maintaner="k141303",
    maintaner_email="kouta.nakayama@gmail.com",
    packages=["liat_ml_roberta", "liat_ml_roberta.tokenizers", "liat_ml_roberta.utils"],
    package_dir={"": "src"},
    url="https://github.com/k141303/liat_ml_roberta",
    download_url="https://github.com/k141303/liat_ml_roberta",
    include_package_data=True,
    install_requires=_requires_from_file("requirements.txt"),
)
