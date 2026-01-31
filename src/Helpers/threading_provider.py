from PyQt6.QtCore import QThread

from src.Helpers.convert_object import ConvertObject
from src.Helpers.error_handler import ErrorHandler


class ThreadingProvider:
    def __init__(self, paths_list: list[str], output_path: str, img_format: str, img_resolution: str, ratio: bool) -> None:
        self.paths_list = paths_list
        self.paths_list = paths_list
        self.output_path = output_path
        self.img_format = img_format
        self.img_resolution = img_resolution
        self.ratio = ratio
        self.convert_thread = QThread()
        self.convert_object = ConvertObject(self.paths_list, self.output_path, self.img_format, self.img_resolution,
                                            self.ratio)
        self.convert_object.moveToThread(self.convert_thread)

    def start_conversion(self):
        try:
            self.convert_thread.started.connect(self.convert_object.start_conversion)
            self.convert_object.convert_success.connect(self.convert_thread.quit)
            self.convert_object.convert_failed.connect(self.convert_thread.quit)
            self.convert_thread.finished.connect(self.convert_thread.deleteLater)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e)