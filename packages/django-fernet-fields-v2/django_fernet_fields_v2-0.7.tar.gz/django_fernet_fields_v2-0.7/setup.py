from os.path import join
from setuptools import setup, find_packages


long_description = open("README.rst").read() + open("CHANGES.rst").read()


def get_version():
    with open(join("fernet_fields", "__init__.py")) as f:
        for line in f:
            if line.startswith("__version__ ="):
                return line.split("=")[1].strip().strip("\"'")


setup(
    name="django-fernet-fields-v2",
    version=get_version(),
    description="Fernet-encrypted model fields for Django",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="MichelML, ORCAS, Inc",
    author_email="michmoreau.l@gmail.com",
    url="https://github.com/MichelML/django-fernet-fields/",
    packages=find_packages(),
    install_requires=["Django>=4.0", "cryptography>=0.9"],
    zip_safe=False,
)
