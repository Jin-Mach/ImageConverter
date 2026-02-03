# ImageConverter

A Python image conversion application built with PyQt6 and Pillow.  
ImageConverter allows you to select multiple images, convert them to different formats, optionally resize them, and save the output to a chosen folder.

## Features

- Select images to convert using the "Select" button or add to the current list with "Add".
- Supported formats and default settings configurable in the Settings dialog.
- Choose output folder for converted images.
- Set target format and resolution.
- Maintain aspect ratio if desired.
- Convert images and view progress with a dialog showing conversion status.
- Clear the list of selected images entirely or remove individual items.
- Application remembers default input/output paths, format, and resolution settings.

## Installation

(Tested on macOS and Windows, IDE: PyCharm)

- Clone the repository:
git clone https://github.com/jindrichmachytka/ImageConverter.git

- Navigate to the project directory:
cd ImageConverter

- Create a virtual environment:
  - On Windows:
python -m venv .venv
  - On macOS/Linux:
python3 -m venv .venv

- Activate the virtual environment:
  - On Windows (Command Prompt):
.venv\Scripts\activate
  - On Windows (PowerShell):
.venv\Scripts\activate.ps1
  - On macOS/Linux:
source .venv/bin/activate

- Install required packages:
pip install -r requirements.txt

## Usage

After installing dependencies, run the application:

- On Windows:
python image_converter.py
- On macOS/Linux:
python3 image_converter.py

## License

MIT License

## Credits

Developed by Jin-Mach

## Contact

Questions or feedback? Reach out via GitHub: https://github.com/Jin-Mach