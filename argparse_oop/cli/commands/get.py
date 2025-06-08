import argparse
import logging
import sys
from typing import NoReturn

from argparse_oop.cli.base import BaseCommand
from argparse_oop.cli.errors import MyCLIParserHelpError
from argparse_oop.cli.utils import discover_subcommands

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """The 'get' command"""

    name = "get"
    help = "Get information about various resources"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add command arguments"""
        self.parser = parser
        subparsers = self.parser.add_subparsers(
            title=f"{self.name} subcommands",
            dest="resource",
            metavar="RESOURCE",
            help="Specify what to get.",
        )

        command_path = self.__class__.__module__.rsplit(".", 1)[0]
        discover_subcommands(subparsers, command_path, self.name)

    def execute(self, args: argparse.Namespace) -> NoReturn:
        """Execute the command"""
        assert args.resource is None, "Resource was not None"
        self.parser.print_help(sys.stderr)
        raise MyCLIParserHelpError
