from setuptools import setup

setup(
    name="strapper",
    version="0.0.0",
    author="André Bienemann",
    author_email="andre.bienemann@gmail.com",
    install_requires=[],
    packages=["strapper", "strapper/commands"],
    entry_points={"console_scripts": ["strapper=strapper:main"]},
)
