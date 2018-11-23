from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name="pubg",
    version=0.1,
    author="Adrienne Karnoski",
    author_email="adrienne.j.karnoski@gmail.com",
    license='MIT',
    py_modules=['pubg, inactive_api_pubg, mock_api_response'],
    package_dir={'': 'src'},
    install_requires=install_requires,
    extras_require={'test': ['pytest', 'pytest-watch']},
    )
