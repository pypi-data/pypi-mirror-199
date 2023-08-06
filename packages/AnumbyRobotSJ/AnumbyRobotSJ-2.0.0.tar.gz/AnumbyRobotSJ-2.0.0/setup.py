import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setup(
    name = "AnumbyRobotSJ",
    version = "2.0.0",
    description = "Software du Robot Anumby pour le Service Jeunesse de Bures sur Yvette ",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/anumby-source/RobotServiceJeunesse2023/tree/main/MasterMind",
    author = "Chris Arnault",
    author_email = "chris.arnault@gmail.com",
    license = "MIT License",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    packages = ["MasterMind"],
    include_package_data = True,
    install_requires = [
        "Pillow == 9.1.0",
        "opencv-python >= 4.7.0",
        "tensorflow >= 2.11.0",
        "keras >= 2.11.0"
    ],
    entry_points = {
        "console_scripts": ["MasterMind = MasterMind:__main__.main"]
    },
)
