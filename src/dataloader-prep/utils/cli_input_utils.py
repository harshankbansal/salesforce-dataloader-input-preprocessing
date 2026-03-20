from typing import Iterable

ENABLE_TERMINAL_BELL = False


def ask_text(prompt: str, default: str | None = None) -> str:
    full_prompt = _build_prompt(prompt, default=default)
    value = input(full_prompt).strip()
    if value == "" and default is not None:
        return default
    return value


def ask_yes_no(prompt: str, default: bool | None = None) -> bool:
    default_label = None
    if default is True:
        default_label = "Y/n"
    elif default is False:
        default_label = "y/N"
    else:
        default_label = "y/n"

    full_prompt = _build_prompt(prompt, default=default_label)

    while True:
        value = input(full_prompt).strip().lower()
        if value == "":
            if default is not None:
                return default
            print("Please enter y/n.")
            continue

        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False

        print("Invalid input. Enter 'y'/'yes' or 'n'/'no'.")


def ask_option(
    prompt: str,
    options: list[str],
) -> str:
    if not options:
        raise ValueError("Options list cannot be empty.")

    full_prompt = _build_options_prompt(
        prompt=prompt,
        options=options,
        choice_hint="number",
    )

    while True:
        value = input(full_prompt).strip()
        if value == "":
            print("Please choose an option number.")
            continue

        if not value.isdigit():
            print("Invalid input. Please enter an option number.")
            continue

        selected_number = int(value)
        if not (1 <= selected_number <= len(options)):
            print(f"Invalid option: {selected_number}. Select 1 to {len(options)}.")
            continue
        return options[selected_number - 1]


def ask_multi_options(
    prompt: str,
    options: list[str],
) -> list[str]:
    full_prompt = _build_options_prompt(
        prompt=prompt,
        options=options,
        choice_hint="comma-separated numbers",
    )

    while True:
        value = input(full_prompt).strip()
        if value == "":
            print("Please enter one or more option numbers.")
            continue

        tokens = [token.strip() for token in value.split(",") if token.strip()]
        if not tokens:
            print("Please enter one or more option numbers.")
            continue

        if not all(token.isdigit() for token in tokens):
            print("Invalid input. Use comma-separated option numbers only.")
            continue

        selected_indices: list[int] = []
        for token in tokens:
            selected_number = int(token)
            if not (1 <= selected_number <= len(options)):
                print(f"Invalid option: {selected_number}. Select 1 to {len(options)}.")
                selected_indices = []
                break
            selected_indices.append(selected_number - 1)

        if not selected_indices:
            continue

        unique_indices = list(dict.fromkeys(selected_indices))
        return [options[index] for index in unique_indices]


def ask_int(
    prompt: str,
    default: int | None = None,
    min_value: int | None = None,
) -> int:
    full_prompt = _build_prompt(prompt, default=str(default) if default is not None else None)
    while True:
        value = input(full_prompt).strip()
        if value == "":
            if default is not None:
                parsed = default
            else:
                print("Please enter a number.")
                continue
        else:
            try:
                parsed = int(value)
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue

        if min_value is not None and parsed < min_value:
            print(f"Value must be >= {min_value}.")
            continue
        return parsed


def _with_default(prompt: str, default: str | None) -> str:
    if default is None:
        return f"{prompt}: "
    return f"{prompt} (default: {default}): "


def _build_prompt(prompt: str, default: str | None = None) -> str:
    if ENABLE_TERMINAL_BELL:
        # Emits terminal bell sound in supporting terminals to draw attention.
        print("\a", end="", flush=True)

    prompt_line = _with_default(prompt, default)
    return f"\n--- INPUT REQUIRED ---\n{prompt_line}\n> "


def _build_options_prompt(prompt: str, options: list[str], choice_hint: str) -> str:
    if ENABLE_TERMINAL_BELL:
        # Emits terminal bell sound in supporting terminals to draw attention.
        print("\a", end="", flush=True)

    lines = ["", "--- INPUT REQUIRED ---", prompt, "Options:"]
    for idx, option in enumerate(options):
        lines.append(f"{idx+1}. {option}")
    lines.append(f"Enter your choice ({choice_hint}):")
    lines.append("> ")
    return "\n".join(lines)
