import argparse
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """Base command class"""

    name: str
    help: str

    def __init__(self) -> None:
        """Initialize a command."""
        if not self.name or not self.help:
            raise NotImplementedError(
                f"{self.__class__.__name__} must define 'name' and 'help' attributes"
            )

    def get_common_options(self) -> list:
        """Subclasses should override this method to return a list of options whose
        arguments should be included
        """
        return []

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add command specific arguments"""
        pass

    @abstractmethod
    def execute(self, args: argparse.Namespace) -> None:
        """Execute the command"""
        pass

    def register(
        self, subparsers_action: argparse._SubParsersAction
    ) -> argparse.ArgumentParser:
        """Register this command with the parent's subparser"""

        declared_options = self.get_common_options()

        parser = subparsers_action.add_parser(
            self.name, help=self.help, description=self.help
        )

        for initializer_func in declared_options:
            initializer_func(parser)

        self.add_arguments(parser)

        parser.set_defaults(
            func=self.execute, command_name=self.name, command_instance=self
        )
        return parser
