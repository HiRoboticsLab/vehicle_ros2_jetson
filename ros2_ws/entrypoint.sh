# !/bin/bash
echo "start..."

colcon build

source install/setup.bash

export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

# ros2 launch vehicle start_web_no.launch.py 
ros2 launch vehicle start_web.launch.py 

exec "/bin/bash"
