import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import input_interfaces.racetechnology_imu06.racetechnology_imu06 as racetechnology_imu06
import input_interfaces.xsens_MTi28A.xsens_MTi28A as xsens_MTi28A
import madgwick
import time
import numpy as np
from scipy.spatial.transform import Rotation as R
import open3d as o3d

if __name__ == "__main__":
    # imu = racetechnology_imu06.HAL("/dev/ttyUSB0")
    imu = xsens_MTi28A.HAL(xsens_MTi28A.Mode.OrientationEstimate, "/dev/ttyUSB0")
    if not imu.init():
        sys.exit(1)

    v = o3d.visualization.Visualizer()
    v.create_window()

    origin_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=20, origin=[0, 0, 0])
    sensor_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=20, origin=[0, 0, 0])
    v.add_geometry(origin_frame)
    v.add_geometry(sensor_frame)

    np.set_printoptions(precision=4)
    np.set_printoptions(suppress=True)

    tf = np.ndarray(shape=(3, 1), dtype=np.float32)

    while True:
        if not imu.get_rot(tf):
            continue
        else:
            break
    prev = R.from_matrix(tf)

    count = 0
    while True:
        if not imu.get_rot(tf):
            continue
        t = int(time.time() * 1e6)
        if count == 5:
            rot = R.from_matrix([tf[0, 0], tf[1, 0], tf[2, 0]])
            sensor_frame.rotate((prev.inv() * rot).as_matrix(), center=(0, 0, 0))
            v.update_geometry(sensor_frame)

            v.poll_events()
            v.update_renderer()

            prev = rot
            count = 0
        count = count + 1
