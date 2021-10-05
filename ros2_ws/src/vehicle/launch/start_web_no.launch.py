import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace

def generate_launch_description():

    lidar_pkg_dir = os.path.join(get_package_share_directory('rplidar_ros2'), 'launch')
    print(lidar_pkg_dir)

    return LaunchDescription([

        Node(
            package = 'adjust_date',
            namespace = 'vehicle',
            executable = 'start',
        ),

        Node(
            package = 'csi_camera',
            namespace = 'vehicle',
            executable = 'start',
        ),

        Node(
            package = 'motherboard',
            namespace = 'vehicle',
            executable = 'start',
        ),

        PushRosNamespace('vehicle'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([lidar_pkg_dir, '/rplidar_launch.py']), 
            launch_arguments={'frame_id': 'base_scan', 'serial_baudrate': '256000'}.items(),
            # launch_arguments={'frame_id': 'base_scan'}.items(),
        ),
    ])