import argparse
import logging
import sys
from importlib import metadata
from typing import Optional

from argparse_oop.cli.errors import MyCLIParserError, MyCLIParserHelpError
from argparse_oop.cli.utils import discover_commands

logger = logging.getLogger(__name__)

APP_NAME = "my-cli"
# VERSION = metadata.version(APP_NAME)
VERSION = "0.1.0"


class MyCLI:
    """The MyCLI class"""

    def __init__(self) -> None:
        """Initialize the CLI class"""
        self.config = None
        self.config_file = None

    def _init_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog=APP_NAME, description="A CLI tool")

        # Add global options here
        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s {VERSION}"
        )

        subparsers = parser.add_subparsers(
            title="commands",
            dest="command",
            metavar="COMMAND",
            required=True,
            help="Top-level commands. Use 'my-cli <command> --help' for more info",
        )

        top_level_commands = discover_commands("argparse_oop.cli.commands")
        for Command in top_level_commands:
            instance = Command()
            # This will in turn discover and register its subcommands
            instance.register(subparsers)

        return parser

    def _load_config(self) -> None:
        pass

    def _update_log_level(self, args: argparse.Namespace) -> None:
        if args.log:
            log_level = getattr(logging, args.log.upper(), None)
            if not isinstance(log_level, int):
                raise ValueError("Invalid log level: %s" % args.log)
            logging.getLogger().setLevel(log_level)

    def _run(self, args: argparse.Namespace, cli_mode: bool) -> object:
        assert hasattr(args, "func") and callable(args.func), (
            "Command/subcommand not configured properly"
        )

        try:
            result = args.func(args)
        except Exception as e:
            logger.debug(e)
            raise

        if cli_mode and result:
            print(result)  # noqa: T201
        else:
            return result

    def run(self, argv: Optional[list[str]] = None) -> Optional[object]:
        """The main CLI run command"""
        cli_mode = True if argv is None else False

        parser = self._init_parser()

        self._load_config()

        if argv is None:
            if len(sys.argv) <= 1:
                parser.print_help(sys.stderr)
                raise MyCLIParserHelpError
            argv = sys.argv[1:]
        else:
            if not argv:
                raise MyCLIParserError("No command provided via programmatic call")

        args = parser.parse_args(argv)

        self._update_log_level(args)

        result = self._run(args, cli_mode)
        return result
