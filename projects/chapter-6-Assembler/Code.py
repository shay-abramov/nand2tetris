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
        val = ""
        if ("A" in mnemonic):
            val = val + "1"
        else:
            val = val + "0"

        if ("D" in mnemonic):
            val = val + "1"
        else:
            val = val + "0"

        if ("M" in mnemonic):
            val = val + "1"
        else:
            val = val + "0"

        return val

    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        val = ""
        if ("M" in mnemonic):
            val = val + "1"
            mnemonic = mnemonic.replace("M", "A")
        else:
            val = val + "0"
        if (mnemonic == "0"):
            val += "101010"
        elif (mnemonic == "1"):
            val += "111111"
        elif (mnemonic == "-1"):
            val += "111010"
        elif (mnemonic == "D"):
            val += "001100"
        elif (mnemonic == "A"):
            val += "110000"
        elif (mnemonic == "!D"):
            val += "001101"
        elif (mnemonic == "!A"):
            val += "110001"
        elif (mnemonic == "-D"):
            val += "001111"
        elif (mnemonic == "-A"):
            val += "110011"
        else:
            val += "?*?*?*"

        return val

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        if (mnemonic == ""):
            return "000"
        if (mnemonic == "JGT"):
            return "001"
        if (mnemonic == "JEQ"):
            return "010"
        if (mnemonic == "JGE"):
            return "011"
        if (mnemonic == "JLT"):
            return "100"
        if (mnemonic == "JNE"):
            return "101"
        if (mnemonic == "JLE"):
            return "110"
        return "111"
