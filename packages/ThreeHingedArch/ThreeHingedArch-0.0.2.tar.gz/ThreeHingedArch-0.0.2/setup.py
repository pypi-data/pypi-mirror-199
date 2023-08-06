import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="ThreeHingedArch",
    version="0.0.2",
    author="giboul",
    author_email="axel.giboulot@epfl.ch",
    packages=["ThreeHingedArch"],
    description="Static analysis of three heinged arches",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/giboul/ThreeHingeArch",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)
