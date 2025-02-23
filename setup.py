from setuptools import setup, find_packages

setup(
    name="termai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "pydantic",
        "google-generativeai",
        "python-dotenv",
        "langchain-google-genai"
    ],
    entry_points={
        "console_scripts": [
            "termai=termai.cli:app",  # Updated to use the package structure
        ],
    },
    author="Your Name",
    description="AI-powered CLI for generating shell commands",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)