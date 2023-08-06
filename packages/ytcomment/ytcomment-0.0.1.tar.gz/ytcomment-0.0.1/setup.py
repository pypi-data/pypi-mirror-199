from setuptools import find_packages, setup

with open("app/Readme.md", "r") as f:
    long_description = f.read()

setup(
    name="ytcomment",
    version="0.0.1",
    description="ytcomment scrap all comments and title given a  youtube url.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azerinho007/",
    author="Azer",
    author_email="azerch.1996@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=["google-api-python-client>=2.81.0"],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.7",
)