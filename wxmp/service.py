#!/usr/bin/env python3

import logging

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

from ble import (
    Advertisement,
    Characteristic,
    Service,
    Application,
    find_adapter,
    Descriptor,
    Agent,
)

import struct
import requests
import array
from enum import Enum

import sys
import uuid

from utils import restartBluezService, connWifi, connHotspot, getssid, getip, isHotspot

# ROS桥
import json
import roslibpy
topicMove = None
topicLight = None


MainLoop = None
try:
    from gi.repository import GLib

    MainLoop = GLib.MainLoop
except ImportError:
    import gobject as GObject

    MainLoop = GObject.MainLoop

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logHandler.setFormatter(formatter)
# filelogHandler = logging.FileHandler("logs.log")
# filelogHandler.setFormatter(formatter)
# logger.addHandler(filelogHandler)
logger.addHandler(logHandler)

mainloop = None

BLUEZ_SERVICE_NAME = "org.bluez"
GATT_MANAGER_IFACE = "org.bluez.GattManager1"
LE_ADVERTISEMENT_IFACE = "org.bluez.LEAdvertisement1"
LE_ADVERTISING_MANAGER_IFACE = "org.bluez.LEAdvertisingManager1"


class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.freedesktop.DBus.Error.InvalidArgs"


class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.NotSupported"


class NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.NotPermitted"


class InvalidValueLengthException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.InvalidValueLength"


class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = "org.bluez.Error.Failed"


def register_app_cb():
    logger.info("GATT application registered")


def register_app_error_cb(error):
    logger.critical("Failed to register application: " + str(error))
    mainloop.quit()


class VivaldiS1Service(Service):
    """
    Dummy test service that provides characteristics and descriptors that
    exercise various API functionality.
    """

    # ESPRESSO_SVC_UUID = "c6d04936-4878-5b80-822b-295f4eb3c3c4"
    ESPRESSO_SVC_UUID = "42e6db8c-3960-11ec-b400-0a80ff2603de"
    # ESPRESSO_SVC_UUID = str(uuid.uuid1())

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.ESPRESSO_SVC_UUID, True)
        self.add_characteristic(WifiCharacteristic(bus, 0, self))


class WifiCharacteristic(Characteristic):
    uuid = "8cbc505e-2b25-5604-9b14-cc4d75d19d4f"
    description = b"fuck"


    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index, self.uuid, ["encrypt-read", "encrypt-write"], service,
        )

        self.value = [0xFF]
        self.add_descriptor(CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        logger.debug("Wifi Read: " + repr(self.value))
        obj = {}
        obj['wlan'] = {}
        obj['wlan']['ssid'] = getssid()
        obj['wlan']['ip'] = getip()
        obj['wlan']['isap'] = isHotspot()
        return bytearray(json.dumps(obj), encoding="utf8")

    def WriteValue(self, value, options):
        # logger.debug("Wifi Write: " + repr(value))
        cmd = bytes(value).decode("utf-8")
        logger.debug(cmd)
        obj = json.loads(cmd)

        if 'move' in obj:
            result = [obj['move'][0], obj['move'][1]]
            # print(result)
            topicMove.publish(roslibpy.Message({'data': result}))
        if 'light' in obj:
            topicLight.publish(roslibpy.Message({'data': obj['light']}))
        if 'wlan' in obj:
            if obj['wlan'] == 'wifi':
                connWifi(obj['ssid'], obj['pwd'])
            if obj['wlan'] == 'ap':
                connHotspot(obj['pwd'])


class CharacteristicUserDescriptionDescriptor(Descriptor):
    """
    Writable CUD descriptor.
    """

    CUD_UUID = "2901"

    def __init__(
        self, bus, index, characteristic,
    ):

        self.value = array.array("B", characteristic.description)
        self.value = self.value.tolist()
        Descriptor.__init__(self, bus, index, self.CUD_UUID, ["read"], characteristic)

    def ReadValue(self, options):
        return self.value

    def WriteValue(self, value, options):
        if not self.writable:
            raise NotPermittedException()
        self.value = value


class VivaldiAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, "peripheral")
        self.add_manufacturer_data(
            0xFFFF, [0x70, 0x74],
        )
        self.add_service_uuid(VivaldiS1Service.ESPRESSO_SVC_UUID)

        self.add_local_name("hairuo vehicle")
        self.include_tx_power = True


def register_ad_cb():
    logger.info("Advertisement registered")


def register_ad_error_cb(error):
    logger.critical("Failed to register advertisement: " + str(error))
    mainloop.quit()


AGENT_PATH = "/com/punchthrough/agent"


def main():
    restartBluezService()

    global mainloop
    # ROS桥
    global topicMove, topicLight

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    # get the system bus
    bus = dbus.SystemBus()
    # get the ble controller
    adapter = find_adapter(bus)

    if not adapter:
        logger.critical("GattManager1 interface not found")
        return

    adapter_obj = bus.get_object(BLUEZ_SERVICE_NAME, adapter)

    adapter_props = dbus.Interface(adapter_obj, "org.freedesktop.DBus.Properties")

    # powered property on the controller to on
    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    # Get manager objs
    service_manager = dbus.Interface(adapter_obj, GATT_MANAGER_IFACE)
    ad_manager = dbus.Interface(adapter_obj, LE_ADVERTISING_MANAGER_IFACE)

    advertisement = VivaldiAdvertisement(bus, 0)
    obj = bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez")

    agent = Agent(bus, AGENT_PATH)

    app = Application(bus)
    app.add_service(VivaldiS1Service(bus, 2))

    mainloop = MainLoop()

    agent_manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    agent_manager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")

    ad_manager.RegisterAdvertisement(
        advertisement.get_path(),
        {},
        reply_handler=register_ad_cb,
        error_handler=register_ad_error_cb,
    )

    logger.info("Registering GATT application...")

    service_manager.RegisterApplication(
        app.get_path(),
        {},
        reply_handler=register_app_cb,
        error_handler=[register_app_error_cb],
    )

    agent_manager.RequestDefaultAgent(AGENT_PATH)

    # ROS桥
    ros_client = roslibpy.Ros(host='localhost', port=9090)
    ros_client.run()
    logger.info('Is ROS connected? ' + str(ros_client.is_connected))
    if ros_client.is_connected:
        topicMove = roslibpy.Topic(ros_client, '/vehicle/cmd_wheel', 'std_msgs/Int32MultiArray')
        topicLight = roslibpy.Topic(ros_client, '/vehicle/cmd_light', 'std_msgs/String')

    mainloop.run()
    # ad_manager.UnregisterAdvertisement(advertisement)
    # dbus.service.Object.remove_from_connection(advertisement)


if __name__ == "__main__":
    main()


'''
    # 工具函数
'''
# json判断
def is_json(value):
    try:
        json_object = json.loads(value)
        return True, json_object
    except ValueError as e:
        print(e)
        return False
