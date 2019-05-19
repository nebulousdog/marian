import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="marian",
    version="0.0.1",
    author="Tom Spalding",
    author_email="tom@catcobralizard.com",
    description="a personal Robinhood API server",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    url="https://github.com/nebulousdog/marian",
    license='MIT',
    classifiers=[
        "Framework :: Flask",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)