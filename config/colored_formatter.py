import logging
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt=None):
        super().__init__(fmt, datefmt)
        self.FORMATS = {
            logging.DEBUG: Fore.CYAN + fmt + Style.RESET_ALL,
            logging.INFO: Fore.GREEN + fmt + Style.RESET_ALL,
            logging.WARNING: Fore.YELLOW + fmt + Style.RESET_ALL,
            logging.ERROR: Fore.RED + fmt + Style.RESET_ALL,
            logging.CRITICAL: Fore.RED + Style.BRIGHT + fmt + Style.RESET_ALL,
        }


    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.datefmt)
        return formatter.format(record)