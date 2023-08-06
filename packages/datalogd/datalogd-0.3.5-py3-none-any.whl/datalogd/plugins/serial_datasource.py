import asyncio
import logging

import json

from datalogd import parse_dot_json
from datalogd import DataSource

try:
    import serial, serial.tools.list_ports, serial.threaded, serial_asyncio
except ModuleNotFoundError:
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.warning("Serial modules not found. Install with \"pip install pyserial pyserial-asyncio\" or similar.")
else:
    # Required modules present, continue loading rest of this module

    class SerialDataSource(DataSource):
        """
        Receive data from an Arduino connected via a serial port device.

        .. container:: toggle

            .. container:: header

                See the ``datalog_arduino.ino`` sketch for matching code to run
                on a USB-connected Arduino.

            .. literalinclude:: ../../../arduino/datalog/datalog.ino
                :language: c++
                :caption: ``datalog.ino``

        Other serial-connected devices should work with this class if they conform to the expected
        communications protocol. Message data should be encoded in a JSON format. For example

        .. code-block::

            {"board":"A","timestamp":"1601251","message":"measurement","data":[{"type":"temperature","source":"A","id":"A_TC0","value":"20.25","units":"C"}]}

        which describes a single temperature measurement data point, encapsulated by a message
        header. Note that the values encoded in the ``"value"`` field will be attempted to be
        decoded using the same logic as :data:`~datalogd.parse_dot_json`, so that ``"20.25"`` will
        be interpreted as the equivalent python float, and special values such as ``None`` and
        ``inf`` are supported.

        If the connection to the serial device cannot be established or is interrupted, regular
        reattempts will be performed. Note that this means an exception will not be raised if the
        serial device cannot be found.

        :param port:     Path of serial device to use. A partial name to match
            can also be provided, such as "usb".
        :param board_id: ID label provided by the Arduino data logging board, to
            select a particular device in case multiple boards are connected.
        """

        class SerialHandler(serial.threaded.LineReader):
            """
            A class used as a :mod:`asyncio` :class:`~asyncio.Protocol` to handle
            lines of text received from the serial device.

            :param parent: The parent :class:`~datalogd.plugins.serial_datasource.SerialDataSource` class.
            """
            def __init__(self, parent):
                super().__init__()
                self.parent = parent

            def handle_line(self, line):
                """
                Accept one line of text, parse it to extract data, and pass the
                data on to any connected sinks.

                :param line: Line of text to process.
                """
                try:
                    j = json.loads(line)
                    if j["message"] == "measurement":
                        self.parent.log.debug(f"Received: {j['data']}")
                        # All data is in string form, attempt to convert values to something more appropriate
                        try:
                            for d in j["data"]:
                                if "value" in d.keys():
                                    d["value"] = parse_dot_json(d["value"])
                        except Exception as ex:
                            self.parent.log.warning("Unable to parse serial data.", exc_info=True)
                        self.parent.send(j["data"])
                except Exception as ex:
                    raise RuntimeError(f"Error interpreting serial data: {ex}")

            def connection_lost(self, exc):
                self.parent.log.warning("Serial connection lost, will attempt to reconnect.")
                self.parent._connection_task = self.parent.loop.create_task(self.parent._connect_serial_port())


        def __init__(self, sinks=[], port="", board_id=None):
            super().__init__(sinks=sinks)
            self.log = logging.getLogger("SerialDataSource")
            self.port = port
            self.sp = None
            self.board_id = board_id
            # Get reference to event loop and schedule task (but loop probably isn't started yet)
            self.loop = asyncio.get_event_loop()
            self._connection_task = self.loop.create_task(self._connect_serial_port(), name="SerialDataSource Connector")


        async def _connect_serial_port(self):
            """
            Coroutine to attempt to find and connect to device over serial port.
            """
            while True:
                # Loop continuously attempting to connect to correct serial device
                self.sp = None
                # Get list of available serial ports (matching given port name)
                portlist = list(serial.tools.list_ports.grep(self.port))
                if len(portlist) == 0:
                    if self.port == "":
                        self.log.warning("No serial ports found.")
                    else:
                        self.log.warning(f"No serial ports found matching \"{self.port}\"")
                
                # Iterate though serial ports looking for requested logging board
                for p in portlist:
                    try:
                        self.sp = serial.Serial(p.device, 115200, timeout=2)
                        # Read and discard potentially partial line
                        self.sp.readline()
                        # Read and attempt json decode of next (complete) line
                        j = json.loads(self.sp.readline().decode("ascii").strip())
                        if j["board"] and j["timestamp"] and j["message"]:
                            # Looks like one of our logging boards
                            if self.board_id is None or j["board"] == str(self.board_id):
                                self.log.info(f"Found board \"{j['board']}\" at {p.device}")
                                break
                            else:
                                self.log.info(f"Found board \"{j['board']}\" at {p.device} (but is not requested board \"{self.board_id}\")")
                                self.sp.close()
                                self.sp = None
                                continue
                    except Exception as ex:
                        # Error opening serial device, or not a logging board
                        self.log.info(f"Error querying board at {p.device} (port error or received invalid data)")
                        try:
                            self.sp.close()
                        except:
                            pass
                        self.sp = None

                # We should now have opened the serial port to requested board...
                if self.sp is None:
                    # ...but failed, so try again in a little while
                    try:
                        await asyncio.sleep(5.0)
                    except asyncio.CancelledError:
                        self.log.info("Serial connection attempt cancelled.")
                        break
                else:
                    # All seems OK, start the serial reader coroutine and stop connection attempts
                    asyncio.create_task(self._create_reader_coroutine(), name="SerialDataSource Reader")
                    break


        async def _create_reader_coroutine(self):
            """
            Coroutine to create the serial port transport and protocol class instances.
            """
            protocol = self.SerialHandler(parent=self)
            transport = serial_asyncio.SerialTransport(self.loop, protocol, self.sp)
            return (transport, protocol)


        def close(self):
            """
            Close the serial port connection.
            """
            if not self.sp is None:
                try:
                    self.sp.close()
                finally:
                    self.sp = None
