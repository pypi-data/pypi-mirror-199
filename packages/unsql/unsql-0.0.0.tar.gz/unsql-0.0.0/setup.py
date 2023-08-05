import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unsql",
    version="0.0.0",
    author="Madhup Sukoon",
    author_email="vagrantism@outlook.in",
    description="UnStructured Query Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vagrantism/unsql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)