
"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self._lines = input_file.read()
        self._lines = re.sub(r'[/].*||[\t\ ]', '', self._lines)     # remove comments and white spaces
        self._lines = re.sub(r'[\s]{2}', '', self._lines)           # remove double newlines
        self._lines = re.sub(r'^\s|\s$', '', self._lines)           # remove first and last lines if they are white spaces
        self._lines = self._lines.splitlines()
        self._curr_line = 0


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self._curr_line < len(self._lines)


    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self._curr_line = self._curr_line + 1


    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        i = self._curr_line
        if ('(' in self._lines[i]):
            return "L_COMMAND"
        if ('@' in self._lines[i]):
            return "A_COMMAND"
        return "C_COMMAND"


    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if (self.command_type() == "A_COMMAND"):
            return self._lines[self._curr_line][1:]
        if (self.command_type() == "L_COMMAND"):
            return self._lines[self._curr_line][1:-1]


    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        mnemonic = self._lines[self._curr_line]
        i = mnemonic.find('=')
        if (self.command_type() == "C_COMMAND" and i != -1):
            return mnemonic[:i]
        return ''


    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        mnemonic = self._lines[self._curr_line]
        i = mnemonic.find('=')
        j = mnemonic.find(';')
        if (self.command_type() == "C_COMMAND"):
            if (i == -1 and j == -1):
                return mnemonic
            if (j == -1):
                return mnemonic[i+1:]
            return mnemonic[i+1:j]
        return ''


    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        mnemonic = self._lines[self._curr_line]
        j = mnemonic.find(';')
        if (self.command_type() == "C_COMMAND" and j != -1):
            return mnemonic[j+1:]
        return ''
