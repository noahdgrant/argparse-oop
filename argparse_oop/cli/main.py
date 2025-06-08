import logging
import sys

from argparse_oop.cli.cli import MyCLI
from argparse_oop.cli.errors import MyCLIParserError, MyCLIParserHelpError

logging.basicConfig(
    format="%(asctime)s | %(funcName)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def main() -> None:
    """The main CLI entrypoint"""
    cli = MyCLI()
    try:
        cli.run()
    except MyCLIParserHelpError:
        sys.exit(2)
    except MyCLIParserError as e:
        logger.error(e)
        sys.exit(2)
