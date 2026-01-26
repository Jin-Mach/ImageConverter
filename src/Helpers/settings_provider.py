import json
import pathlib

from src.Helpers.error_handler import ErrorHandler


class SettingsProvider:

    DEFAULT_PATH = pathlib.Path.home()
    USER_SETTINGS_PATH = pathlib.Path(__file__).parents[2].joinpath("config")
    KEYS_LIST = ["input_path", "output_path", "format_value", "resolution_value"]

    DEFAULT_SETTINGS = {
        "input_path": DEFAULT_PATH,
        "output_path": DEFAULT_PATH,
        "format_list": ["BMP", "GIF", "JPEG", "PNG", "TIFF", "WebP"],
        "format_value": "JPEG",
        "resolution_list": [[320, 240], [640, 480], [800, 600], [1024, 768], [1280, 720], [1366, 768], [1600, 900],
                            [1920, 1080], [2560, 1440], [3840, 2160]],
        "resolution_value": [1920, 1080],
        "ratio": True,
    }

    USER_SETTINGS = {
        "input_path": DEFAULT_PATH,
        "output_path": DEFAULT_PATH,
        "format_value": "JPEG",
        "resolution_value": [1920, 1080],
    }

    @staticmethod
    def initialize_settings() -> bool:
        try:
            SettingsProvider.USER_SETTINGS_PATH.mkdir(parents=True, exist_ok=True)
            user_settings_file = SettingsProvider.USER_SETTINGS_PATH.joinpath("settings.json")
            if not user_settings_file.exists() or user_settings_file.stat().st_size == 0:
                with open(user_settings_file, "w", encoding="utf-8") as file:
                    json.dump(SettingsProvider.USER_SETTINGS, file, indent=4, sort_keys=True)
            else:
                with open(user_settings_file, "r+", encoding="utf-8") as file:
                    json_settings = json.load(file)
                    for key in SettingsProvider.KEYS_LIST:
                        json_settings.setdefault(key, "")
                    for key, value in json_settings.items():
                        if value == "" or value == []:
                            json_settings[key] = SettingsProvider.DEFAULT_SETTINGS[key]
                    file.seek(0)
                    json.dump(json_settings, file, indent=4, sort_keys=True)
                    file.truncate()
            return True
        except Exception as e:
            ErrorHandler.write_log_exception(SettingsProvider.__name__, e)
            return False
