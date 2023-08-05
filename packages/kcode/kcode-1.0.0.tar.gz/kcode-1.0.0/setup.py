from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name="kcode",
    version="1.0.0",
    packages=find_packages(),
    author="Pavel Frolov",
    author_email="pfrol007@gmail.com",
    description="King-code package",
    long_description_content_type="text/markdown",
    long_description=open(join(dirname(__file__), "README.md")).read(),
    url="https://github.com/frolpaxa/kcode",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
