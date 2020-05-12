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
    name="Kitty Getter",
    version="1.0",
    description="The Queue Management System which shows kitties images according queue order.",
    author="Aleksandr Kasian",
    author_email="aleksandr.juicefv@gmail.com",
    packages=find_packages(),
    zip_safe=True,
    entry_points={
        'console_scripts':
            ['start_app = ..entry.py']
    }
)
