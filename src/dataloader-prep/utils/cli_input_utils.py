from InquirerPy import inquirer

ENABLE_TERMINAL_BELL = False


def ask_text(prompt: str, default: str | None = None) -> str:
    prompt = prompt + "\n>"
    return inquirer.text(
        message=prompt,
        default=default if default is not None else "",
    ).execute()


def ask_yes_no(prompt: str, default: bool | None = None) -> bool:
    return inquirer.confirm(
        message=prompt,
        default=default if default is not None else False,
    ).execute()

def ask_option(
    prompt: str,
    options: list[str],
) -> str:
    if not options:
        raise ValueError("Options list cannot be empty.")

    return inquirer.fuzzy(
        message=prompt,
        choices=options,
    ).execute()

def ask_multi_options(
    prompt: str,
    options: list[str],
) -> list[str]:
    return inquirer.fuzzy(
        message=prompt + " (Press TAB to select multiple, ENTER to confirm)",
        choices=options,
        multiselect=True,
    ).execute()


def ask_int(
    prompt: str,
    default: int | None = None,
    min_value: int | None = None,
) -> int:
    def validate(value: str) -> bool:
        if value == "" or value is None:
            return False

        if not value.isdigit():
            return False

        if min_value is None:
            return True

        num = int(value)
        return num >= min_value

    return inquirer.text(
        message=prompt+"\n>",
        default=str(default) if default is not None else "",
        validate=validate,
        invalid_message="Enter a valid integer.",
        filter=int,
    ).execute()