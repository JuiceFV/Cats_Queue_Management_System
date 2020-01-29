from setuptools import setup, find_packages

setup(
    name="Kitty Getter",
    version="1.0",
    packages=find_packages(),
    zip_safe=True,
    entry_points={
        'console_scripts':
            ['start_app = entry.py']
    }
)