import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-json-config-parser",
    version="1.0.7",
    author="Bruno Silva de Andrade",
    author_email="brunojf.andrade@gmail.com",
    description="Project created to given the possibility of create dynamics Json config files",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BrunoSilvaAndrade/python-json-config-parser",
    py_modules=["jsonconfigparser"],
    install_requires=open("requirements.txt", "r").read().split("\n"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)