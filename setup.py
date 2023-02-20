# installation script for the module

from distutils.core import setup


with open("VERSION", "r") as f:
    version = f.read().strip()

setup(
    name="plinx",
    version=version,
    description="Plinx is an experimental, minimalistic, and extensible web framework and ORM written in Python.",
    author="Dhaval Savalia",
    author_email="coder@dhavalsavalia.com",
    url="https://github.com/dhavalsavalia/plinx",
    packages=["plinx"],
)
