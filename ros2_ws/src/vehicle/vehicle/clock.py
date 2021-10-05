# import traceback
# import rclpy
# from rclpy.node import Node
# from rclpy.executors import SingleThreadedExecutor
# from builtin_interfaces.msg import Time
# import threading
# import time


# class ClockPublisher(Node):

#     hz = 25

#     def __init__(self):
#         super().__init__('vehicle_clock')
#         # ROS节点
#         self.pub_colck = self.create_publisher(Time, '/clock', 10)
#         thread = threading.Thread(target = self.publish, args=())
#         # 为了解决程序退出线程不退出的问题
#         thread.setDaemon(True)
#         thread.start()


#     def publish(self):
#         while True:
#             try:
#                 msg = Time()
#                 msg = self.get_clock().now().to_msg()
#                 # msg.nanosec = self.get_clock().now().to_msg()
#                 self.pub_colck.publish(msg)
#                 time.sleep(1 / self.hz)
#             except Exception as e:
#                 self.get_logger().error('vehicle_time error')


# def main(args=None):
#     rclpy.init(args=args)
#     try:
#         clock = ClockPublisher()
#         # Runs all callbacks in the main thread
#         executor = SingleThreadedExecutor()
#         # Add imported nodes to this executor
#         executor.add_node(clock)
#         try:
#             # Execute callbacks for both nodes as they become ready
#             executor.spin()
#         finally:
#             executor.shutdown()
#             clock.destroy_node()
#     finally:
#         rclpy.shutdown()


# if __name__ == '__main__':
#     main()