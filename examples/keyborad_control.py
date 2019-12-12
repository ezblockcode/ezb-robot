# import picar_4wd as fc
import sys
import tty
import termios
import asyncio
from  spider import Spider
from ezblock import Camera

power_val = 50
key = 'status'

cam = Camera(0, rotation=180)
cam.start()

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def Keyborad_control():
    sp = Spider([1,2,3,4,5,6,7,8,9,10,11,12])
    
    sp.set_offset([15,-4,-7,  -8,-6,6,  10,10,-10,  -5,3,-5])
    # sp.do_action("ready", speed=100)
    while True:
        global power_val
        key=readkey()
        print(key)
        if key=='6':
            if power_val <=90:
                power_val += 10
                print("power_val:",power_val)
        elif key=='4':
            if power_val >=10:
                power_val -= 10
                print("power_val:",power_val)
        if key=='w':
            sp.do_action("forward",speed=100)
        elif key=='a':
            sp.do_action("turn left",speed=100)
        elif key=='s':
            sp.do_action("backward",speed=100)
        elif key=='d':
            sp.do_action("turn right",speed=100)
        elif key=='n':
            sp.do_action("sit",speed=100)
        else:
            if key=='l':
                sp.do_action("look right",speed=100)
            elif key=='j':
                sp.do_action("look left",speed=100)
            elif key=='i':
                sp.do_action("look up",speed=100)
            elif key=='k':
                sp.do_action("look down",speed=100)    
            elif key=='f':
                sp.do_action("push up",speed=100)
            elif key=='g':
                sp.do_action("wave",speed=100)
            else:
                sp.do_action("stand",speed=100)
            
        # else:
        #     sp.do_action("sit",speed=100)
        if key=='q':
            print("quit")  
            break  
if __name__ == '__main__':
    Keyborad_control()




