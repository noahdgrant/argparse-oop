import argparse
import importlib
import inspect
import logging
import pkgutil
from typing import Type

from argparse_oop.cli.base import BaseCommand

logger = logging.getLogger(__name__)


def discover_commands(package_import_path: str) -> list[Type[BaseCommand]]:
    """Discover command classes"""
    command_classes: list[Type[BaseCommand]] = []

    try:
        package = importlib.import_module(package_import_path)
    except ImportError:
        raise ImportError(
            f"Package '{package_import_path}' not found or could not be imported."
        )

    # Scan modules directly within the package, but not subpackages
    if hasattr(package, "__path__"):
        for _, module_name, is_pkg_flag in pkgutil.iter_modules(
            path=package.__path__,  # List the paths constituting the package
            prefix=package.__name__ + ".",  # Prefix for an absolute import
        ):
            if not is_pkg_flag:
                try:
                    sub_module = importlib.import_module(module_name)
                    for _, member_obj in inspect.getmembers(sub_module):
                        if (
                            inspect.isclass(member_obj)
                            and issubclass(member_obj, BaseCommand)
                            and member_obj is not BaseCommand
                            and member_obj.__module__ == sub_module.__name__
                        ):
                            if member_obj not in command_classes:
                                command_classes.append(member_obj)
                except ImportError as e:
                    logger.warning(
                        f"Could not import module '{module_name}' from {package_import_path}: {e}"
                    )

    return command_classes


def discover_subcommands(
    subparsers: argparse._SubParsersAction, command_path: str, name: str
) -> None:
    """Discover subcommands for top-level commands"""
    subcommand_path = f"{command_path}.{name}_subcommands"
    logger.debug(f"Scanning for '{name}' subcommands in: {subcommand_path}")

    subcommands = discover_commands(subcommand_path)
    for Command in subcommands:
        try:
            instance = Command()
            instance.register(subparsers)
        except Exception as e:
            logger.warning(
                f"Could not register '{name}' resource {Command.__name__}: {e}"
            )
