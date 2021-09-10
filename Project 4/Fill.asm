// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@SCREEN
D = A           // D = first register of screen
@address
M = D           // Initialize address to screen
D = M
@8191
D = D + A       // D = screen + 8191
@max
M = D           // max = screen + 8191
(LOOP)
@color
M = 0           // Set color to white
@SCREEN
D = A           // D = first register of screen
@address
M = D           // Reset address to screen
@KBD
D = M           // D = keyboard register value
@SCREEN
D = D - M       // Check if color and input = 0
@LOOP
D;JEQ           // Restart if screen is already white
@KBD
D = M           // D = keyboard register value
@SCREEN
D = D + M       // Check if color and input = 0
D = D + 1
@FILL
D;JEQ           // Skip to fill if kbd = 0 and screen is black (-1)
@color
M = -1          // Set color to black (-1 = all 1s for black row)
@KBD
D = M           // Check if input != 0
@LOOP
D;JEQ           // Restart if input = 0
@SCREEN
D = M           // Check if screen already black
@LOOP
D;JNE           // Restart if so
(FILL)
@color
D = M           // D = color (color row black or white)
@address
A = M           // Set address value stored in address
M = D           // Color pixels
@address
M = M + 1       // Address += 1
D = M           // D = address
@max
D = D - M       // D = address - max
@FILL
D;JNE           // Jump if D != 0 (address != max)
@LOOP
0;JMP           // Repeat program