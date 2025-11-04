"""
Setup script for Delta Exchange Python Client
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="delta-exchange-python",
    version="0.1.0",
    author="Delta Exchange Python Client Contributors",
    author_email="",
    description="Professional Python client library for Delta Exchange API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuldeepakkatwal/Delta_client",
    project_urls={
        "Bug Reports": "https://github.com/kuldeepakkatwal/Delta_client/issues",
        "Source": "https://github.com/kuldeepakkatwal/Delta_client",
        "Documentation": "https://docs.delta.exchange",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    keywords="delta exchange trading cryptocurrency futures api client",
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "websockets>=12.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-mock>=3.10.0",
            "responses>=0.23.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
        "pydantic": [
            "pydantic>=2.0.0",
        ],
    },
    package_data={
        "delta_exchange": ["py.typed"],
    },
    zip_safe=False,
)

