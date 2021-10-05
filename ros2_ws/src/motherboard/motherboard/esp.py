import json
from rclpy.node import Node
from std_msgs.msg import String


class Esp(Node):

    def __init__(self, sender):
        super().__init__('esp')
        self.listener_esp = self.create_subscription(String, 'cmd_esp', self.on_receive_msg, 10)
        self.sender = sender

    def on_receive_msg(self, msg):
        self.get_logger().info('receive cmd --> esp : "%s"' % msg)
        try:
            obj = json.loads(msg.data.replace("\'", "\""))
            obj["to"] = "esp"
            # stm32接收换行表示结尾
            json_str = json.dumps(obj) + "\r\n"
            self.sender(json_str)
        except Exception as e:
            self.get_logger().error('%s' % e)