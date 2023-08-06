import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zintor",                             # This is the name of the package
    version="0.0.15",                        # The initial release version
    author="__Async__",                     # Full name of the author
    description="Python Admin Package",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    py_modules=["zintor"],                     # Name of the python package
    package_dir={'':'zintor/src'},          # Directory of the source code of the package
    install_requires=[
        'Flask',
        'Flask-Admin>=1.6',
        'flask_login',
        'Flask-BabelEx',
        'MarkupSafe>=2',
        'WTForms>=3',
    ]                                       # Install other dependencies if any
)
