from setuptools import find_packages, setup

setup(
    name="data-driven-stock-portfolio-selection",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
