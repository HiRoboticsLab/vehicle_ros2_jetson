import os
import logging
import subprocess
import socket
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


SYSTEM_PASSWORD = "jetbot"


def connWifi(ssid, pwd):
    if isHotspot():
        disconnHotspot()
    if check(ssid):
        delete(ssid)
    time.sleep(2)
    cmd = "echo '{}' | sudo -S nmcli device wifi connect '{}' password '{}'".format(SYSTEM_PASSWORD, ssid, pwd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    logger.info(tmp)
    if "Device 'wlan0' successfully activated" in tmp:
        logger.info('成功')
    else:
        logger.info('失败')

def check(ssid):
    exist = False
    cmd = "echo '{}' | sudo -S nmcli connection show".format(SYSTEM_PASSWORD)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    logger.info(tmp)
    if ssid in tmp:
        logger.info('already exist')
        exist = True
    return exist


def delete(ssid):
    cmd = "echo '{}' | sudo -S nmcli connection delete '{}'".format(SYSTEM_PASSWORD, ssid)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    logger.info(tmp)


def isHotspot():
    hotspotMode = False
    cmd = "echo '{}' | sudo -S nmcli connection show --active".format(SYSTEM_PASSWORD)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    if 'Hotspot' in tmp:
        logger.info('device is hotspot mode')
        hotspotMode = True
    return hotspotMode


def disconnHotspot():
    cmd = "echo '{}' | sudo -S nmcli connection down Hotspot".format(SYSTEM_PASSWORD)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    logger.info(tmp)


def connHotspot(pwd):
    delete("Hotspot")
    ssid = 'vehicle-{}'.format(getSerialNumber())
    cmd = "echo '{}' | sudo -S sudo nmcli dev wifi hotspot ssid '{}' password '{}'".format(SYSTEM_PASSWORD, ssid, pwd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    logger.info(tmp)
    setDefaultConn('Hotspot')


def setDefaultConn(ssid):
    cmd = "echo '{}' | sudo -S sudo nmcli connection modify '{}' autoconnect yes".format(SYSTEM_PASSWORD, ssid)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    logger.info(tmp)


def getSerialNumber():
    cmd = "echo '{}' | sudo -S cat /proc/device-tree/serial-number".format(SYSTEM_PASSWORD)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    logger.info(tmp)
    logger.info(tmp[-9:-1])
    return tmp[-9:-1]


def restartBluezService():
    cmd = "echo '{}' | sudo -S sudo /etc/init.d/bluetooth restart".format(SYSTEM_PASSWORD)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.wait()
    tmp = str(output.stdout.read(), encoding='utf-8')
    logger.info(tmp)


def getssid():
    result = ""
    if isHotspot():
        result = 'vehicle-{}'.format(getSerialNumber())
    else:
        cmd = "echo '{}' | sudo -S nmcli connection show --active".format(SYSTEM_PASSWORD)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()
        for i in output:
            data = str(i, encoding='utf-8')
            # logger.info(data)
            temp = ' '.join(data.split())
            array = temp.split(' ')
            if(array[3] == 'wlan0'):
                result = array[0]
    logger.info(result)
    return result


def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    result = s.getsockname()[0]
    logger.info(result)
    return result


# connWifi('HaiRuoTech', 'hairuotech')
# delete('HaiRuoTech')
# check('HaiRuoTech')
# getSerialNumber()
# connHotspot('12344321')
# restartBluezService()

# getssid()
# getip()
