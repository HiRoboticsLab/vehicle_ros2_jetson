import traceback
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import String
import subprocess


class AdjustDate(Node):

    def __init__(self):
        super().__init__('adjust_date')
        # ROS节点
        self.create_subscription(String, 'adjust_date', self.on_receive_msg, 10)


    def on_receive_msg(self, msg):
        self.get_logger().info('receive date --> "%s"' % msg)
        subprocess.call("date -s '" + msg.data + "'", shell = True)


def main(args = None):
    rclpy.init(args = args)
    date = AdjustDate()
    # Runs all callbacks in the main thread
    executor = SingleThreadedExecutor()
    # Add imported nodes to this executor
    executor.add_node(date)
    try:
        # Execute callbacks for both nodes as they become ready
        executor.spin()
    finally:
        executor.shutdown()
        date.destroy_node()
