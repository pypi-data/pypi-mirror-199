from setuptools import setup, find_packages

setup(
    name="texonomy", include_package_data=True, package_data={'': ['templates/template.tex']}, packages=find_packages()
)
