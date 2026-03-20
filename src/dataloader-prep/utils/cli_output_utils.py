RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
RESET = '\033[0m'

def print_plain(text: str) -> None:
    print(text)

def print_bad(text: str) -> None:
    print(RED + text + RESET)

def print_good(text: str) -> None:
    print(GREEN + text + RESET)

def print_warning(text: str) -> None:
    print(YELLOW + text + RESET)

def print_info(text: str) -> None:
    print(BLUE + text + RESET)
