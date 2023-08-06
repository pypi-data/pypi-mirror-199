# This file is placed in the Public Domain.


"object programming version"


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="opv",
    version="10",
    author="B.H.J. Thate",
    author_email="operbot100@gmail.com",
    url="http://github.com/operbot/opv",
    zip_safe=True,
    description="object programming version",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["opv"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
