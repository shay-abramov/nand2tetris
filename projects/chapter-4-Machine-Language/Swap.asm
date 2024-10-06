// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.
    @16384
    D=A
    @max
    M=-D
    @min
    M=D
    @i
    M=0
    D=M
(LOOP)
    @i
    D=M
    @R15
    D=D-M
    @END
    D;JGE
    @i
    D=M
    @R14
    D=D+M
    A=D
    D=M
    @max
    D=D-M
    @SWAP_MAX_END
    D;JLE
(SWAP_MAX)
    @i
    D=M
    @R14
    A=D+M
    D=M
    @max
    M=D
(SWAP_MAX_END)
    @i
    D=M
    @R14
    A=D+M
    D=M
    @min
    D=D-M
    @SWAP_MIN_END
    D;JGE
(SWAP_MIN)
    @i
    D=M
    @R14
    A=D+M
    D=M
    @min
    M=D
(SWAP_MIN_END)
    @i
    M=M+1
    @LOOP
    0;JMP
(LOOP_END)
(END)
    @END
    0;JMP
