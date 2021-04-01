from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

tests_require = ['pytest', 'mypy', 'pycodestyle', 'data-science-types']

extras_require = {
    'test': tests_require,
    'doc': ['sphinx', 'sphinx_rtd_theme'],
}

packages = find_packages(exclude=['tests'])


setup(
    name="pyschilog",
    version="0.1.2",
    author="Gijs Molenaar",
    author_email="gijs@pythonic.nl",
    description="the Python scientific logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gijzelaerr/pyscilog/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.6',
    extras_require=extras_require,
    install_requires=['psutil',
                      'dataclasses'],
    tests_require=tests_require,
    test_suite="tests",
)
