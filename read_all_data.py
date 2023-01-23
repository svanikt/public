'''!
  @file read_all_data.py
  @brief Through the example, you can get the sensor data by using getSensorData:
  @n     get all data of magnetometer, gyroscope, accelerometer.
  @n     With the rotation of the sensor, data changes are visible.
  @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [luoyufeng] (yufeng.luo@dfrobot.com)
  @maintainer [Fary](feng.yang@dfrobot.com)
  @version  V1.0
  @date  2021-10-20
  @url https://github.com/DFRobot/DFRobot_BMX160
'''
import sys

sys.path.append('../../')
import time
from DFRobot_BMX160 import BMX160

bmx = BMX160(1)

# begin return True if succeed, otherwise return False
while not bmx.begin():
    time.sleep(2)


def main():
    while True:
        data = bmx.get_all_data()
        time.sleep(1)
        print("magn: x: {0:.2f} uT, y: {1:.2f} uT, z: {2:.2f} uT".format(data[0], data[1], data[2]))
        print("gyro  x: {0:.2f} g, y: {1:.2f} g, z: {2:.2f} g".format(data[3], data[4], data[5]))
        print("accel x: {0:.2f} m/s^2, y: {1:.2f} m/s^2, z: {2:.2f} m/s^2".format(data[6], data[7], data[8]))
        print(" ")


# Fast Offset Compensation of gyroscope and accelerometer
def FastOffsetCompensation():
try:
    bmx.write_bmx_reg(bmx._BMX160_FOC_CONF_ADDR, 0x7F) 
except:
    return "BMX160 Error: couldn't configure fast offset calibration"
try:

    bmx.write_bmx_reg(bmx._BMX160_COMMAND_REG_ADDR,0x03)
except:
    return "Error start fast offset compensation BMX160"

time.sleep(0.5) # wait time for FOC to finish

try:
    stat = bmx.read_bmx_reg(bmx._BMX160_STATUS_ADDR)
except:
    return "BMX160 Error: Reading Status Byte after FOC"

if stat & bmx._BMX160_STATUS_ADDR != 0x8:
    return "BMX160 Error: Couldn't complete FOC"

return None

# Enable Offset Compensation for gyroscope and accelerometer
def EnableOffsetCompensation():
try:
    # Get the OFFSET byte that also holds the 9:8 bits of the gyro offsets, we don't want to disturb those bits
    stat = bmx.read_bmx_reg(bmx._BMX160_OFFSET_CONF_ADDR)
except:
    return "BMX160 Error: Reading Offset config byte"

try: 
    bmx.write_bmx_reg(bmx._BMX160_OFFSET_CONF_ADDR, stat|0x80)
except:
    return "BMX160 Error: Couldn't enable offset"

try:
    stat = bmx.read_bmx_reg(bmx._BMX160_OFFSET_CONF_ADDR)
except:
    return "BMX160 Error: Reading Offset config byte"

return None


if __name__ == "__main__":
    main()
