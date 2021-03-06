# altair8800
8-bit computer simulation for the BBC micro:bit
The simulator demonstrates 8-bit programming with the ability to save and load programs: it also works as a simple binary to decimal or hexadecimal translator. http://dperks.co.uk/altair/

Tilt the board to select the active column and row for data LED.  
The button functions:  
Button A: press to toggle data LED. Long press to clear all data LEDs.  
Run: Hold Button A, press button B once. Release both buttons.  
Load: Hold Button A, press button B twice. Release both buttons.  
Save: Hold Button A, press button B thrice. Release both buttons.  
Trace: Hold Button A, press button B four times. Release both buttons.  
Reload sample code: Hold Button A, press button B five times. Release both buttons.  
Halt program execution: hold Button A.

Button B: press for decimal. Long press hexadecimal.  
Write. PC++: Hold Button B, press button A once. Release both buttons.  
PC--. Read: Hold Button B, press button A twice. Release both buttons.  
Goto: Hold Button B, press button A thrice. Release both buttons.  

Here is a list of the implemented operating codes using the Accumulator, Register B, Register C, and zeroflag.   
I am providing two address bytes although one would be perfectly functional since program memory is currently set at 256 bytes.   
No further additions are now envisaged due to memory allocation limits.

|Decimal |Hex |Binary  |Mnemonic    |Bytes   |Action|
|---|---|---|---|---|---|
|7   |0x07    |0000 0111   |RLC     |1   |Accumulator bit shift left|
|13  |0x0D    |0000 1101   |DECC    |1   |Register C - 1|
|15  |0x0F    |0000 1111   |RRC     |1   |Accumulator bit shift left|
|50  |0x32    |0011 0001   |STA     |3   |Store Accumulator in address|
|58  |0x3A    |0011 1010   |LDA     |3   |Load Accumulator with contents of address|
|60  |0x3C    |0011 1100   |INRA    |1   |Accumulator + 1|
|61  |0x3D    |0011 1101   |DCRA    |1   |Accumulator - 1|
|71  |0x47    |0100 0111   |MOVBA   |1   |Move Accumulator to Register B|
|79  |0x4F    |0100 1111   |MOVCA   |1   |Move Accumulator to Register C|
|118 |0x76    |0111 0110   |HLT     |1   |Halt program execution|
|128 |0x80    |1000 0000   |ADDB    |1   |Add Register B to Accumulator| 
|160 |0xA0    |1010 0000   |ANAB    |1   |Bitwise Accumulator & Register B|
|168 |0xA8    |1010 1000   |XRAB    |1   |Bitwise Accumulator ^ Register B| 
|175 |0xAF    |1010 1111   |ANAA    |1   |Bitwise Accumulator ^ Accumulator| 
|176 |0xB0    |1011 0000   |ORAB    |1   |Bitwise Accumulator \| Register B|
|194 |0xC2    |1100 0010   |JNZ     |3   |Jump to address if zeroflag false| 
|195 |0xC3    |1100 0111   |JMP     |3   |Jump to address|

On reboot, the emulator will have a clear memory.   
If you load a program (A, 3 clicks B) it will load the sample program given in the Altair manual.  
If you have saved your own program then that will be loaded.  
Use (A, 5 clicks B) to revert to the sample program.  
You can toggle a trace feature for the contents of the Accumulator (A, 4 clicks B) which is useful for debugging.  
I have added a program at memory address 0x10 (16) to demonstrate JNZ op code.  
I have also changed the memory addresses used by the sample program so that data examples are preloaded with the code:  
add contents of memory addresses 12 and 13, store the answer in memory address 15.

|Address |Mnemonic  |Binary     |Action|
|---|---|---|---|
|0   |LDA     |0011 1010   |Load Accumulator with contents of address|
|1   |        |0000 1100   |Address (12)|
|2   |        |0000 0000   |Address|
|3   |MOVAB   |0100 0111   |Move accumulator to Register B|
|4   |LDA     |0011 1010   |Load Accumulator with contents of address|
|5   |        |0000 1101   |Address (13)|
|6   |        |0000 0000   |Address|
|7   |ADDB    |1000 0000   |Add Register B to Accumulator|
|8   |STA     |0011 0010   |Store Accumulator in address|
|9   |        |0000 1111   |Address (15)|
|10  |        |0000 0000   |Address|
|11  |HLT     |0111 0110   |Halt program|
|12  |        |0000 0001   |Data|
|13  |        |0000 0010   |Data|
|14  |        |0000 0100   |Data|
|15  |        |0000 0000   |Data|
|16  |LDA     |0011 1010   |Load Accumulator with contents of address|
|17  |        |0000 1110   |Address (14)|
|18  |        |0000 0000   |Address|
|19  |MOVCA   |0100 1111   |Move accumulator to Register C|
|20  |INRA    |0011 1100   |Accumulator + 1|
|21  |DECC    |0000 1101   |Register C - 1|
|22  |JNZ     |1100 0010   |Jump to address if zeroflag false|
|23  |        |0001 0100   |Address (20)|
|24  |        |0000 0000   |Address|
|25  |STA     |0011 0010   |Store Accumulator in address|
|26  |        |0000 1111   |Address (15)|
|27  |        |0000 0000   |Address|
|28  |HLT     |0111 0110   |Halt program|
