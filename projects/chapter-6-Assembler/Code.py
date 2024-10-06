"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""
    
    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        str = ""
        if 'A' in mnemonic:
            str += '1'
        else:
            str += '0'
        if 'D' in mnemonic:
            str += '1'
        else:
            str += '0'
        if 'M' in mnemonic:
            str += '1'
        else:
            str += '0'
        return str


    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        a = "0"
        if "M" in mnemonic:
            a = "1"
            mnemonic = mnemonic.replace("M", "A")

        match mnemonic:
            case "0":
                return a + "101010"
            case "1":
                return a + "111111"
            case "-1":
                return a + "111010"
            case "D":
                return a + "001100"
            case "A":
                return a + "110000"
            case "!D":
                return a + "001101"
            case "!A":
                return a + "110001"
            case "-D":
                return a + "001111"
            case "-A":
                return a + "110011"
            case "D+1":
                return a + "011111"
            case "A+1":
                return a + "110111"
            case "D-1":
                return a + "001110"
            case "A-1":
                return a + "110010"
            case "D+A":
                return a + "000010"
            case "D-A":
                return a + "010011"
            case "A-D":
                return a + "000111"
            case "D&A":
                return a + "000000"
            case "D|A":
                return a + "010101"
            case _:
                # default, if code was correct shouldn't get here
                return ""

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        str = ""
        if mnemonic == "":
            return "000"
        if mnemonic == "JMP":
            return "111"
        if mnemonic == "JNE":
            return "101"

        if 'L' in mnemonic:
            str += '1'
        else:
            str += '0'

        if 'E' in mnemonic:
            str += '1'
        else:
            str += '0'

        if 'G' in mnemonic:
            str += '1'
        else:
            str += '0'

        return str

