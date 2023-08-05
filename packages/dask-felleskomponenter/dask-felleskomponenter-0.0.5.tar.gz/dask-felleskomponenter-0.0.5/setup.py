import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "dask-felleskomponenter",
    version = "0.0.5",
    author = "Dataplattform@Statens Kartverk",
    author_email = "dataplattform@kartverket.no",
    description = "Felleskomponeneter for utvikling av Apache Beam pipelines",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kartverket/dask-felleskomponenter",
    project_urls = {
        "Bug Tracker": "https://github.com/kartverket/dask-felleskomponenter/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.7"
)
