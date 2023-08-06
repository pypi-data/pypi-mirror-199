from setuptools import find_packages, setup

with open("app/Readme.md", "r") as f:
    long_description = f.read()

setup(
    name="radargeocoder",
    version="0.0.10",
    description="Python functions for geocoding addresses using the Radar API",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdventistVirtual/radargeocoder",
    author="Adventist Virtual",
    author_email="<devsupport@adventistvirtual.com>",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas', 'radar-python'],
    python_requires=">=3.10",
)