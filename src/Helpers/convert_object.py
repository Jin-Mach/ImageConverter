from PyQt6.QtCore import QObject, pyqtSignal

from src.Helpers.pillow_provider import PillowProvider
from src.Helpers.error_handler import ErrorHandler


class ConvertObject(QObject):
    convert_success = pyqtSignal()
    convert_failed = pyqtSignal()
    convert_progress = pyqtSignal(str)
    convert_failed_list = pyqtSignal(list[str])

    def __init__(self, paths_list: list[str], output_path: str, img_format: str, img_resolution: str, ratio: bool) -> None:
        super().__init__()
        self.setObjectName("convertObject")
        self.paths_list = paths_list
        self.output_path = output_path
        self.img_format = img_format
        self.img_resolution = img_resolution
        self.ratio = ratio

    def start_conversion(self):
        try:
            paths_count = len(self.paths_list)
            progress = 1
            failed_list = []
            for path in self.paths_list:
                self.convert_progress.emit(f"{progress} / {paths_count}")
                progress += 1
                if not PillowProvider.convert_image(path, self.output_path, self.img_format, self.img_resolution,
                                                    self.ratio):
                    failed_list.append(path)
                    continue
            self.convert_failed_list.emit(failed_list)
            self.convert_success.emit()
        except Exception as e:
            ErrorHandler.write_log_exception(self.__class__.__name__, e)
            self.convert_failed.emit()