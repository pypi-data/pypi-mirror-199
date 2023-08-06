from setuptools import setup, find_packages

setup(
    name="Mani175",
    version="1.7.5",
    install_requires=[],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5",
)