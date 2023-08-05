import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mostpopular-News-Kompas.com",
    version="0.0.5",
    author="Deni Rahmawan",
    author_email="dapatheia@gmail.com",
    description="This package will get the Mostpopular News From Kompas.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Apatheia8/Mostpopular-News-Kompas.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    package=setuptools.find_packages(),
    python_requires='>=3.6',
)
