import sys
from setuptools import setup, find_packages

versions = dict(numpy='1.20.3',
                scipy='1.7.3',
                pandas='1.4.0',
                ftfy='6.0.3',
                pyreadstat='1.1.4')

precisions = dict(numpy='==',
                  scipy='==',
                  pandas='==',
                  ftfy='==',
                  pyreadstat='==')

libs = ['numpy',
        'scipy',
        'pandas',
        'ftfy',
        'xmltodict',
        'lxml',
        'xlsxwriter',
        # 'pillow',
        'prettytable',
        'decorator',
        # 'watchdog',
        'requests',
        'python-pptx',
        'pyreadstat',
        'daal']


def version_libs(libs, precisions, versions):
    return [lib + precisions[lib] + versions[lib]
            if lib in versions.keys() else lib
            for lib in libs]


if sys.platform == 'win32':
    INSTALL_REQUIRES = version_libs(libs[2:], precisions, versions)
else:
    INSTALL_REQUIRES = version_libs(libs, precisions, versions)

setup(
    name="qudo-quantipy",
    version="0.1.1",
    author="Constance Maurer",
    description="A reduced and adapted version of quantipy3 package by author Geir Freysson.",
    packages=find_packages(exclude=['tests']),
    install_requires=INSTALL_REQUIRES,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
