"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


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
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.input_lines = input_file.read().replace(" ", "").splitlines()
        self.curr_line = -1
        self.advance()


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self.curr_line<len(self.input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.curr_line = self.curr_line + 1
        while(self.has_more_commands() and ("//" in self.input_lines[self.curr_line] or self.input_lines[self.curr_line]=='')):
            self.curr_line = self.curr_line + 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if (not self.has_more_commands()):
            return
        if (self.input_lines[self.curr_line][0] == '@'):
            return "A_COMMAND" 
        if (self.input_lines[self.curr_line][0] == '('):
            return "L_COMMAND"
        return "C_COMMAND"


    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if (self.command_type() == "A_COMMAND"):
            return self.input_lines[self.curr_line][1:]


    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if (self.command_type() == "C_COMMAND"):
            str1 = self.input_lines[self.curr_line]
            i = str1.find('=')
            if (i == -1):
                return ""
            return str1[:i]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if (self.command_type() == "C_COMMAND"):
            str1 = self.input_lines[self.curr_line]
            i = str1.find('=')
            j = str1.find(';')
            if (i == -1 and j == -1):
                return str1
            if (i == -1 and j != -1):
                return str1[:j]
            if (i != -1 and j == -1):
                return str1[i+1:]
            return str1[i+1:j] 

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if (self.command_type() == "C_COMMAND"):
            str1 = self.input_lines[self.curr_line]
            j = str1.find(';')
            if (j == -1):
                return ""
            return str1[j+1:]
 
