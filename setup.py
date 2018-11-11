from setuptools import setup

setup(
    name="pubg",
    version=0.1,
    author="Adrienne Karnoski",
    author_email="adrienne.j.karnoski@gmail.com",
    license='MIT',
    py_modules=['pubg, inactive_api_pubg, practice_data'],
    package_dir={'': 'src'},
    install_requires=[],
    extras_require={'test': ['pytest', 'pytest-watch']},
    )
