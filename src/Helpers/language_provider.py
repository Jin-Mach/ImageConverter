import json
import pathlib

from PyQt6.QtCore import QLocale

from src.Helpers.error_handler import ErrorHandler


class LanguageProvider:
    class_name = "languageProvider"
    ui_texts_path = pathlib.Path(__file__).parents[2].joinpath("resources", "ui_texts")
    default_language = "en_GB"
    language_code = QLocale().name() or default_language

    @staticmethod
    def get_ui_texts(class_name: str) -> dict[str, str] | None:
        try:
            code = LanguageProvider.language_code
            file_path = LanguageProvider.ui_texts_path / f"{code}.json"

            if not file_path.exists():
                file_path = LanguageProvider.ui_texts_path / f"{LanguageProvider.default_language}.json"

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Text file not found for {code} or fallback {LanguageProvider.default_language}")

            with open(file=file_path, mode="r", encoding="utf-8") as file:
                json_text = json.load(file)
            return json_text.get(class_name, {})
        except Exception as e:
            ErrorHandler.write_log_exception(class_name=class_name, exception=e)
            return None