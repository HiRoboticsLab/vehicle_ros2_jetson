import json
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, MultiArrayDimension
from sensor_msgs.msg import Imu as MsgImu
import math


class Imu(Node):

    def __init__(self):
        super().__init__('imu')
        self.talker_imu_ypr = self.create_publisher(Float64MultiArray, 'imu_ypr', 10)
        self.talker_imu = self.create_publisher(MsgImu, 'imu', 10)
        # 记录提交时间
        self.last_time = self.get_clock().now()
        self.last_angle = 0

    def report_ypr(self, array_ypr):
        # self.get_logger().info('report array_ypr : "%s"' % array_ypr)
        try:
            msg_ypr = Float64MultiArray()
            thing = MultiArrayDimension()
            thing.size = 1
            thing.stride = 1
            thing.label = "y"
            msg_ypr.layout.dim.append(thing)
            thing.label = "p"
            msg_ypr.layout.dim.append(thing)
            thing.label = "r"
            msg_ypr.layout.dim.append(thing)
            msg_ypr.data =  [array_ypr[0] * 1.0, array_ypr[1] * 1.0, array_ypr[2] * 1.0]
            self.talker_imu_ypr.publish(msg_ypr)
        except Exception as e:
            self.get_logger().error('%s' % e)

    def report_imu(self, array_ypr, array_quaternion, array_linear_acceleration):
        # self.get_logger().info('report array_ypr : "%s"' % array_ypr)
        # self.get_logger().info('report array_quaternion : "%s"' % array_quaternion)
        # self.get_logger().info('report linear_acceleration : "%s"' % linear_acceleration)
        try:
            current_time = self.get_clock().now()
            delta_time = (current_time - self.last_time).to_msg().nanosec / 1000 / 1000 
            # 计算变换弧度
            angle = array_ypr[0] * (-1.0)
            delta_angle = angle - self.last_angle
            delta_radian = delta_angle / 360 * 2 * math.pi
            self.last_angle = angle
            
            # ROS数据封装
            imu = MsgImu()

            imu.header.stamp = current_time.to_msg()
            imu.header.frame_id = "imu_link"

            imu.orientation.w =  array_quaternion[0] * 1.0
            imu.orientation.x =  array_quaternion[1] * 1.0
            imu.orientation.y =  array_quaternion[2] * 1.0
            imu.orientation.z =  array_quaternion[3] * 1.0

            # imu.angular_velocity.x = 0 * 1.0
            # imu.angular_velocity.y = 0 * 1.0
            imu.angular_velocity.z = delta_radian * 20 * 1.0

            imu.linear_acceleration.x = array_linear_acceleration[0] * 1.0
            imu.linear_acceleration.y = array_linear_acceleration[1] * 1.0
            imu.linear_acceleration.z = array_linear_acceleration[2] * 1.0

            self.talker_imu.publish(imu)

            self.last_time = current_time

        except Exception as e:
            self.get_logger().error('%s' % e)
