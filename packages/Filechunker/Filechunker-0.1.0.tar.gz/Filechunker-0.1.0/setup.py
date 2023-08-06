from setuptools import setup, find_packages

setup(
    name="Filechunker",
    version="0.1.0",
    author="Rohaan Ahmed",
    author_email="silent.death3500@gmail.com",
    description="A utility for chunking large files into smaller ones.",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "SQLAlchemy",
        "concurrent",
        "sys",
        "time",
        "uuid",
        "os",
        "hashlib",
        "threading",
        "pathlib",
        "threading",
        "timeit",
        "asyncio",
        "multiprocessing",
        "queue",
        "enum",
    ],
)
