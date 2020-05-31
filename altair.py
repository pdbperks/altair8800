# Altair 8800 emulator for BBC Micro:bit
# UI code
# run code for sample program in original manual page 33
# @pdbperks 2020
from microbit import *

row = 0
col = 4
databyte = "00000000"
memory = [0 for x in range(256)]
#prog = [58,128,0,71,58,129,0,128,50,130,0]
prog = bytearray([
    0x3A,0x0C,0x0,0x47,0x3A,0x0D,0x0,0x80,
    0x32,0x0F,0x0,0x00,0x01,0x02,0x04,0x0,
    0x3A,0x0E,0x0,0x4F,0x3C,0x0D,0xC2,0x14,
    0x0,0x32,0x0F,0x0
    ])
pc = 0
tr = False   #show acc value
zf = True

def run():
    acc = 0
    regB = 0
    regC = 0
    global pc, memory, zf
    display.scroll('>')
    while True:
        sleep(500)
        if tr:
            display.scroll('a:'+str(acc))
            #display.scroll('z:'+str(zf))
        memRead(pc)
        if memory[pc] ==0:
            break
        # implemented 8080 operating codes
        elif memory[pc] == 0x07:    #7: #RLC rotate left <<
            acc = acc << 1
            pc = pc + 1
        elif memory[pc] == 0x0D:    #13: #DCR_C RegC -1
            regC = regC - 1
            zf = (regC == 0)
            pc = pc + 1            
        elif memory[pc] == 0x0F:    #15: #RLR rotate right <<
            acc = acc >> 1
            pc = pc + 1
        elif memory[pc] == 0x32:    #50:   #STA
            memory[memory[pc + 1]] = acc
            pc = pc + 3
        elif memory[pc] == 0x3A:    #58:    #LDA
            acc = memory[memory[pc + 1]]
            pc = pc + 3
        elif memory[pc] == 0x3C:    #60: #INR_A
            acc = acc + 1
            zf = (acc == 0)
            pc = pc + 1
        elif memory[pc] == 0x3D:    #61: #DCR_A
            acc = acc - 1
            zf = (acc == 0)
            pc = pc + 1
        elif memory[pc] == 0x47:    #71 : #MOV_B,A
            regB = acc
            pc = pc + 1
        elif memory[pc] == 0x4F:    #71 : #MOV_C,A
            regC = acc
            pc = pc + 1
        elif memory[pc] == 0x80:    #128:  #ADD
            acc = acc + regB
            pc = pc + 1
        elif memory[pc] == 0xC3:    #195:   #JMP
            pc = memory[pc + 1]
        elif memory[pc] == 0xC2:    #194:   #JNZ
            if zf == False:
                pc = memory[pc + 1]
            else:
                pc = pc + 3
        elif button_a.is_pressed():
            break
    display.scroll('end')

def bin00(dec):
    bin0 = "00000000"
    bin1 = bin(dec)[2:]
    #display.scroll(bin1)
    bin1L = len(bin1)
    return bin0[0:8-bin1L] + bin1

#led matrix for data entry
def level():
    global row, col
    for x in range(0, 4):
        display.set_pixel(x, 0, 0)
    for y in range(0, 5):
        display.set_pixel(4, y, 0)
    row = accelerometer.get_x()     #pitch 2 row
    row = min(max(0,int(row/200) + 2),3) # roll sensitivity row/60=narrow 400=wide + tilt factor
    display.set_pixel(row, 0 , 1)
    col = accelerometer.get_y()   # roll 4 bit cols
    col = min(max(3,int(col/200) + 1),4)  #pitch sensitivity 200 horizontal 300 more vertical + tilt factor
    display.set_pixel(4, col , 1)

#convert data rows to binary string
def dataRead():
    global databyte
    datab =""
    for y in range(3,5):
        for x in range(0,4 ):
            if (display.get_pixel(x, y)>0):
                datab = datab  + "1"
            else:
                datab = datab  + "0"
    databyte = datab

#write databyte to data display
def dataWrite(db = databyte, ledrow = 3):
    #global databyte
    p = 0
    bright = 4 + ledrow
    for y in range(ledrow,ledrow + 2):
        for x in range(0,4 ):
            if db[p] == "1":
                display.set_pixel(x,y,bright)
            else:
                display.set_pixel(x,y,0)
            p = p + 1

def memWrite(progcount = pc):
    global databyte, memory
    memory[progcount] = int(databyte, 2)
    dataWrite(bin00(progcount),1)
    dataWrite(databyte,3)

def memRead(progcount = pc):
    global databyte, memory
    databyte = bin00(memory[progcount])
    dataWrite(bin00(progcount),1)
    dataWrite(databyte)

#main program loop
while True:
    level()
    sleep(200)
    if (button_a.is_pressed()):
        longpress = 0
        clicks = button_b.get_presses()
        clicks = 0
        while button_a.is_pressed():
            sleep(100)#wait until button released
            longpress = longpress + 1
        #clicks = button_a.get_presses()
        if longpress > 10:  #clear display if button down >1second 
            clicks = button_b.get_presses()
            if clicks == 1: #run
                run()
            elif clicks == 2:   #load mem.dat
                    try:
                        with open('data.bin','rb') as f:
                            memory = list(f.read())
                        memRead(pc)
                    except OSError:
                        #if no file saved then load sample program
                        for i, d in enumerate(prog):
                            memory[i] = d
                        memRead(pc)
            elif clicks == 3:   #save
                with open('data.bin','wb') as f:
                    f.write(bytearray(memory))
                display.scroll('saved')
            elif clicks == 4:   #toggle tr acc
                tr ^= True
            elif clicks == 0: #no button clear data
                databyte = "00000000"
                dataWrite(databyte)

        else:
            display.set_pixel(row, col , (7 * (display.get_pixel(row, col) < 1)))
            dataRead()

    elif button_b.is_pressed():
        longpress = 0
        clicks = button_a.get_presses()
        clicks = 0
        while button_b.is_pressed():
            sleep(100)
            longpress = longpress + 1
        if longpress > 5:  #clear display if button down >0.5second
            clicks = button_a.get_presses()
            if clicks == 1:
                memWrite(pc)
                pc = min(pc + 1,256)
                memRead(pc)
            elif clicks == 2:
                pc = max(0,pc - 1)
                memRead(pc)
            elif clicks == 3:   #goto mem addr from data entry
                dataRead()
                pc = int(databyte, 2)
                memRead(pc)
            elif clicks == 0: #no button a click print hex
                display.scroll(hex(int(databyte, 2)))
                memWrite(pc)
        else:
            display.scroll(int(databyte, 2))
            memWrite(pc)

