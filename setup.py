from setuptools import setup, find_packages
from gaapi4py import name, version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=name,
    version=version,
    description="Google Analytics Reporting API v4 for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/gaapi4py/gaapi4py",
    author="Oleh Omelchenko",
    author_email="ptrvtch@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    install_requires=["pandas", "oauth2client", "google-api-python-client"],
)
