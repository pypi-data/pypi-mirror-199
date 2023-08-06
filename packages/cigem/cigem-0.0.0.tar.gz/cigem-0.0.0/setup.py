from setuptools import setup

setup(
    name="cigem",
    version="0.0.0",
    author="André Bienemann",
    author_email="andre.bienemann@gmail.com",
    install_requires=["click"],
    packages=["cigem", "cigem/commands"],
    entry_points={"console_scripts": ["cigem=cigem:main"]},
)
