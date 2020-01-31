from setuptools import setup, find_packages

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
            ['start_app = entry.py']
    }
)
