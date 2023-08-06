from colorama import *

init()

class Logs:
    _string: str

    def __init__(self, string: str) -> None:
        self._string = string

    def __str__(self) -> str:
        return f'string: {self.get_string()}'

    def __eq__(self, __other: object) -> bool:
        if self is __other:
            return True
        if not isinstance(__other, Logs):
            return False
        return self._string == __other._string

    def __hash__(self) -> int:
        return hash(self._string)

    @property
    def get_string(self) -> str:
        return self._string

    @property
    def set_string(self, value: str) -> None:
        self._string = value

    @staticmethod
    def success_log(text: str, tag: str = '') -> str:
        if tag:
            tag = Fore.GREEN + tag + Style.RESET_ALL
            text = Fore.WHITE + text + Style.RESET_ALL
            return f'[{tag}] {text}'
        else:
            text = Fore.GREEN + text + Style.RESET_ALL
            return f'{text}'

    @staticmethod
    def warning_log(text: str, tag: str = '') -> str:
        if tag:
            tag = Fore.YELLOW + tag + Style.RESET_ALL
            text = Fore.WHITE + text + Style.RESET_ALL
            return f'[{tag}] {text}'
        else:
            text = Fore.YELLOW + text + Style.RESET_ALL
            return f'{text}'

    @staticmethod
    def error_log(text: str, tag: str = '') -> str:
        if tag:
            tag = Fore.RED + tag + Style.RESET_ALL
            text = Fore.WHITE + text + Style.RESET_ALL
            return f'[{tag}] {text}'
        else:
            text = Fore.RED + text + Style.RESET_ALL
            return f'{text}'

    @staticmethod
    def info_log(text: str, tag: str = '') -> str:
        if tag:
            tag = Fore.BLUE + tag + Style.RESET_ALL
            text = Fore.WHITE + text + Style.RESET_ALL
            return f'[{tag}] {text}'
        else:
            text = Fore.BLUE + text + Style.RESET_ALL
            return f'{text}'
