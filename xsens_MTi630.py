import can
import struct
import numpy as np


class HAL:
    init = False

    def __init__(self, channel="can0"):
        pass

    def init(self, channel="can0"):
        self.can0 = can.interface.Bus(channel=channel, bustype='socketcan_ctypes')
        self.init = True
        return True

    def get_rpy_ned(self, ned):
        if not self.init:
            raise Exception("XSENS MTI630 HAL not initialized")
        while True:
            msg = self.can0.recv(0.1)
            if msg is None:
                continue
            if msg.arbitration_id != 0x22:
                continue
            (roll, pitch, yaw) = struct.unpack(">hhh", msg.data)
            enu_roll = roll * 0.0078
            enu_pitch = pitch * 0.0078
            enu_yaw = yaw * 0.0078
            ned[0, 0] = ned_roll = - enu_pitch
            ned[1, 0] = ned_pitch = enu_roll
            ned[2, 0] = ned_yaw = -enu_yaw
            return True

    def get_rot(self, rpy_ned):
        return self.get_rpy_ned(rpy_ned)

    def has_rot(self):
        return True

    def has_raw(self):
        return False

    def has_mag(self):
        return False

