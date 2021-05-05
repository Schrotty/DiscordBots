class Template:
    ALIAS: list = []
    COMMAND_NAME: str = "add"
    HELP_TEXT: str = "Adds a new quote. Author must not contain any spaces."

    QUOTE: str = '#{ID}: "{QUOTE}" - {AUTHOR}'
    NO_QUOTE_FOUND: str = "Found no quote. Add one with !quote add <author> <quote>"
    ELEMENT_IS_MISSING: str = "Quote or author is missing"
    MISSING_PERMISSION: str = "You are not allowed to use this, {MENTION}"
