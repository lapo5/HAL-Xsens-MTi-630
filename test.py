import time

import xsens_MTi630
import numpy as np
import sys

if __name__ == "__main__":
    imu = xsens_MTi630.HAL()
    if not imu.init("can0"):
        sys.exit(1)
    rpy_ned = np.ndarray(shape=(3, 1), dtype=np.float32)

    imu.get_rpy_ned(rpy_ned)

    while True:
        imu.get_rpy_ned(rpy_ned)
        print("Received: {0}".format(rpy_ned))
