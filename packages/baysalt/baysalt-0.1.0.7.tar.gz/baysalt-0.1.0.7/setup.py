import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="baysalt",
    version="0.1.0.7",
    author="Christmas, Dovelet, Qidi Ma",
    author_email="273519355@qq.com",
    description="Some simple tools for baysalt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'netCDF4',
        'scipy',
        'baysalt_christmas',
    ],
)
# python3 setup.py sdist bdist_wheel
# twine upload dist/*
