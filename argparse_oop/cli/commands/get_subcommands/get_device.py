import argparse
import logging

from argparse_oop.cli.base import BaseCommand
from argparse_oop.cli.options import options_log

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """The 'get device' command"""

    name = "device"
    help = "Get information about a device."

    def get_common_options(self) -> list:
        """Command options the command uses"""
        return [options_log]

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add command arguments"""
        parser.add_argument("hardware", type=int, help="The device hardware ID.")

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the command"""
        print(args.hardware)
