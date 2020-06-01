# Altair 8800 emulator for BBC Micro:bit
# UI code
# run code for sample program in original manual page 33
# @pdbperks 2020
from microbit import display, button_a, button_b, accelerometer, sleep

row = 0 # LED display
col = 4
databyte = "00000000"
memory = bytearray([0 for x in range(256)])
prog = bytearray([
    0x3A,0x0C,0x0,0x47,0x3A,0x0D,0x0,0x80,
    0x32,0x0F,0x0,0x76,0x01,0x02,0x04,0x0,
    0x3A,0x0E,0x0,0x4F,0x3C,0x0D,0xC2,0x14,
    0x0,0x32,0x0F,0x0,0x76
    ])
pc = 0  #program counter
tr = False   #show acc value
zf = True   #zero flag

def run():
    acc = 0 #Accumulator
    regB = 0    #register B
    regC = 0    #register C
    rpc = 0		#temp pc for loop
    global pc, memory, zf
    display.scroll('<')
    while True:
        sleep(500)
        memRead(pc)
        rpc = pc
        if tr:
            display.scroll('a:'+str(acc))
        # implemented 8080 operating codes
        if memory[rpc] == 0x00:    #0: #NOP
            pc = pc + 1
        if memory[rpc] == 0x07:    #7: #RLC rotate left <<
            acc = acc << 1
            pc = pc + 1
        if memory[rpc] == 0x0D:    #13: #DCR_C RegC -1
            regC = regC - 1
            zf = (regC == 0)
            pc = pc + 1            
        if memory[rpc] == 0x0F:    #15: #RLR rotate right <<
            acc = acc >> 1
            pc = pc + 1
        if memory[rpc] == 0x32:    #50:   #STA
            memory[memory[pc + 1]] = acc
            pc = pc + 3
        if memory[rpc] == 0x3A:    #58:    #LDA
            acc = memory[memory[pc + 1]]
            pc = pc + 3
        if memory[rpc] == 0x3C:    #60: #INR_A
            acc = acc + 1
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0x3D:    #61: #DCR_A
            acc = acc - 1
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0x47:    #71 : #MOV_B,A
            regB = acc
            pc = pc + 1
        if memory[rpc] == 0x4F:    #71 : #MOV_C,A
            regC = acc
            pc = pc + 1
        if memory[rpc] ==0x76: # HLT
            break
        if memory[rpc] == 0x80:    #128:  #ADD
            acc = acc + regB
            pc = pc + 1
        if memory[rpc] == 0xA0:    #61: #ANA_B
            acc = acc & regB
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0xA8:    #61: #XRA_B
            acc = acc ^ regB
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0xAF:    #61: #XRA_A
            acc = acc ^ acc
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0xB0:    #61: #ORA_B
            acc = acc | regB
            zf = (acc == 0)
            pc = pc + 1
        if memory[rpc] == 0xC3:    #195:   #JMP
            pc = memory[pc + 1]
        if memory[rpc] == 0xC2:    #194:   #JNZ
            if zf == False:
                pc = memory[pc + 1]
            else:
                pc = pc + 3
        if button_a.is_pressed():
            break
    display.scroll('>')

def bin00(dec):
    bin0 = "00000000"
    bin1 = bin(dec)[2:]
    #display.scroll(bin1)
    bin1L = len(bin1)
    return bin0[0:8-bin1L] + bin1

#led matrix for data entry
def level():
    global row, col
    bright = 3
    for x in range(0, 4):
        display.set_pixel(x, 0, 0)
    for y in range(0, 5):
        display.set_pixel(4, y, 0)
    row = accelerometer.get_x()     #pitch 2 row
    row = min(max(0,int(row/200) + 1),3) # roll sensitivity row/60=narrow 400=wide + tilt factor
    display.set_pixel(row, 0 , bright)
    col = accelerometer.get_y()   # roll 4 bit cols
    col = min(max(3,int(col/200) + 1),4)  #pitch sensitivity 200 horizontal 300 more vertical + tilt factor
    display.set_pixel(4, col , bright)

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
    bright = 6 + ledrow
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
        if longpress > 5:  #optons if button down >0.5second 
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
        if longpress > 5:  #options if button down >0.5second
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
