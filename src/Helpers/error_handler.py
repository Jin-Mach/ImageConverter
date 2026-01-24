from src.Helpers.dialogs_provider import DialogsProvider
from src.Helpers.logger_provider import get_logger


class ErrorHandler:
    class_name = "errorHandler"
    logger = get_logger()

    @staticmethod
    def write_log_exception(class_name: str, exception: Exception, parent=None) -> None:
        ErrorHandler.logger.error(f"{class_name}: {exception}", exc_info=True)
        DialogsProvider.get_error_dialog(error_message=str(exception), parent=parent)