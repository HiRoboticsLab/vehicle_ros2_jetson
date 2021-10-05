```shell
# 拉代码
# 进入ros2_ws/src执行
git clone -b ros2 https://github.com/slamtec/rplidar_ros.git

git clone https://github.com/RobotWebTools/rosbridge_suite
```

```shell
# 显示镜像
sudo docker images

# 创建镜像（需要进入Dockerfile路径下执行，注意“点”）
# sudo docker build -t ros2-vehicle .
sudo docker build -f Dockerfile.ROS2 -t ros2-vehicle .

# 删除镜像
sudo docker rmi ros2-vehicle
# 删除虚悬镜像（构建后）
sudo docker images 

# 查看docker容器
sudo docker ps -a
# 停止容器
sudo docker stop ros2
# 删除容器
sudo docker rm ros2


# 智能车启动正式命令
# sudo docker run -it -d --restart always --runtime nvidia --network host --privileged --device /dev/video* -v /dev/bus/usb:/dev/bus/usb -v /tmp/argus_socket:/tmp/argus_socket --name ros2 ros2-vehicle

sudo docker run -it -d --restart always --runtime nvidia --network host --privileged --device /dev/video* -v /dev/bus/usb:/dev/bus/usb -v /tmp/argus_socket:/tmp/argus_socket -v /home/jetbot/Desktop/vehicle/ros2_ws:/root/ros2_ws --name ros2 ros2-vehicle
```


```shell
# 解决CSI摄像头周围泛红的问题
# 下载camera-override.isp文件，解压到特定文件夹
wget http://www.waveshare.net/w/upload/e/eb/Camera_overrides.tar.gz
tar zxvf Camera_overrides.tar.gz
sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/
# 安装文件
sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp
sudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp
```


```shell
# 网页文件
sudo docker pull nginx

sudo docker run -it -d --restart always --network host -v /home/jetbot/Desktop/vehicle/web_page/dist:/usr/share/nginx/html --name webtool nginx
```

