import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alarm-clock-pkg-ap910-exeter",
    version="0.0.1",
    author="Adarsh Prusty",
    author_email="ap910@exeter.ac.uk",
    description="A smart alarm programmed for ECM1400's CA3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)