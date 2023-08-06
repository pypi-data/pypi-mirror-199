from setuptools import find_packages, setup

base_packages = ["clumper", "numpy", "pandas", "typer"]
dev_packages = ["flake8", "pytest", "jupyter", "jupyterlab"]

setup(
    name="zep2md",
    version="0.1.3",
    packages=find_packages(exclude=["notebooks"]),
    install_requires=base_packages,
    entry_points={
        "console_scripts": [
            "zep2md = zep2md.__main__:app",
        ],
    },
    extras_require={"dev": dev_packages},
)
