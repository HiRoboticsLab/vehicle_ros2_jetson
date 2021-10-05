import json
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class PID(Node):

    def __init__(self, sender):
        super().__init__('pid')
        self.listener_light = self.create_subscription(Float64MultiArray, 'cmd_pid', self.on_receive_msg, 10)
        self.sender = sender

    def on_receive_msg(self, msg):
        self.get_logger().info('receive cmd --> pid : "%s"' % msg)
        try:
            data = msg.data
            obj = {
                'to': 'pid',
                'data': [data[0], data[1], data[2]]
            }
            # stm32接收换行表示结尾
            json_str = json.dumps(obj) + "\r\n"
            self.sender(json_str)
        except Exception as e:
            self.get_logger().error('%s' % e)
        