import json
import pathlib

from src.Helpers.error_handler import ErrorHandler


class SettingsProvider:

    DEFAULT_PATH = pathlib.Path.home()
    CONFIG_DIR = pathlib.Path(__file__).parents[2].joinpath("config")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    USER_SETTINGS_PATH = CONFIG_DIR.joinpath("settings.json")
    KEYS_LIST = ["input_path", "output_path", "format_value", "resolution_value"]

    DEFAULT_SETTINGS = {
        "input_path": str(DEFAULT_PATH),
        "output_path": str(DEFAULT_PATH),
        "format_list": ["BMP", "GIF", "JPEG", "PNG", "TIFF", "WebP"],
        "format_value": "JPEG",
        "resolution_list": [[320, 240], [640, 480], [800, 600], [1024, 768], [1280, 720], [1366, 768], [1600, 900],
                            [1920, 1080], [2560, 1440], [3840, 2160]],
        "resolution_value": [1920, 1080],
        "ratio": True,
    }

    USER_SETTINGS = {
        "input_path": str(DEFAULT_PATH),
        "output_path": str(DEFAULT_PATH),
        "format_value": "JPEG",
        "resolution_value": [1920, 1080],
    }

    @staticmethod
    def initialize_settings() -> bool:
        try:
            if not SettingsProvider.USER_SETTINGS_PATH.exists() or SettingsProvider.USER_SETTINGS_PATH.stat().st_size == 0:
                with open(SettingsProvider.USER_SETTINGS_PATH, "w", encoding="utf-8") as file:
                    json.dump(SettingsProvider.USER_SETTINGS, file, indent=4, sort_keys=True)
            else:
                with open(SettingsProvider.USER_SETTINGS_PATH, "r+", encoding="utf-8") as file:
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

    @staticmethod
    def get_settings_data() -> dict[str, dict[str, str | list[str] | list[list[int]] | list[int]]]:
        settings_data = {
            "default": SettingsProvider.DEFAULT_SETTINGS.copy(),
            "user": {}
        }
        try:
            with open(SettingsProvider.USER_SETTINGS_PATH, "r", encoding="utf-8") as file:
                json_settings = json.load(file)
                if not json_settings:
                    json_settings = SettingsProvider.USER_SETTINGS.copy()
                settings_data["user"] = json_settings
        except Exception as e:
            ErrorHandler.write_log_exception(SettingsProvider.__name__, e)
            settings_data["user"] = SettingsProvider.USER_SETTINGS.copy()
        return settings_data