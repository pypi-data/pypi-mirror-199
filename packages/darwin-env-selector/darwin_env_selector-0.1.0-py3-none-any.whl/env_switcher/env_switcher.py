#!/usr/bin/env python

from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm
from simple_term_menu import TerminalMenu
from typing import List
from shutil import copyfile
from datetime import datetime


console = Console()


def continue_confirm(affirmative: str = "Continue") -> None:
    console.line(1)
    console.rule(affirmative + "?")
    if not Confirm.ask(affirmative):
        exit(0)


def choose_directory() -> List[Path]:
    home_darwin = Path.home() / ".darwin"
    options = [f"Default directory ({home_darwin})", "Custom directory"]
    menu = TerminalMenu(options, clear_screen=False, clear_menu_on_exit=False)
    console.rule("Choose a directory")
    selected = menu.show()
    if selected == 0:
        path = home_darwin
    else:
        path = Path(console.input("Enter the path to the directory: "))

    if not path.exists():
        console.print(f"Directory does not exist: {path}")
        continue_confirm("Try again")
        return choose_directory()

    config_files = [
        f
        for f in path.glob("*.yaml")
        if f.is_file() and f.name != "config.yaml"
    ]
    backup_files = [f for f in path.glob("*.yaml.backup") if f.is_file()]
    console.print(
        f"Using directory: {path}, found {len(config_files)} config files, and {len(backup_files)} backup files."
    )

    if not config_files:
        console.print("No config files found, but we could create one for you")
        if not Confirm.ask("Create a file?"):
            exit(0)
        elif not Confirm.ask("Create a new config file in {path}?}"):
            return create_config_file(path)
        else:
            continue_confirm("Return to main menu")
            main_menu(path, config_files, backup_files)

    if not Confirm.ask("Is this correct?"):
        choose_directory()

    main_menu(path, config_files, backup_files)


def main_menu(
    path: Path,
    config_files: List[Path],
    backup_files: List[Path],
    backup_mode: bool = False,
) -> None:
    console.rule("Choose an action")
    menu = TerminalMenu(
        [
            "Create a new config file",
            "Choose a config file",
            "Backup current file",
            "Restore backup file",
            "Delete old backup files",
        ],
        clear_screen=False,
        clear_menu_on_exit=False,
    )
    action = menu.show()

    actions = ["new", "choose", "backup", "restore", "delete"]
    action = actions[action]

    if action == "new":
        create_config_file(path)

    elif action == "choose":
        choose_config_file(config_files)

    elif action == "backup":
        backup_config_file(path)

    elif action == "restore":
        choose_config_file(backup_files, restore_mode=True)

    elif action == "delete":
        if Confirm.ask("Are you sure you want to delete all backup files?"):
            path.glob("*.yaml.backup").unlink()
        main_menu(path, config_files)


def backup_config_file(config_path: Path) -> None:
    console.rule("Copy current config file to a named file")

    console.print(
        "Copies the active config file to a new file that you can switch to and from later."
    )
    console.print("E.g. config.yaml -> foo.yaml")
    console.print(
        "You can then switch to foo.yaml by choosing it from the main menu."
    )

    config_file = config_path / "config.yaml"
    if not config_file.exists():
        console.print("No config file found")
        continue_confirm("Return to main menu")
        main_menu()

    filename: str = console.input(
        "Name for backup file (defaults to current date and time):",
        default=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    )

    if not filename.endswith(".yaml"):
        filename += ".yaml"

    whole_path = config_path / filename

    copyfile(config_file, whole_path)
    return None


def choose_config_file(
    config_files: List[Path], restore_mode: bool = True
) -> None:
    if restore_mode:
        console.rule("Choose a backup file to restore")
    else:
        console.rule("Choose a config file")

    full_paths = [
        f for f in config_files if f.is_file() and f.name != "config.yaml"
    ]
    menu_options = [f.name for f in full_paths]

    choose_menu = TerminalMenu(
        menu_options, clear_screen=False, clear_menu_on_exit=False
    )
    chosen = choose_menu.show()

    file: Path = full_paths[chosen]

    console.print(f"Using config file: {file.name}")

    if not Confirm.ask("Apply config file?"):
        continue_confirm("Return to main menu?")

    if restore_mode:
        backup_name = (
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".yaml.backup"
        )
        backup_path = file.parent / backup_name

        console.print(f"Backing up {file.name} to {backup_name}")

        copyfile(file, backup_path)
        with open(backup_path, "w+") as f:
            f.write(f"# Backup of {file.name} created on {datetime.now()}")

    console.print(f"Copying {file.name} to config.yaml")
    copyfile(file, file.parent / "config.yaml")


def create_config_file(config_path: Path) -> None:
    try:
        console.print("Enter a name for the new config file")
        server = (
            console.input(
                'Server(include protocol, like "https://", no trailing space, defaults to darwin): '
            ).strip()
            or "https://darwin.v7labs.com"
        )
        name = console.input(
            "File name (A-z0-9 with dashes and underscores only, don't include the extension): "
        )

        while True:
            teams = []
            while True:
                console.print(
                    "Add a team to the config file. You can add more later."
                )
                team_slug = console.input(
                    "Team slug [a-z and underscores only]: "
                )
                api_key = console.input("API key: ", password=True)
                teams.append((team_slug, api_key))
                if not Confirm.ask("Add another team?", console=console):
                    break

            if not teams:
                console.print("You need to add at least one team.")
                if not Confirm.ask("Try again?", console=console):
                    exit(0)
                continue
            else:
                break

        assert name and teams and server, "Name and teams are required"
        assert all(
            slug for slug, _ in teams
        ), "All teams must have a slug and an API key"
        assert all(
            api_key for _, api_key in teams
        ), "All teams must have a slug and an API key"
    except ValueError:
        console.print("Invalid input, please try again")
        continue_confirm("Return to main menu?")
        main_menu()
    else:
        console.print(
            "[red][bold]WARNING[/bold][/red]: We don't verify much about the info you entered, so double check it."
        )

        new_config = Path(config_path) / Path(f"{name}.yaml")
        content = f"""
global:
  api_endpoint: {server}/api/
  base_url: {server}
  default_team: {teams[0][0]}
teams:"""
        for slug, api_key in teams:
            content += f"""
  {slug}:
    api_key: {api_key}
    datasets_dir: {Path(config_path).parent / slug / "datasets"}
"""

        console.print(content)
        if not Confirm.ask("Save config file?"):
            continue_confirm("Return to main menu?")
            main_menu()
        else:
            with new_config.open("w") as f:
                f.write(content)

            console.print(f"Config file saved to {new_config}")
            continue_confirm("Return to main menu?")
            main_menu()

    return None


def main() -> None:
    try:
        console.clear()
        console.rule("Welcome to the Darwin config file selector")
        console.print(
            "This program will help you choose a config file for Darwin."
        )
        console.line(2)
        choose_directory()
        exit()
    except KeyboardInterrupt:
        continue_confirm("Exit the program")
    except Exception as exc:
        console.print("An error occurred unexpectedly, details below:\n")
        console.rule()
        console.print(exc)
        console.rule()
        exit(128)


if __name__ == "__main__":
    main()
