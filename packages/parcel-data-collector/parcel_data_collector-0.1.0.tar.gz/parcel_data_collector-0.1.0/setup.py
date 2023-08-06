from setuptools import setup, find_packages

setup(
    name="parcel_data_collector",
    version="0.1.0",
    author="Philip Diegel",
    author_email="philipdiegel@gmail.com",
    description="A package for collecting and analyzing data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pdiegel/Parcel-Data-Collector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=open("requirements.txt").readlines(),
)
