import cv2
import traceback
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from sensor_msgs.msg import Image, CompressedImage, CameraInfo
import numpy as np
import gi

# 必须带着“点”
from .cv_bridge import CvBridge
from .gst_camera import GstCamera


class CSICam(Node):
    def __init__(self):
        super().__init__('camera')
        # ROS节点
        # self.pub_camera_raw = self.create_publisher(Image, 'camera/raw', 10)
        self.pub_camera_compressed = self.create_publisher(CompressedImage, 'camera/compressed', 10)
        self.cvb = CvBridge()
        # 摄像头
        self.camera = GstCamera()
        self.camera.on_image(self.rev_image)
        self.camera.start()
        print("Camera Start")

    def rev_image(self, image):
        # img_msg = self.cvb.cv2_to_imgmsg(image)
        # img_msg.header.frame_id = "camera"
        # self.pub_camera_raw.publish(img_msg)

        img_msg_compressed = self.cvb.cv2_to_compressed_imgmsg(image)
        img_msg_compressed.header.frame_id = "camera"
        img_msg_compressed.header.stamp = self.get_clock().now().to_msg()
        self.pub_camera_compressed.publish(img_msg_compressed)


def main(args=None):
    rclpy.init(args=args)
    try:
        camera = CSICam()
        # Runs all callbacks in the main thread
        executor = SingleThreadedExecutor()
        # Add imported nodes to this executor
        executor.add_node(camera)
        try:
            # Execute callbacks for both nodes as they become ready
            executor.spin()
        finally:
            executor.shutdown()
            camera.camera.stop()
            camera.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()