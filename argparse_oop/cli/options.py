import argparse


def options_log(parser: argparse.ArgumentParser) -> None:
    """Log options"""
    group = parser.add_argument_group(title="logger options")
    group.add_argument(
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level (%(choices)s) - default is %(default)s.",
        metavar="LEVEL",
    )
