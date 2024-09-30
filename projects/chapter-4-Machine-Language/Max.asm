// Set R0 to max(R1,R2)
    @R1
    D=M
    @R2
    D=D-M
    // If R1 is bigger
    @MAX1
    D;JGT
    // else R2 is bigger
    @R2
    D=M
    @R0
    M=D
    @END
    0;JMP
(MAX1)
    @R1
    D=M
    @R0
    M=D
(END)
    @END
    0;JMP
