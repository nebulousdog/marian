import setuptools
from marian.version import __version__

with open('README.rst', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='marian',
    version=__version__,
    author='Tom Spalding',
    author_email='tom@blackforestbotanics.com',
    description='a Robinhood API server built on Fast Arrow.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    url='https://github.com/nebulousdog/marian',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    entry_points={
        'console_scripts': [
            'marian=marian.cli:cli',
        ],
    },
)
