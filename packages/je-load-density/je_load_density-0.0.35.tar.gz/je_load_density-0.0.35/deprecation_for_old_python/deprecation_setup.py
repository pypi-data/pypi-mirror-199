import setuptools

with open("../README.md", "r") as README:
    long_description = README.read()

setuptools.setup(
    name="je_load_density",
    version="0.0.33",
    author="JE-Chen",
    author_email="zenmailman@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JE-Chen/LoadTesting",
    packages=setuptools.find_packages(),
    install_requires=[
        "locust"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
