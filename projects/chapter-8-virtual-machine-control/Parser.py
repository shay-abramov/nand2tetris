"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re

C_ARITHMETIC    = "C_ARITHMETIC"
C_PUSH          = "C_PUSH"
C_POP           = "C_POP"
C_LABEL         = "C_LABEL"
C_GOTO          = "C_GOTO"
C_IF            = "C_IF"
C_FUNCTION      = "C_FUNCTION"
C_RETURN        = "C_RETURN"
C_CALL          = "C_CALL"


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # next sequence of lines used to remove comments and extra white lines
        input_str = input_file.read()
        input_str = re.sub(r'[/]{2}.*', '', input_str)
        input_str = re.sub(r'\s{2,}', '', input_str)
        input_str = re.sub(r'\s$', '', input_str)
        
        # split effective lines into an array and set line index to -1 
        # (ready to advance to the first line)
        self._lines = input_str.splitlines()
        self._i = -1
        self._curr_line = None


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self._i < len(self._lines) - 1


    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        if self.has_more_commands():
            self._i = self._i + 1
            self._curr_line = self._lines[self._i]


    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        arithmetic_commands = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

        if any(command in self._curr_line for command in arithmetic_commands):
            return C_ARITHMETIC
        elif "push" in self._curr_line:
            return C_PUSH
        elif "pop" in self._curr_line:
            return C_POP
        elif "label" in self._curr_line:
            return C_LABEL
        elif "goto" in self._curr_line:
            return C_GOTO
        elif "return" in self._curr_line:
            return C_RETURN


    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type() == C_ARITHMETIC:
            return self._curr_line.split()[0]
        elif self.command_type() == C_PUSH or self.command_type() == C_POP:
            return self._curr_line.split()[1]


    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        if self.command_type() == C_PUSH or self.command_type() == C_POP:
            return self._curr_line.split()[2]

