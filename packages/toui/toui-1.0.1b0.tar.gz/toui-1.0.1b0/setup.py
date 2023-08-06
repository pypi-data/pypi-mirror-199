import setuptools
from toui import __version__

with open("README.md", "r") as file:
    long_description = file.read()

name = "ToUI"
version = __version__
author = "Mubarak Almehairbi"
description = "Creates user interfaces (websites and desktop apps) from HTML easily"
package_name = "toui"
requirements = []
with open(f"requirements.txt", "rt") as file:
    for pkg in file.read().splitlines():
        pkg_name = pkg.split("==")[0]
        pkg_version = pkg.split("==")[1]
        pkg_major_version = pkg_version.split(".")[0]
        req = f"{pkg_name}>={pkg_version},<{int(pkg_major_version)+1}"
        requirements.append(req)


setuptools.setup(
    name=package_name,                     # This is the name of the package
    version=version,                        # The initial release version
    author=author,                     # Full name of the author
    description=description,
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    py_modules=[package_name],             # Name of the python package
    install_requires=requirements                     # Install other dependencies if any
)