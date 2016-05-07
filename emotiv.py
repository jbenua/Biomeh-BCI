try:
    import pywinusb.hid as hid

    windows = True
except:
    windows = False

import os
# from asyncio import Queue
from Crypto.Cipher import AES
from Crypto import Random
import time
import asyncio
from asyncio import Queue

from subprocess import check_output

sensorBits = {
    'F3': [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
    'FC5': [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9],
    'AF3': [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27],
    'F7': [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45],
    'T7': [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63],
    'P7': [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65],
    'O1': [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83],
    'O2': [
        140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121],
    'P8': [
        158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139],
    'T8': [
        160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157],
    'F8': [
        178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175],
    'AF4': [
        196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177],
    'FC6': [
        214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195],
    'F4': [
        216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213]
}
quality_bits = [
    99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]

g_battery = 0
tasks = Queue()

# this is useful for further reverse engineering for EmotivPacket
byte_names = {
    "saltie-sdk": [  # also clamshell-v1.3-sydney
                     "INTERPOLATED",
                     "COUNTER",
                     "BATTERY",
                     "FC6",
                     "F8",
                     "T8",
                     "PO4",
                     "F4",
                     "AF4",
                     "FP2",
                     "OZ",
                     "P8",
                     "FP1",
                     "AF3",
                     "F3",
                     "P7",
                     "T7",
                     "F7",
                     "FC5",
                     "GYRO_X",
                     "GYRO_Y",
                     "RESERVED",
                     "ETE1",
                     "ETE2",
                     "ETE3",
    ],
    "clamshell-v1.3-san-francisco": [  # amadi ?
                                       "INTERPOLATED",
                                       "COUNTER",
                                       "BATTERY",
                                       "F8",
                                       "UNUSED",
                                       "AF4",
                                       "T8",
                                       "UNUSED",
                                       "T7",
                                       "F7",
                                       "F3",
                                       "F4",
                                       "P8",
                                       "PO4",
                                       "FC6",
                                       "P7",
                                       "AF3",
                                       "FC5",
                                       "OZ",
                                       "GYRO_X",
                                       "GYRO_Y",
                                       "RESERVED",
                                       "ETE1",
                                       "ETE2",
                                       "ETE3",
    ],
    "clamshell-v1.5": [
        "INTERPOLATED",
        "COUNTER",
        "BATTERY",
        "F3",
        "FC5",
        "AF3",
        "F7",
        "T7",
        "P7",
        "O1",
        "SQ_WAVE",
        "UNUSED",
        "O2",
        "P8",
        "T8",
        "F8",
        "AF4",
        "FC6",
        "F4",
        "GYRO_X",
        "GYRO_Y",
        "RESERVED",
        "ETE1",
        "ETE2",
        "ETE3",
    ],
    "clamshell-v3.0": [
        "INTERPOLATED",
        "COUNTER",
        "BATTERY",
        "F3",
        "FC5",
        "AF3",
        "F7",
        "T7",
        "P7",
        "O1",
        "SQ_WAVE",
        "UNUSED",
        "O2",
        "P8",
        "T8",
        "F8",
        "AF4",
        "FC6",
        "F4",
        "GYRO_X",
        "GYRO_Y",
        "RESERVED",
        "ETE1",
        "ETE2",
        "ETE3",
    ],
}

class EmotivPacket(object):
    """
    Basic semantics for input bytes.
    """

    def __init__(self, data, sensors):
        """
        Initializes packet data. Sets the global battery value.
        Updates each sensor with current sensor value from the packet data.
        """
        global g_battery
        self.raw_data = data
        self.counter = ord(data[0])
        self.battery = g_battery
        if self.counter > 127:
            self.battery = self.counter
            g_battery = battery_values[str(self.battery)]
            self.counter = 128
        self.sync = self.counter == 0xe9
        self.gyro_x = ord(data[29]) - 106
        self.gyro_y = ord(data[30]) - 105
        sensors['X']['value'] = self.gyro_x
        sensors['Y']['value'] = self.gyro_y
        for name, bits in sensor_bits.items():
            #Get Level for sensors subtract 8192 to get signed value
            value = get_level(self.raw_data, bits) - 8192
            setattr(self, name, (value,))
            sensors[name]['value'] = value
        self.old_model = False
        self.handle_quality(sensors)
        self.sensors = sensors

    def handle_quality(self, sensors):
        """
        Sets the quality value for the sensor from the quality bits in the packet data.
        Optionally will return the value.
        """
        if self.old_model:
            current_contact_quality = get_level(self.raw_data, quality_bits) / 540
        else:
            current_contact_quality = get_level(self.raw_data, quality_bits) / 1024
        sensor = ord(self.raw_data[0])
        if sensor == 0 or sensor == 64:
            sensors['F3']['quality'] = current_contact_quality
        elif sensor == 1 or sensor == 65:
            sensors['FC5']['quality'] = current_contact_quality
        elif sensor == 2 or sensor == 66:
            sensors['AF3']['quality'] = current_contact_quality
        elif sensor == 3 or sensor == 67:
            sensors['F7']['quality'] = current_contact_quality
        elif sensor == 4 or sensor == 68:
            sensors['T7']['quality'] = current_contact_quality
        elif sensor == 5 or sensor == 69:
            sensors['P7']['quality'] = current_contact_quality
        elif sensor == 6 or sensor == 70:
            sensors['O1']['quality'] = current_contact_quality
        elif sensor == 7 or sensor == 71:
            sensors['O2']['quality'] = current_contact_quality
        elif sensor == 8 or sensor == 72:
            sensors['P8']['quality'] = current_contact_quality
        elif sensor == 9 or sensor == 73:
            sensors['T8']['quality'] = current_contact_quality
        elif sensor == 10 or sensor == 74:
            sensors['F8']['quality'] = current_contact_quality
        elif sensor == 11 or sensor == 75:
            sensors['AF4']['quality'] = current_contact_quality
        elif sensor == 12 or sensor == 76 or sensor == 80:
            sensors['FC6']['quality'] = current_contact_quality
        elif sensor == 13 or sensor == 77:
            sensors['F4']['quality'] = current_contact_quality
        elif sensor == 14 or sensor == 78:
            sensors['F8']['quality'] = current_contact_quality
        elif sensor == 15 or sensor == 79:
            sensors['AF4']['quality'] = current_contact_quality
        else:
            sensors['Unknown']['quality'] = current_contact_quality
            sensors['Unknown']['value'] = sensor
        return current_contact_quality

    def __repr__(self):
        """
        Returns custom string representation of the Emotiv Packet.
        """
        return 'EmotivPacket(counter=%i, battery=%i, gyro_x=%i, gyro_y=%i)' % (
            self.counter,
            self.battery,
            self.gyro_x,
            self.gyro_y)


def get_linux_setup():
    """
    Returns hidraw device path and headset serial number.
    """
    raw_inputs = []
    for filename in os.listdir("/sys/class/hidraw"):
        real_path = check_output(["realpath", "/sys/class/hidraw/" + filename]).decode()
        print(real_path)
        split_path = real_path.split('/')
        s = len(split_path)
        s -= 4
        i = 0
        path = ""
        while s > i:
            path = path + split_path[i] + "/"
            i += 1
        raw_inputs.append([path, filename])
    for input in raw_inputs:
        try:
            with open(input[0] + "/manufacturer", 'r') as f:
                manufacturer = f.readline()
                f.close()
            if "Emotiv Systems" in manufacturer:
                with open(input[0] + "/serial", 'r') as f:
                    serial = f.readline().strip()
                    f.close()
                print("Serial: " + serial + " Device: " + input[1])
                # Great we found it. But we need to use the second one...
                hidraw = input[1]
                hidraw_id = int(hidraw[-1])
                # The dev headset might use the first device, or maybe if more than one are connected they might.
                hidraw_id += 1
                hidraw = "hidraw" + hidraw_id.__str__()
                print("Serial: " + serial + " Device: " + hidraw + " (Active)")
                return [serial, hidraw, ]
        except IOError as e:
            print("Couldn't open file: %s" % e)


class Emotiv(object):

    def __init__(self, displayOutput=False, headsetId=0, research_headset=True):
        self._goOn = True
        self.packets = Queue()
        self.packetsReceived = 0
        self.packetsProcessed = 0
        self.battery = 0
        self.displayOutput = displayOutput
        self.headsetId = headsetId
        self.research_headset = research_headset
        self.sensors = {
            'F3': {'value': 0, 'quality': 0},
            'FC6': {'value': 0, 'quality': 0},
            'P7': {'value': 0, 'quality': 0},
            'T8': {'value': 0, 'quality': 0},
            'F7': {'value': 0, 'quality': 0},
            'F8': {'value': 0, 'quality': 0},
            'T7': {'value': 0, 'quality': 0},
            'P8': {'value': 0, 'quality': 0},
            'AF4': {'value': 0, 'quality': 0},
            'F4': {'value': 0, 'quality': 0},
            'AF3': {'value': 0, 'quality': 0},
            'O2': {'value': 0, 'quality': 0},
            'O1': {'value': 0, 'quality': 0},
            'FC5': {'value': 0, 'quality': 0},
            'X': {'value': 0, 'quality': 0},
            'Y': {'value': 0, 'quality': 0},
            'Unknown': {'value': 0, 'quality': 0}
        }

    def updateStdout(self):
        while self._goOn:
            if self.displayOutput:
                if windows:
                    os.system('cls')
                else:
                    os.system('clear')
                print(
                    "Packets Received: {} Packets Processed: {}".format(
                        self.packetsReceived, self.packetsProcessed))
                print('\n'.join(
                    "{} Reading: {} Strength: {}".format(
                        k[1], self.sensors[k[1]]['value'],
                        self.sensors[k[1]]['quality'])
                    for k in enumerate(self.sensors)))
                print("Battery:", g_battery)

    def setup_posix(self):
        """
        Setup for headset on the Linux platform.
        Receives packets from headset and sends them to a Queue to be processed
        by the crypto greenlet.
        """
        self._os_decryption = False
        if os.path.exists('/dev/eeg/raw'):
            self._os_decryption = True
            print("/dev/eeg/raw")
            hidraw = open("/dev/eeg/raw", 'rb')
        else:
            serial, hidraw_filename = get_linux_setup()
            self.serial_number = serial
            if os.path.exists("/dev/" + hidraw_filename):
                print("/dev/" + hidraw_filename)
                hidraw = open("/dev/" + hidraw_filename, 'rb')
            else:
                print("/dev/hidraw4")
                hidraw = open("/dev/hidraw4", 'rb')
            self.running = True
            self.device = hidraw

    @asyncio.coroutine
    def read_data_linux(self):
        self.packets_received = 0
        while self.running:
            try:
                data = self.device.read(32)
                if data:
                    if self._os_decryption:
                        self.packets.put_nowait(EmotivPacket(data))
                    else:
                        # Queue it
                        self.packets_received += 1
                        tasks.put_nowait(data)
                else:
                    # No new data from the device; yield
                    # We cannot sleep(0) here because that would go 100% CPU if both queues are empty
                    # gevent.sleep(DEVICE_POLL_INTERVAL)
                    yield from asyncio.sleep(2)
            except KeyboardInterrupt:
                self.running = False
        self.device.close()
        print(tasks.qsize())
        # print(temp_data)
        # return temp_data
        # if not self._os_decryption:
        #     gevent.kill(crypto, KeyboardInterrupt)
        # gevent.kill(console_updater, KeyboardInterrupt)

    def setupWin(self):
        devices = []
        temp_data = []
        try:
            len(hid.find_all_hid_devices())
            for device in hid.find_all_hid_devices():
                print(device)
                if device.vendor_id != 0x21A1 and device.vendor_id != 0x1234:
                    continue
                elif device.product_name == 'Emotiv RAW DATA':
                    devices.append(device)
                    device.open()
                    self.serialNum = device.serial_number
                    # print device.serial_number
                    device.set_raw_data_handler(self.handler)
            temp_data = self.setupCrypto(self.serialNum)
        except Exception as e:
            print(e)
        finally:
            for device in devices:
                device.close()
            return temp_data

    def handler(self, data):
        assert data[0] == 0
        tasks.put_nowait(''.join(map(chr, data[1:])))
        self.packetsReceived += 1
        return True

    @asyncio.coroutine
    def setupCrypto(self):
        k = ['\0'] * 16
        k[0] = self.serial_number[-1]
        k[1] = '\0'
        k[2] = self.serial_number[-2]
        k[3] = 'T'
        k[4] = self.serial_number[-3]
        k[5] = '\x10'
        k[6] = self.serial_number[-4]
        k[7] = 'B'
        k[8] = self.serial_number[-1]
        k[9] = '\0'
        k[10] = self.serial_number[-2]
        k[11] = 'H'
        k[12] = self.serial_number[-3]
        k[13] = '\0'
        k[14] = self.serial_number[-4]
        k[15] = 'P'
        key = ''.join(k)
        print(key)
        for i in k:
            print("0x%.02x " % (ord(i)))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_ECB, iv)
        vector = [0 for i in range(17)]
        i = 0
        while self._goOn:
            while not tasks.empty():
                # print(i)
                # if i == 10:
                #     result = []
                #     for bit in vector:
                #         result.append(bit/10)
                #     return result
                task = yield from tasks.get()



                data = cipher.decrypt(task[:16]) + cipher.decrypt(task[16:])
                print(data)
                self.lastPacket = EmotivPacket(data, self.sensors)
                self.packets.put_nowait(self.lastPacket)
                self.packetsProcessed += 1
                self.displayOutput = True
                # self.updateStdout()
                self.displayOutput = False
                for k in enumerate(self.sensors):
                    vector[k[0]] += self.sensors[k[1]]['value']
                i += 1
                # print vector
                print(vector)


    def dequeue(self):
        try:
            return self.packets.get()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    print("START")
    try:
        a = Emotiv()
        # a.setupWin()
        # a.setup_posix()
        print("HERE")
        loop = asyncio.get_event_loop()
        a.setup_posix()
        tasks_to_async = [

            asyncio.ensure_future(a.read_data_linux()),
            asyncio.ensure_future(a.setupCrypto()),
            ]
        finished, pending = loop.run_until_complete(
            asyncio.wait(tasks_to_async, return_when=asyncio.FIRST_COMPLETED))

    except KeyboardInterrupt:
        a.device.close()
        loop.close()
