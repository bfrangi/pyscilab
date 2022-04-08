from setuptools import setup, find_packages

__version__ = "1.0.5.dev1"

setup(
    name='pyscilab',
    version=__version__,
    description='Package including useful methods to process data from laboratory experiments',
    url='https://github.com/bfrangi/pyscilab.git',
    author="Bernat Frangi",
    author_email='bernat.frangi@gmail.com',
    license='GNU General Public License v3.0',
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
    keywords='laboratory utility latex',
    project_urls={
        'Source': 'https://github.com/bfrangi/pyscilab',
    },
    python_requires='>=3',
    package_dir={"pyscilab": "src/pyscilab"},
    packages=[
        'pyscilab',
    ],
)