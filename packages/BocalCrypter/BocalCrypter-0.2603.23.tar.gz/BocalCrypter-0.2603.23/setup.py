import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BocalCrypter",
    version="0.2603.23",
    author="JuanDiegoTorresInfante",
    author_email="juandiegotorres35@gmail.com",
    description="Easy encrypt of any data.",
    long_description=long_description,
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)