# altair8800
8-bit computer simulation for the BBC micro:bit
The simulator demonstrates 8-bit programming with the ability to save and load programs: it also works as a simple binary to decimal or hexadecimal translator.

The button functions:
Button A: press to toggle data LED. Long press to clear data LEDs.
Run: Hold Button A, press button B once. Release both buttons.
Load: Hold Button A, press button B twice. Release both buttons.
Save: Hold Button A, press button B thrice. Release both buttons.
Trace: Hold Button A, press button B four times. Release both buttons.

Button B: press for decimal. Long press hexadecimal.
Write. PC++: Hold Button B, press button A once. Release both buttons.
PC--. Read: Hold Button B, press button A twice. Release both buttons.
Goto: Hold Button B, press button A thrice. Release both buttons.

Here is a list of the implemented operating codes using the Accumulator and Register B. I am providing two address bytes although one would be perfectly functional since program memory is currently set at 256 bytes. More op codes will be added.

Decimal	Hex	Binary	Mnemonic	Bytes	Action
7	0x07	0000 0111	RLC	1	Accumulator bit shift left
15	0x0F	0000 1111	RRC	1	Accumulator bit shift left
50	0x32	0011 0001	STA	3	Store Accumulator in address
58	0x3A	0011 1010	LDA	3	Load Accumulator with contents of address
60	0x3C	0011 1100	INRA	1	Accumulator + 1
61	0x3D	0011 1101	DCRA	1	Accumulator - 1
71	0x47	0100 0111	MOVBA	1	Move Accumulator to Register B
128	0x80	1000 0000	ADDB	1	Add Register B to Accumulator
195	0xC3	1100 0111	JMP	3	Jump to address

On reboot, the emulator will have a clear memory. If you load a program (A, 3 clicks B) it will load the sample program given in the Altair manual. If you have saved your own program then that will be loaded. You can toggle a trace feature for the contents of the Accumulator (A, 4 clicks B) which is useful for debugging.

Add	Mnemonic	Binary	Action
0 	LDA	  0011 1010	Load Accumulator with contents of address
1	  	    1000 0000	Address
2		      0000 0000	Address
3	  MOVAB	0100 0111	Move accumulator to Register B
4	  LDA	  0011 1010	Load Accumulator with contents of address
5		      1000 0001	Address
6		      0000 0000	Address
7	  ADDB	1000 0000	Add Register B to Accumulator
8	  STA	  0011 0010	Store Accumulator in address
9		      1000 0010	Address
10	  	  0000 0000	Address

