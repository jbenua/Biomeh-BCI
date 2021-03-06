import asyncio
from asyncio import Queue
import numpy as np

sensor_bits = {
    'F3': {'value': 7},
    'FC5': {'value': 10},
    'AF3': {'value': 10},
    'F7': {'value': 4},
    'T7': {'value': 9},
    'P7': {'value': 7},
    'O1': {'value': 9},
    'O2': {'value': 11},
    'P8': {'value': 12},
    'T8': {'value': 6},
    'F8': {'value': 9},
    'AF4': {'value': 7},
    'FC6': {'value': 12},
    'F4': {'value': 3},
}


class MagicPacket:
    """
    Basic semantics for input bytes.
    """

    def __init__(self, data, sensors, model):
        """
        Initializes packet data. Sets the global battery value.
        Updates each sensor with current sensor value from the packet data.
        """
        self.raw_data = data
        self.battery = 40
        self.counter = 120
        self.gyro_x = data[29] - 106  # ord(data[29]) - 106
        self.gyro_y = data[30] - 105  # ord(data[30]) - 105
        self.old_model = model
        self.sensors = sensors

    def __repr__(self):
        """
        Returns custom string representation of the Emotiv Packet.
        """
        return 'EmotivPacket(counter=%i, battery=%i, gyro_x=%i, gyro_y=%i)' % (
            self.counter,
            self.battery,
            self.gyro_x,
            self.gyro_y)


class MagicEmotiv:
    def __init__(self, filter_hz=25):
        self.data_to_send = Queue()
        self.battery = 40
        self.packets = Queue()
        self.poll_interval = 1 / filter_hz
        self.running = True

    def set_filter(self, value):
        self.poll_interval = 1 / value

    async def setup(self):
        print("creating magic emotiv...")

    async def read_data(self):
        print("magic: running", self.running)
        while self.running:
            print("magic: running", self.running)
            print(self.data_to_send.qsize())
            s = {}
            for shift, sensor in enumerate(sorted(sensor_bits, reverse=True)):
                s[sensor] = {'quality': sensor_bits[sensor]['value']}
                s[sensor]['value'] = np.random.normal() + shift * 5

            packet = MagicPacket(
                b'Py2\x18\xe7\xb7\xdf\x8e\x86n;g\xbd\xc0\x00\x00\x02\x11(!`' +
                b'=\x80\x15\xecX\xc6 \xd9ii\x9e',
                s, False)
            self.packets.put_nowait(packet)
            self.data_to_send.put_nowait(packet)
            await asyncio.sleep(self.poll_interval)

    async def update_console(self):
        while self.running:
            packet = await self.packets.get()
            print(packet)
            await asyncio.sleep(self.poll_interval)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    a = MagicEmotiv()
    loop.run_until_complete(a.setup())
    a.running = True
    try:
        loop_tasks = [
            asyncio.ensure_future(a.read_data()),
            asyncio.ensure_future(a.update_console())
        ]
        finished, pending = loop.run_until_complete(asyncio.wait(loop_tasks))

    except KeyboardInterrupt:
        a.running = False
        for task in pending:
            task.cancel()
    loop.close()
    a.close()
