import pathlib

from PIL import Image
from PIL.Image import Resampling

from src.Helpers.error_handler import ErrorHandler


class PillowProvider:

    @staticmethod
    def convert_image(path: str, output_path: str, img_format: str, img_resolution: str, ratio: bool) -> bool:
        try:
            if not path or not output_path or not img_format or not img_resolution:
                raise ValueError("Invalid arguments for image conversion")
            image = Image.open(path)
            image_width = int(img_resolution.split("x")[0])
            image_height = int(img_resolution.split("x")[1])
            file_name = pathlib.Path(path).stem
            final_output = f"{pathlib.Path(output_path).joinpath(file_name)}.{img_format.lower()}"
            pathlib.Path(final_output).parent.mkdir(parents=True, exist_ok=True)
            if ratio:
                image.thumbnail(size=(image_width, image_height), resample=Resampling.LANCZOS)
            else:
                image = image.resize(size=(image_width, image_height), resample=Resampling.LANCZOS)
            if img_format.upper() == "JPEG" and image.mode in ("RGBA", "LA"):
                image = image.convert("RGB")
            image.save(final_output, format=img_format)
            return True
        except Exception as e:
            ErrorHandler.write_log_exception(PillowProvider.__class__.__name__, e)
            return False