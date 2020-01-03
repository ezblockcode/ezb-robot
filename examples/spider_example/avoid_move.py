from spider import Spider
from ezblock import Pin
from ultrasonic import Ultrasonic

us = Ultrasonic(Pin('D0'), Pin('D1'))

def aviod_move(ref):
    sp = Spider([1,2,3,4,5,6,7,8,9,10,11,12])
    while True:
        distance = us.get_distance()
        if distance > ref or distance == -2:
            sp.do_action("forward", step=1, speed=100)
        else:
            sp.do_action("turn right", step=2, speed=100)
        
if __name__ == '__main__':
    aviod_move(35)