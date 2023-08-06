from setuptools import setup

setup(
    name="county_property_data",
    version="0.1",
    author="Philip Diegel",
    py_modules=["county_property_data"],
    install_requires=["requests", "beautifulsoup4"],
    description="A Python module for collecting property data by county.",
)
