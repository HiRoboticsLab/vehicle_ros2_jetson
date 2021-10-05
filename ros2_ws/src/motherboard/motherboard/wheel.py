import json
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray


class Wheel(Node):

    def __init__(self, sender):
        super().__init__('wheel')
        self.listener_wheel = self.create_subscription(Int32MultiArray, 'cmd_wheel', self.on_receive_msg, 10)
        self.talker_wheel = self.create_publisher(Int32MultiArray, 'wheel', 10)
        self.sender = sender

    def on_receive_msg(self, msg):
        self.get_logger().info('receive cmd --> wheel : "%s"' % msg)
        try:
            data = msg.data
            left = data[0]
            right = data[1]
            obj = {
                'to': 'wheel',
                'data': [left, right]
            }
            # stm32接收换行表示结尾
            json_str = json.dumps(obj) + "\r\n"
            self.sender(json_str)
        except Exception as e:
            self.get_logger().error('%s' % e)

    def report(self, array_wheel):
        # self.get_logger().info('report wheel : "%s"' % array_wheel)
        try:
            msg_wheel = Int32MultiArray()
            msg_wheel.data = array_wheel
            self.talker_wheel.publish(msg_wheel)
        except Exception as e:
            self.get_logger().error('%s' % e)
        
