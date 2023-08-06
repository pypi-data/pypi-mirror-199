import asyncio
import logging
from enum import Enum

from datalogd import DataSource

try:
    import pyvisa
    from ThorlabsPM100 import ThorlabsPM100
except ModuleNotFoundError:
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("ThorlabsPM100 and/or visa module not found. Install it with \"pip install pyvisa pyvisa-py pyusb ThorlabsPM100\" or similar. A VISA backend must also be present, use pyvisa-py if the native NI libraries are not installed.")
else:
    # Required modules present, continue loading rest of this module

    class ThorlabsPMDataSource(DataSource):
        """
        Provide data from a Thorlabs laser power meter.

        This uses the VISA protocol over USB. On Linux, read/write permissions to the power meter
        device must be granted. This can be done with a udev rule such as:

        .. code-block:: none
            :caption: ``/etc/udev/rules.d/52-thorlabs-pm.rules``

            # Thorlabs PM100D
            SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1313", ATTRS{idProduct}=="8078", OWNER="root", GROUP="usbusers", MODE="0664"
            # Thorlabs PM400
            SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1313", ATTRS{idProduct}=="8075", OWNER="root", GROUP="usbusers", MODE="0664"


        where the ``idVendor`` and ``idProduct`` fields should match that listed from running
        ``lsusb``. The ``usbusers`` group must be created and the user added to it:

        .. code-block:: bash

            groupadd usbusers
            usermod -aG usbusers yourusername

        A reboot will then ensure permissions are set and the user is a part of the group (or use ``udevadm control --reload`` and re-login).
        To check the permissions have been set correctly, get the USB bus and device numbers from the output of ``lsusb``. For example

        .. code-block:: none
            :caption: ``lsusb``
        
            Bus 001 Device 010: ID 1313:8075 ThorLabs PM400 Handheld Optical Power/Energy Meter
        
        the bus ID is 001 and device ID is 010. Then list the device using ``ls -l /dev/bus/usb/[bus ID]/[device ID]``

        .. code-block:: none
            :caption: ``ls /dev/bus/usb/001/010 -l``

            crw-rw-r-- 1 root usbusers 189, 9 Mar 29 13:19 /dev/bus/usb/001/010
        
        The middle "rw" and the "usbusers" indicates read-write permissions enabled to any user in
        the usbusers group. You can check which groups your current user is in using the ``groups``
        command.

        Note that you may also allow read-write access to any user (without having to make a
        usbusers group) by changing the lines in the udev rule to ``MODE="0666"`` and removing the
        ``GROUP="usbusers"`` part.

        :param serial_number: Serial number of power meter to use. If ``None``, will use the first device found.
        :param usb_vid: USB vendor ID (0x1313 or 4883 for Thorlabs).
        :param usb_pid: USB product ID (0x8078 for PM100D, 0x8075 for PM400).
        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], serial_number=None, usb_vid="0x1313", usb_pid="0x8078", interval=1.0):
            super().__init__(sinks=sinks)
            self.log = logging.getLogger("ThorlabsPMDataSource")
            self.interval = interval
            self.rm = pyvisa.ResourceManager()
            if self.rm.visalib.library_path in ("py", "unset"):
                # Native python VISA library, USB VID and PID in decimal, has extra field
                # Here, 4883 == vendorID == 0x1313, 32888 == productID == 0x8078
                try:
                    usb_vid = int(usb_vid, 16)
                    usb_pid = int(usb_pid, 16)
                except Exception as ex:
                    pass
                res = self.rm.list_resources("USB0::{}::{}::{}::0::INSTR".format(usb_vid, usb_pid, serial_number if serial_number else "?*"))
            else:
                # NI VISA library (probably) in use, USB VID and PID are in hex, also extra field missing
                res = self.rm.list_resources("USB0::{}::{}::{}::INSTR".format(usb_vid, usb_pid, serial_number if serial_number else "?*"))
            if len(res) == 0:
                self.log.warning("Could not find a Thorlabs PM device{}. Check USB device permissions and usb_pid parameter.".format(f" with serial {serial_number}" if serial_number else ""))
                self.inst = None
                self.pm = None
                self.serial_number = None
            else:
                try:
                    self.inst = self.rm.open_resource(res[0])
                    self.pm = ThorlabsPM100(self.inst)
                    self.serial_number = self.inst.resource_info.resource_name.split("::")[3]
                    self.log.info(f"Initialised Thorlabs PM device: {self.serial_number}.")
                    # Queue first call of update routine
                    asyncio.get_event_loop().call_soon(self._read_power)
                except Exception as ex:
                    self.log.warning("Could not initialise Thorlabs PM device: {}".format(ex))

        def close(self):
            """
            Close the connection to the power meter.
            """
            self.rm.close()

        def _read_power(self):
            """
            Read power and send data to any connected sinks.
            """
            loop = asyncio.get_event_loop()
            try:
                data = {"type": "power", "source": "ThorlabsPM", "id": self.serial_number, "value": self.pm.read}
                self.send(data)
            except Exception as ex:
                self.log.warning("Could not read power from Thorlabs PM device.")
            # Reschedule next update
            loop.call_later(self.interval, self._read_power)


    class ThorlabsPM100DataSource(ThorlabsPMDataSource):
        """
        Provide data from a Thorlabs PM100 laser power meter.

        This is a wrapper around
        :class:`~datalogd.plugins.thorlabspm100_datasource.ThorlabsPMDataSource` with the
        appropriate USB PID used as default. See its documentation regarding configuring permissions
        for accessing the USB device.

        :param serial_number: Serial number of power meter to use. If ``None``, will use the first
            device found.
        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], serial_number=None, interval=1.0):
            super().__init__(sinks=sinks, usb_vid="0x1313", usb_pid="0x8078", serial_number=serial_number, interval=interval)


    class ThorlabsPM400DataSource(ThorlabsPMDataSource):
        """
        Provide data from a Thorlabs PM400 laser power meter.

        This is a wrapper around
        :class:`~datalogd.plugins.thorlabspm100_datasource.ThorlabsPMDataSource` with the
        appropriate USB PID used as default. See its documentation regarding configuring permissions
        for accessing the USB device.

        :param serial_number: Serial number of power meter to use. If ``None``, will use the first
            device found.
        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], serial_number=None, interval=1.0):
            super().__init__(sinks=sinks, usb_vid="0x1313", usb_pid="0x8075", serial_number=serial_number, interval=interval)