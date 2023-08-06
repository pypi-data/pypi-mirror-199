import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brighterflame",
    version="0.0.0",
    author="Dario Balboni",
    author_email="dario.balboni.96@gmail.com",
    description="Speed up your deep pytorch models with sound optimization procedures!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dbalboni/brighterflame",
    packages=["brighterflame"],
    zip_safe=False,
    keywords="pytorch optimization deep-learning",
    install_requires=[
        "torch",
    ],
    include_package_data=True,
    license="PROPRIETARY",
    python_requires=">=3.9",
    classifiers=[
        "License :: Other/Proprietary License",
    ],
)
