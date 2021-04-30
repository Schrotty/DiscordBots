from discord.ext import commands
from typing import List,  Optional

class BoolParser(commands.Converter):
    """Converts a string to boolean value, based on true or false equivalent words in argument.
    """

    TRUE_STRINGS: Optional[List[str]] = ['true', 'ja', 'y', '1']
    FALSE_STRINGS: Optional[List[str]] = ['false', 'nein', 'n', '0']

    def __init__(self, true_strings: List[str] = None, false_strings: List[str] = None, is_case_sensitive : bool = False):
        """Uses default lists from config if optionals are None \n
        Args:
            true_strings (List[str]): Strings that resolve to a True value
            false_strings (List[str]): Strings that resolve to a False value
            is_case_sensitive (Optional[bool], optional): [description]. Defaults to false.
        """

        #Fill with default values
        if true_strings is []:
            true_strings = BoolParser.TRUE_STRINGS
        if false_strings is []:
            false_strings = BoolParser.FALSE_STRINGS

        #Set to lower depending on is_case_senstivie
        if is_case_sensitive:
            self.true_strings = [true_string.lower() for true_string in true_strings]
            self.false_strings = [false_string.lower() for false_string in false_strings]

    async def convert(self, ctx, argument : str) -> Optional[bool]:
        lowered = argument.lower()
        if lowered in self.true_strings:
            return True
        elif lowered in self.false_strings:
            return False
        else:
            return None #None if none were catched