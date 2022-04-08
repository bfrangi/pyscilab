from setuptools import setup, find_packages

__version__ = "1.0.7.dev1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyscilab',
    version=__version__,
    author="Bernat Frangi",
    author_email='bernat.frangi@gmail.com',
    description='Package including useful methods to process data from laboratory experiments',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bfrangi/pyscilab.git',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
    ],
    python_requires='>=3',
    keywords='laboratory utility latex',
    license='GNU General Public License v3.0',
    project_urls={
        'Source': 'https://github.com/bfrangi/pyscilab',
    },
)