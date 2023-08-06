import setuptools

from loci_sarif import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loci-sarif",
    author="TheTwitchy",
    version=__version__,
    author_email="thetwitchy@thetwitchy.com",
    description="The official Loci Notes SARIF processor.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/loci-notes/loci-sarif",
    packages=setuptools.find_packages(),
    install_requires=[
        "loci-cli",
    ],
    entry_points={
        "console_scripts": [
            "loci-sarif = loci_sarif.main:root_entry",
        ],
    },
)
