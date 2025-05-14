from setuptools import find_packages, setup

setup(
    name = "MedCare Chatbot Project",
    version = "0.0.0",
    author = "Muhammad Furqan Rauf",
    author_email = "furqanrauf11@gmail.com",
    description = "A chatbot for medical care",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires = [

    ]
)