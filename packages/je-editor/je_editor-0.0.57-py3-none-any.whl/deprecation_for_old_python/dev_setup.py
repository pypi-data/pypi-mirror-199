import setuptools

with open("../README.md", "r") as README:
    long_description = README.read()

setuptools.setup(
    name="je_editor_dev",
    version="0.0.51",
    author="JE-Chen",
    author_email="zenmailman@gmail.com",
    description="simple editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JE-Chen/je_editor",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)

# python dev_setup.py sdist bdist_wheel
# python -m twine upload dist/*
