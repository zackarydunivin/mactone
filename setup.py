from setuptools import setup, find_packages

setup(
    name="mactone",
    version="0.1.0",
    description="Play macOS system alert tones from Python",
    author="Zackary Okun Dunivin",
    packages=find_packages(),
    install_requires=["pydub"],
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "License :: OSI Approved :: MIT License",
    ],
)