from io import open

from setuptools import find_packages, setup

version = "0.0.1"

install_requires = [
    "requests",
    "python-ldap",
]

scripts = [
]

entry_points = """
    [console_scripts]
    ldap_sync = ldap_sync.cli:main
"""

setup(
    name="ldap_sync",
    version=version,
    description="Tool to sync user data from a HR management system to a LDAP server.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="",
    keywords=["ops", "linux", "command line tools"],
    author="tclh123",
    author_email="tclh123@gmail.com",
    license="BSD",
    packages=find_packages(exclude=["examples*", "tests*"]),
    include_package_data=True,
    zip_safe=False,
    entry_points=entry_points,
    scripts=scripts,
    install_requires=install_requires,
    extras_require={},
)  # NOQA
