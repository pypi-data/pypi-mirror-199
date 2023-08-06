from setuptools import setup

setup(
    name="samantha",
    version="0.0.0",
    author="André Bienemann",
    author_email="andre.bienemann@gmail.com",
    install_requires=[],
    packages=["samantha", "samantha/commands"],
    entry_points={"console_scripts": ["samantha=samantha:main"]},
)
