"""This file contains some rules for ease build of this application.
"""
from setuptools import setup, find_packages


# The setup util makes it possible to more comfortable build
# and distribute python packages. You can find more information here:
# https://setuptools.readthedocs.io/en/latest/setuptools.html


setup(
    name="kitty_getter",
    version="1.0.0",
    description="The Queue Management System which shows kitties images according queue order.",
    author="Aleksandr Kasian",
    author_email="aleksandr.juicefv@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    # Uncomment this if you don't use the MANIFEST.in
    # package_data={
    #     "application": ["*.yaml",
    #          ".ip_banlist",
    #          "sources/static/icons/*",
    #          "sources/static/images/*",
    #          "sources/static/scripts/*",
    #          "sources/static/styles/*",
    #          "sources/templates/*"],
    # },
    zip_safe=True,
    entry_points={
        'console_scripts':
            ['start_app = application.entry:main']
    }
)
