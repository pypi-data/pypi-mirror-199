from setuptools import setup

setup(
    name="pytest-file-watcher",
    version="0.2.4",
    description="Pytest-File-Watcher is a CLI tool that watches for changes in your code and runs pytest on the changed files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Deviljin112",
    url="https://github.com/deviljin112/Pytest-File-Watcher",
    license="MIT",
    keywords="python pytest testing testing-tools watch watcher",
    packages=["src"],
    install_requires=[
        "PyYAML==6.0",
        "watchfiles==0.18.1",
        "typer==0.7.0",
        "rich==12.6.0",
        "pytest",
    ],
    entry_points={"console_scripts": ["pytest-w=src.main:cli"]},
    setup_requires=["pytest-runner", "flake8"],
    tests_require=["pytest"],
    python_requires=">=3.9",
)
