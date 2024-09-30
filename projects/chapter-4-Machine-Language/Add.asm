// Computes R2 = R0+R1+17
    @0
    D=M
    @R1
    D=D+M
    @17
    D=D+A
    @R2
    M=D
(END)
    @END
    0;JMP
