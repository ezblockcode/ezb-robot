from spider import Spider
import sys
import tty
import termios
import asyncio
import time

def cali_helper():
    
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

    cali_print_template = '''
  .........        .........
<=|   2   |┌-┌┐┌┐-┐|   1   |=>
  `````````├ ```` ┤`````````
  .........├      ┤.........
<=|   3   |└------┘|   4   |=>
  `````````        ````````
'''
    sp = Spider([1,2,3,4,5,6,7,8,9,10,11,12])
    print("*****************************************")
    print("*                                       *")
    print("*      Spider Calibration Helper        *")
    print("*                                       *")
    print("*****************************************")
    print("")
   
    cali_coord = [[62, 0, -30], [62, 0, -30], [62, 0, -30], [62, 0, -30]]
    cali_position = sp.do_step(cali_coord, speed=100)
    offset = list(sp.offset)
    current_coord = [[62, 0, -30], [62, 0, -30], [62, 0, -30], [62, 0, -30]]
   
    while True:
        print(cali_print_template)
        leg = input("Select calibration leg [1/2/3/4/q]: ")
        if leg == "q":
            break
        if leg not in ["1","2","3","4"]:
            continue
        leg = int(leg)-1
        print('Use "W", "A", "S", "D", "I", "K" to adjust the leg, "Space" to confirm')
        while True:
            key = readkey()
            
            if key == "w":
                current_coord[leg][1] += 1
            elif key == "s":
                current_coord[leg][1] -= 1
            elif key == "a":
                current_coord[leg][0] += 1
            elif key == "d":
                current_coord[leg][0] -= 1
            elif key == "i":
                current_coord[leg][2] += 1
            elif key == "k":
                current_coord[leg][2] -= 1
            elif key == " ":
                print("current_position = %s"%current_position)
                tmp = [current_position[i] - cali_position[i] + offset[i] for i in range(len(current_position))]
                offset[leg*3:(leg + 1)*3] = tmp[leg*3:(leg + 1)*3]
                print("offset: %s"%offset)
                current_coord[leg] = [62, 0, -30]
                sp.set_offset(offset)
                break
            else:
                print("None")
            current_position = sp.do_step(current_coord, speed=100)
            time.sleep(0.05)
            
if __name__ == "__main__":
    cali_helper()