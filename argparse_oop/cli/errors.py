class MyCLIBaseError(Exception):
    """Base error for MyCLI"""

    pass


class MyCLIParserError(MyCLIBaseError):
    """Parser error for MyCLI"""

    pass


class MyCLIParserHelpError(MyCLIBaseError):
    """Parser error for MyCLI"""

    pass


class MyCLIRuntimeError(MyCLIBaseError):
    """Runtime error for MyCLI"""

    pass
