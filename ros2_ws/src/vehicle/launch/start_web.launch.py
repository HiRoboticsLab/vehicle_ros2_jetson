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

        Node(
            package = 'rosbridge_server',
            executable = 'rosbridge_websocket',
            parameters = [
                {
                    "port": 9090,
                    "address": "", 
                    "retry_startup_delay": 5.0,
                    "fragment_timeout": 600,
                    "delay_between_messages": 0,
                    "max_message_size": 10000000,
                    "unregister_timeout": 10.0,
                    "use_compression": False,

                    "topics_glob": "",
                    "services_glob": "",
                    "params_glob": "",

                    "bson_only_mode": False,
                }
            ]
        ),

        Node(
            package = 'rosapi',
            executable = 'rosapi_node',
            parameters = [
                {
                    "topics_glob": "",
                    "services_glob": "",
                    "params_glob": "",
                }
            ]
        ),

        PushRosNamespace('vehicle'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([lidar_pkg_dir, '/rplidar_launch.py']), 
            launch_arguments={'frame_id': 'base_scan', 'serial_baudrate': '256000'}.items(),
            # launch_arguments={'frame_id': 'base_scan'}.items(),
        ),
    ])