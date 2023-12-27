import usb.core
import usb.util
import usb.control
import time
import array
import json


# Test by Arduino
VENDER = 0x16c0
PRODUCT = 0x27dd
CDC_COMM_INTF = 0
CDC_DATA_INTF = 1
EP_IN = 0x83
EP_OUT = 0x4


class LibusbSerial:

  def __init__(self, timeout=30):

    # The unit of libusb is millisecond
    self.timeout = timeout*1000

    self.dev = usb.core.find(idVendor=VENDER, idProduct=PRODUCT)
    if self.dev is None:
      raise ValueError('Device not found')

    print(self.dev.get_active_configuration())
    if self.dev.is_kernel_driver_active(CDC_DATA_INTF):
      self.dev.detach_kernel_driver(CDC_DATA_INTF)

    if self.dev.is_kernel_driver_active(CDC_COMM_INTF):
      self.dev.detach_kernel_driver(CDC_COMM_INTF)


    # Lock usb device
    usb.util.claim_interface(self.dev, CDC_DATA_INTF)
    usb.util.claim_interface(self.dev, CDC_COMM_INTF)

    # Get endpoint
    self.cfg = self.dev.get_active_configuration()

    self.intf = self.cfg[(1, 0)]
    self.ep_in = self.intf[0]

    # https://github.com/tytouf/libusb-cdc-example/blob/master/cdc_example.py
    # buad rate 115200 = 1C200
    self.dev.ctrl_transfer(0x21, 0x22, 0x01 | 0x02, CDC_COMM_INTF, None)
    self.dev.ctrl_transfer(0x21, 0x20, 0, CDC_COMM_INTF,
                  array.array('B', [0x00, 0xC2, 0x01, 0x00, 0x00, 0x00, 0x08]))

  def read(self):
    ret = self.ep_in.read(self.ep_in.wMaxPacketSize, self.timeout)
    return ret

  def write(self, text):
    self.dev.write(EP_OUT, text)


if __name__ == "__main__":
  ser = LibusbSerial()
  while True:
    print(ser.read())
    time.sleep(0.001)