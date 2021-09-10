// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@R2
M = 0           // Initialize R2 to 0
(LOOP)
@R0
D = M           // D = R0 value
@END
D;JEQ           // Exit if R0 value = 0
@R1
D = M           // D = R1 value
@R2
M = D + M       // R2 value += R1 value
@R0
M = M - 1       // R0 value -= 1
@LOOP
0;JMP           // Jump until we have looped R0 times (counter = R0)

(END)
@END
0;JMP           // Infinite loop to prevent nop slide