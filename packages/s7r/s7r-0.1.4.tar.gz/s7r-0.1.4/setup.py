import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="s7r",
    author="Henry Jones",
    author_email="henryivesjones@gmail.com",
    url="https://github.com/henryivesjones/sprinkler",
    description="An easy to use job runner.",
    packages=["sprinkler", "sprinkler.db_interfaces", "sprinkler.targets"],
    package_dir={
        "sprinkler": "sprinkler",
        "sprinkler.db_interfaces": "sprinkler/db_interfaces",
        "sprinkler.targets": "sprinkler/targets",
    },
    package_data={
        "": [".build/**"],
        "sprinkler": [
            "py.typed",
        ],
        "sprinkler.db_interfaces": ["py.typed"],
        "sprinkler.targets": ["py.typed"],
    },
    include_package_data=True,
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
    ],
)
