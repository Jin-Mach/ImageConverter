from src.Helpers.dialogs_provider import DialogsProvider
from src.Helpers.logger_provider import get_logger


class ErrorHandler:
    class_name = "errorHandler"
    logger = get_logger()

    @staticmethod
    def exception_handler(class_name: str, exception: Exception, ui_texts=None, parent=None) -> None:
        try:
            ErrorHandler.write_log_exception(class_name=class_name, exception=exception)
            DialogsProvider.get_error_dialog(error_message=str(exception), ui_texts=ui_texts, parent=parent)
        except Exception as e:
            ErrorHandler.write_log_exception(class_name=class_name, exception=e)

    @staticmethod
    def write_log_exception(class_name: str, exception: Exception) -> None:
        ErrorHandler.logger.error(f"{class_name}: {exception}", exc_info=True)