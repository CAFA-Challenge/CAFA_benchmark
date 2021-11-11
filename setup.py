import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CAFABench",
    version="1.0.11",
    author="Iddo Friedberg Lab",
    author_email="parnal@iastate.edu",
    description="A program to generate benchmark for the CAFA challenge",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/CAFA-Challenge/CAFA_benchmark",
    packages=setuptools.find_packages(),
    # packages=["lib\create_benchmark"],
    test_suite="tests.test_create_benchmark",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "CAFABench=CAFABench.create_benchmark:main",
        ],
    },
)
