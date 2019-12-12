from ezblock import PWM, Servo
#from ezblock import __PRINT__ as print
import time
import math

class Robot():
    move_list = {}
    PINS = [None, "P0","P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","P11"]
    # PINS = [None, "D0","D1","D2","D3","D6","D7","A8","A9","A10","A11","A12","A13"]
    def __init__(self, pin_list, group=4):
        self.pin_list = []
        for i in range(0, len(pin_list), group):
            _pin_list = pin_list[i:i+group]
            for pin in _pin_list:
                pwm = PWM(self.PINS[pin])
                servo = Servo(pwm)
                servo.angle(0)
                self.pin_list.append(servo)
            time.sleep(0.2)
        self.pin_num = len(pin_list)
        self.origin_positions = self.new_list(0)
        self.offset = self.new_list(0)
        self.servo_positions = self.new_list(0)
        self.servo_move = self.servo_move_bak_2

    def new_list(self, default_value):
        _ = []
        for i in range(self.pin_num):
            _.append(default_value)
        return _

    def angle_list(self, angle_list):
        for i in range(self.pin_num):
            self.pin_list[i].angle(angle_list[i])

    def servo_write_all(self, angles):
        rel_angles = []  # ralative angle to home
        for i in range(self.pin_num):
            rel_angles.append(self.origin_positions[i] + angles[i] + self.offset[i])
            # rel_angles.append(angles[i])
            # print(rel_angles)
        self.angle_list(rel_angles)

    # def servo_move_bak_1(self, targets, speed=50):
    #     '''
    #         calculate the max delta angle, multiply by 2 to define a max_step
    #         loop max_step times, every servo add/minus 1 when step reaches its adder_flag
    #     '''
    #     delta = []
    #     absdelta = []
    #     adder_flag = []
    #     max_step = 0

    #     for i in range(self.pin_num):
    #         value = targets[i] - self.servo_positions[i]
    #         delta.append(value)
    #         absdelta.append(abs(value))

    #     max_step = abs(max(absdelta))

    #     if max_step != 0:
    #         for i in range(self.pin_num):
    #             if abs(delta[i]) != 0:
    #                 adder_flag.append(int(max_step / abs(delta[i])))
    #             else:
    #                 adder_flag.append(0)

    #         for step in range(max_step):
    #             for j in range(self.pin_num):
    #                 if adder_flag[j] != 0 and step % adder_flag[j] == 0 and self.servo_positions[j] != targets[j]:
    #                             self.servo_positions[j] = int(self.servo_positions[j] + (delta[j] / abs(delta[j])))
    #             self.servo_write_all(self.servo_positions)
    #             time.sleep((int(21-speed/(100/10)))/1000)

    def servo_move_bak_2(self, targets, speed=50):
        '''
            calculate the max delta angle, multiply by 2 to define a max_step
            loop max_step times, every servo add/minus 1 when step reaches its adder_flag
        '''
        speed = max(0, speed)
        speed = min(100, speed)
        delta = []
        absdelta = []
        max_step = 0
        steps = []

        for i in range(self.pin_num):
            value = targets[i] - self.servo_positions[i]
            delta.append(value)
            absdelta.append(abs(value))

        max_step = int(1*max(absdelta))
        if max_step != 0:
            for i in range(self.pin_num):
                step = float(delta[i])/max_step
                steps.append(step)

            for _ in range(max_step):
                for j in range(self.pin_num):
                    self.servo_positions[j] += steps[j]
                self.servo_write_all(self.servo_positions)
                #5~5005us
                t = (100-speed)*50+5
                time.sleep(t/100000)

    def do_action(self,motion_name, step=1, speed=50):
        for i in range(step):
            for motion in self.move_list[motion_name]:
                self.servo_move(motion, speed)

    def set_offset(self,offset_list):
        self.offset = offset_list
        self.reset() 


    def reset(self,):
        self.servo_positions = self.new_list(0)
        self.servo_write_all(self.servo_positions)

    def soft_reset(self,):
        self.servo_positions = self.new_list(0)
        self.servo_move(self.servo_positions)
