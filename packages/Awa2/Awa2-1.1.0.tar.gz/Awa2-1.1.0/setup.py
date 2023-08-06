
from setuptools import find_packages, setup


setup(
    name="Awa2",
    version="1.1.0",
    author="XiangQinxi",
    description="Simple Setup",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3",
    packages=find_packages(where='.'),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
        