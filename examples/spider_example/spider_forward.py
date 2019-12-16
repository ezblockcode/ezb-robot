from spider import Spider

sp = Spider([1,2,3,4,5,6,7,8,9,10,11,12])
sp.set_offset([15,-5,-7,  -7,-5,5,  10,5,-4,  -10,3,-5])
sp.do_action("forward",step=2,speed=100)
    