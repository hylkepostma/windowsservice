from setuptools import setup

setup(
    name="windowsservice",
    version="0.1.0",
    description="A Python package for building Windows services.",
    url="https://github.com/hylkepostma/windowsservice",
    author="Hylke Postma",
    author_email="info@hylkeposta.nl",
    license="MIT",
        classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="python windows service pywin32 multiprocessing pyinstaller windowsservice",
    install_requires=[
        "pywin32",
    ],
    packages=["windowsservice"],
    zip_safe=False,
)
