from setuptools import setup, find_packages

def read_me() -> str:
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

setup(
    name="ImageConverter",
    version="0.1.0",
    author="PP",
    author_email="Ji82Ma@seznam.cz",
    description="Simply image converter for my work buddy PP :-)",
    long_description=read_me(),
    long_description_content_type="text/markdown",
    url="https://github.com/jindrichmachytka/ImageConverter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt6>=6.10",
        "pywin32; sys_platform=='win32'",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    entry_points={
        "console_scripts": [
            "image_converter=image_converter:create_app",
        ],
    },
    keywords="image_converter, pyqt6",
)