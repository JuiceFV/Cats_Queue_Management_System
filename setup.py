import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='showkitty',
    py_modules=['showkitty'],
    entry_points={
            'console_scripts':
                ['start_app = showkitty']
            }
)
