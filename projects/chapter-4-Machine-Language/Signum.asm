// if R0>=0 then R1=1
// else R1=-1
    @R0
    D=M
    @POSITIVE
    D;JGE
(NEGATIVE)
    @R1
    M=-1
    @END
    0;JMP
(POSITIVE)
    @R1
    M=1
(END)
    @END
    0;JMP
