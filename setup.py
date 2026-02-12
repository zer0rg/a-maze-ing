#!/usr/bin/env python3
"""Setup script for A-Maze-Ing package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="a-maze-ing",
    version="1.0.0",
    author="amarcill, rgerman-",
    description="A maze generator and solver using DFS algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["a_maze_ing"],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "a-maze-ing=a_maze_ing:main",
        ],
    },
)
