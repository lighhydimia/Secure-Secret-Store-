from setuptools import setup, find_packages

setup(
    name="secure-secret-store",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "secret-store=secure_secret_store.cli:main",
        ]
    },
    install_requires=[
        "cryptography>=39.0.0",
        "click>=8.0.0"
    ]
)
