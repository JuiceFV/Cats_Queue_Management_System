"""This file contains some rules for ease build of this application.
"""
from setuptools import setup, find_packages


# The setup util makes it possible to more comfortable build
# and distribute python packages. You can find more information here:
# https://setuptools.readthedocs.io/en/latest/setuptools.html

# Following statements are represent the brief description:
# 1) name - sets the project name.
# 2) version - sets the project version
# 3) description - this is the short description of your project.
# 4) author - Author name/nickname
# 5) author_email - Author contact e-mail.
# 6) packages - all packages used in the project. Apparently, find packages - looking for them. More information here:
#    https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
# 7) zip_safe - For some use cases, Python packages may be run directly from a zip file. More information here:
#    https://setuptools.readthedocs.io/en/latest/setuptools.html#setting-the-zip-safe-flag
# 9) entry_points - sets the entry point of the whole application.
# 9.1) console_scripts - means that you can write the 'start_app' instead of the 'python3 entry_py'
#      and the application starts


setup(
    name="kitty_getter",
    version="1.0.0",

    install_requires=[
        "docutils>=0.3",
        "aiohttp>=3.6.2",
        "aiohttp-jinja2>=1.2.0",
        "aiohttp-session == 2.9.0",
        "aiohttp-sse>=2.0.0",
        "astroid>=2.3.3",
        "async-timeout>=3.0.1",
        "asyncpg>=0.20.1"
        "asyncpgsa>=0.26.1",
        "atomicwrites>=1.3.0",
        "attrs>=19.3.0",
        "cchardet>=2.1.5",
        "certifi>=2019.11.28",
        "cffi>=1.14.0",
        "chardet>=3.0.4",
        "click>=7.1.2",
        "colorama>=0.4.3",
        "cryptography>=2.9",
        "decorator>=4.4.2",
        "idna>=2.8",
        "interrogate>=1.1.2",
        "isort>=4.3.21",
        "Jinja2>=2.11.1",
        "lazy-object-proxy>=1.4.3",
        "MarkupSafe>=1.1.1",
        "mccabe>=0.6.1",
        "more-itertools>=8.2.0",
        "multidict>=4.7.5",
        "networkx>=2.4",
        "packaging>=20.1",
        "Pillow>=7.1.1",
        "pipenv>=2018.11.26",
        "pluggy>=0.13.1",
        "py>=1.8.1",
        "pycparser>=2.20",
        "pyjsparser>=2.7.1",
        "pylint>=2.4.4",
        "pyparsing>=2.4.6",
        "pytz>=2019.3",
        "PyYAML>=5.3.1",
        "requests>=2.22.0",
        "six>=1.14.0",
        "SQLAlchemy>=1.3.16",
        "tabulate>=0.8.7",
        "toml>=0.10.0",
        "tzlocal>=2.0.0",
        "urllib3>=1.25.8",
        "virtualenv>=16.7.9",
        "virtualenv-clone>=0.5.3",
        "wcwidth>=0.1.8",
        "wrapt>=1.11.2",
        "yarl>=1.4.2"],

    description="The Queue Management System which shows kitties images according queue order.",
    author="Aleksandr Kasian",
    author_email="aleksandr.juicefv@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    # Uncomment this of you don't use the MANIFEST.in
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
