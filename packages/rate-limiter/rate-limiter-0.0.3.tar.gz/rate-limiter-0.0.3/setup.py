from setuptools import setup
from setuptools import find_packages

setup(
    name="rate-limiter",
    version="0.0.3",
    description="A rate limiter which can use any backend",
    url="https://github.com/shuttl-tech/rate-limiter",
    author="Sherub Thakur",
    author_email="sherub.thakur@shuttl.com",
    license="MIT",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=["redis"],
    extras_require={
        "test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8", "flask"]
    },
)
