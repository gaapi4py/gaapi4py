from setuptools import setup

setup(
    name="gaapi4py",
    version="0.1",
    description="Google Analytics Reporting API v4 for Python 3",
    url="http://github.com/ptrvtch/gaapi4py",
    author="Oleh Omelchenko",
    author_email="ptrvtch@gmail.com",
    license="MIT",
    pagkages=["gaapi4py"],
    zip_safe=False,
    install_requires=[
        "pandas",
        "pandas-gbq",
        "oauth2client",
        "google-api-python-client",
    ],
)
