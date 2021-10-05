import json
from rclpy.node import Node
from std_msgs.msg import String


class Light(Node):

    def __init__(self, sender):
        super().__init__('light')
        self.listener_light = self.create_subscription(String, 'cmd_light', self.on_receive_msg, 10)
        self.sender = sender

    def on_receive_msg(self, msg):
        self.get_logger().info('receive cmd --> light : "%s"' % msg)
        try:
            obj = {
                'to': 'light',
                'data': msg.data
            }
            # stm32接收换行表示结尾
            json_str = json.dumps(obj) + "\r\n"
            self.sender(json_str)
        except Exception as e:
            self.get_logger().error('%s' % e)
        
