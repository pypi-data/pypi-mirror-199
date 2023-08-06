import setuptools

with open("../README.md", "r") as README:
    long_description = README.read()

setuptools.setup(
    name="je_web_runner",
    version="0.0.35",
    author="JE-Chen",
    author_email="zenmailman@gmail.com",
    description="selenium get_webdriver_wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JE-Chen/WebRunner",
    packages=setuptools.find_packages(),
    install_requires=[
        "selenium>=4.0.0",
        'requests',
        'python-dotenv'
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

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
