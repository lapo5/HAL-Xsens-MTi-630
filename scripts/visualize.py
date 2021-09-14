import time

import xsens_MTi630
import numpy as np
import sys
import open3d as o3d
from scipy.spatial.transform import Rotation as R

if __name__ == "__main__":
    imu = xsens_MTi630.HAL()
    if not imu.init("can0"):
        sys.exit(1)
    rpy_ned = np.ndarray(shape=(3, 1), dtype=np.float32)

    v = o3d.visualization.Visualizer()
    v.create_window()

    origin_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=20, origin=[0, 0, 0])
    sensor_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=20, origin=[0, 0, 0])
    v.add_geometry(origin_frame)
    v.add_geometry(sensor_frame)

    tf = np.eye(3, dtype=np.float32)

    imu.get_rpy_ned(rpy_ned)
    t = int(time.time() * 1e6)
    r = rpy_ned[0, 0]
    p = rpy_ned[1, 0]
    y = rpy_ned[2, 0]
    prev = R.from_euler("xyz", [r, p, y], degrees=True)

    count = 0
    while True:
        imu.get_rpy_ned(rpy_ned)
        t = int(time.time() * 1e6)
        if count == 5:
            r = rpy_ned[0, 0]
            p = rpy_ned[1, 0]
            y = rpy_ned[2, 0]
            rot = R.from_euler("xyz", [r, p, y], degrees=True)
            sensor_frame.rotate((prev.inv() * rot).as_matrix(), center=(0, 0, 0))
            v.update_geometry(sensor_frame)

            v.poll_events()
            v.update_renderer()

            prev = rot
            count = 0
        count = count + 1
