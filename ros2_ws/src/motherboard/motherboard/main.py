import json
import rclpy
import serial
import threading
from rclpy.executors import SingleThreadedExecutor
import traceback

from .light import Light
from .esp import Esp
from .wheel import Wheel
from .imu import Imu
from .pid import PID

# 临时变量
light = None
esp = None
wheel = None
imu = None
pid = None

# 串口初始化
# serial_port = {}
serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)


# 写串口
def write_serial(json_str):
    serial_port.write(json_str.encode())


# 读串口
def read_serial():
    while True:
        try:
            if serial_port.inWaiting() > 0:
                # 读取串口数据
                data = serial_port.readline()
                # 可以去掉b与‘符号
                json_str = str(data, encoding="ascii")
                # print(json_str)
                ok, obj = is_json(json_str)

                if ok:
                    array_wheel = obj['wheel']
                    wheel.report(array_wheel)

                    array_ypr = obj['ypr']
                    array_quaternion = obj['quaternion']
                    array_accel = obj['accel']
                    imu.report_ypr(array_ypr)
                    imu.report_imu(array_ypr, array_quaternion, array_accel)

        except Exception as e:
            traceback.print_exc()
            print('Serial receive error')

# 主函数
def main(args = None):
    global light, esp, wheel, imu, pid
    # !!! 顺序不要乱改 !!!
    # ROS初始化
    rclpy.init(args = args)
    # 倒入类
    light = Light(write_serial)
    esp = Esp(write_serial)
    wheel = Wheel(write_serial)
    imu = Imu()
    pid = PID(write_serial)
    # 启动串口接收
    thread = threading.Thread(target=read_serial, args=())
    # 为了解决程序退出线程不退出的问题
    thread.setDaemon(True)
    thread.start()
    # 在主线程中运行所有节点
    executor = SingleThreadedExecutor()
    # 添加节点
    executor.add_node(light)
    executor.add_node(esp)
    executor.add_node(wheel)
    executor.add_node(imu)
    executor.add_node(pid)
    try:
        executor.spin()
    finally:
        # 释放资源占用
        executor.shutdown()
        light.destroy_node()
        esp.destroy_node()
        wheel.destroy_node()
        imu.destroy_node()
        pid.destroy_node()



# json判断
def is_json(value):
    try:
        json_object = json.loads(value)
        return True, json_object
    except ValueError as e:
        return False
