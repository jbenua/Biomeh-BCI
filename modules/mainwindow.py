import numpy as np
import pyqtgraph as pg
import sys
import asyncio
import datetime
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from .login import LoginDialog
from .training import TrainingDialog
from .emotiv import Emotiv
from .tests.magic_emotiv import MagicEmotiv

MAINWINDOW_UI = './ui/main_window.ui'


QUALITY = {
    0: 'grey',
    1: 'red',
    2: 'orange',
    3: 'yellow',
    4: 'green',
}

SENSORS = {
    'f3': {
        'color': (0, 0, 255),
        'item': 'check_f3',
    },
    'fc6': {
        'color': (0, 255, 255),
        'item': 'check_fc6',
    },
    'p7': {
        'color': (0, 0, 128),
        'item': 'check_p7',
    },
    't8': {
        'color': (64, 0, 0),
        'item': 'check_t8',
    },
    'f7': {
        'color': (128, 128, 0),
        'item': 'check_f7',
    },
    'f8': {
        'color': (255, 255, 0),
        'item': 'check_f8',
    },
    't7': {
        'color': (0, 128, 0),
        'item': 'check_t7',
    },
    'p8': {
        'color': (255, 0, 0),
        'item': 'check_p8',
    },
    'af4': {
        'color': (128, 0, 128),
        'item': 'check_af4',
    },
    'f4': {
        'color': (0, 64, 0),
        'item': 'check_f4',
    },
    'af3': {
        'color': (128, 0, 0),
        'item': 'check_af3',
    },
    'o2': {
        'color': (0, 0, 64),
        'item': 'check_o2',
    },
    'o1': {
        'color': (255, 0, 255),
        'item': 'check_o1',
    },
    'fc5': {
        'color': (64, 64, 0),
        'item': 'check_fc5',
    },
    'x': {
        'color': (0, 128, 128),
        'item': 'check_x',
    },
    'y': {
        'color': (64, 0, 64),
        'item': 'check_y',
    },
    'unknown': {
        'color': (0, 255, 0),
        'item': 'check_un'
    }
}


class MainWindow(QMainWindow):
    should_close = pyqtSignal()
    goon = pyqtSignal()

    def __init__(self, current_user, loop, filter_hz=0.5):
        self.sensors = list(SENSORS.keys())
        self.curves = {}
        self.data = {name: np.empty(100) for name in self.sensors}
        self.login_dialog = LoginDialog(current_user)
        self.loop = loop
        self.filter_hz = filter_hz
        self.update_interval = 1 / filter_hz
        QMainWindow.__init__(self)

        self.user = current_user
        uic.loadUi(MAINWINDOW_UI, self)

        self.train_button.clicked.connect(self.train)
        if self.filter_hz != 0.5:
            self.set_filter_vals()
        self.filter_apply_button.clicked.connect(self.change_filter)
        self.filter_slider.sliderPressed.connect(self.set_echo_filter)
        self.filter_slider.sliderReleased.connect(self.unset_echo_filter)
        self.filter_value_edit.textEdited.connect(self.update_slider_val)
        self.change_sensors_button.clicked.connect(self.change_sensor_list)
        self.login_dialog.logged.connect(self._draw_main_window)
        self.login_dialog.close_only.connect(self.interrupt)
        self.loop.run_until_complete(self._log_in())
        self.predict = False

    def interrupt(self):
        """user didn't log in"""
        self.should_close.emit()

    def closeEvent(self, event):
        # save logs
        if len(sys.argv) > 2:
            if sys.argv[2] == 'no_logs':
                event.accept()
                return
            else:
                type_ = "_" + sys.argv[2]
        else:
            type_ = ''
        path = str(Path('.').resolve())
        filename = "{path}/logs/{date}_{user}{type_}.py".format(
            path=path, date=str(datetime.datetime.now()),
            user=self.user.username, type_=type_)
        with open(filename, 'a') as file:
            file.write('data = {')
            for sensor in self.data:
                file.write("'{}': [{}],\n".format(sensor, ', '.join([
                    '%.2f' % float(val) for val in self.data[sensor]])))
            file.write('}')
        event.accept()

    def set_classify(self, val):
        self.classify.setChecked(val)
        self.predict = val

    def check_classify(self):
        self.predict = self.classify.isChecked()
        return self.predict

    def train(self):
        state = self.check_classify()
        self.set_classify(False)
        training_dialog = TrainingDialog(self)
        training_dialog.show()
        training_dialog.exec_()
        if self.to_save:
            raws = self.user.put_raws({
                sensor: self.data[sensor][
                    self.to_save['begin']:self.to_save['end']]
                for sensor in self.data})
            self.user.add_tag(self.to_save['title'], raws)
            self.user.update_prev_data()
            print('Tag %s saved' % self.to_save['title'])
        self.set_classify(state)

    def set_tags(self, tags):
        self.label.setText(','.join(tags))

    async def additional_work(self):
        while self.device.running:
            if self.predict:
                ptr = self.ptr
                tags = self.user.detect([
                    self.data[sensor][ptr] for sensor in [
                        'f3', 'fc6', 'p7', 't8', 'f7', 'f8', 't7', 'p8',
                        'af4', 'f4', 'af3', 'o2', 'o1', 'fc5', 'x',
                        'y', 'unknown']])
                self.set_tags(tags)
            await asyncio.sleep(self.update_interval)

    async def setup_device(self):
        """Connect device to ui"""
        self.ptr = 0
        if len(sys.argv) > 1:
            device = MagicEmotiv(filter_hz=self.filter_hz)
        else:
            device = Emotiv(
                display_output=True, filter_hz=self.filter_hz)
        await device.setup()
        device.running = True
        self.set_battery(device.battery)
        if device:
            self.status.setText("OK")
            self.status.setStyleSheet("color: green")
        else:
            self.status.setText("NO DEVICE")
            self.status.setStyleSheet("color: red")

        self.device = device

    def change_filter(self):
        """Change a filter for Emotiv"""
        print("setting new filter...")
        new_val = float(self.filter_value_edit.text())
        self.update_interval = 1 / new_val
        self.device.set_filter(new_val)

    def set_battery(self, level):
        self.battery_level.setText(str(level))
        if 50 <= level <= 100:
            self.battery_level.setStyleSheet('color: green')
        elif level >= 30:
            self.battery_level.setStyleSheet('color: orange')
        else:
            self.battery_level.setStyleSheet('color: red')

    def set_connection_levels(self, packet):
        for sensor in packet.sensors:
            has_value = packet.sensors[sensor].get('quality', None)
            if has_value:

                sensor_circle = getattr(self, sensor)
                ss = '''
                border: 1px solid black;
                border-radius: 15px;
                background: {};'''.format(QUALITY[int(has_value / 3)])
                sensor_circle.setStyleSheet(ss)

    def set_filter_vals(self):
        val = float(self.filter_hz)
        self.filter_slider.setValue(val)
        self.filter_value_edit.setText(str(val))

    def unset_echo_filter(self):
        """Display real-time value change in input"""
        self.filter_slider.valueChanged.disconnect(self.update_slider_inp)

    def set_echo_filter(self):
        """Stop displaying"""
        self.filter_slider.valueChanged.connect(self.update_slider_inp)

    def update_slider_val(self):
        """Set slider to position, defined in input"""
        self.filter_slider.setValue(float(self.filter_value_edit.text()) * 2)

    def update_slider_inp(self):
        """Set input value to the one correcponding to slider"""
        self.filter_value_edit.setText(str(self.filter_slider.value() / 2))

    async def _log_in(self):
        self.login_dialog.show()
        self.login_dialog.exec_()

    def change_sensor_list(self):
        for s in SENSORS:
            if not getattr(self, SENSORS[s]['item']).isChecked():
                try:
                    self.sensors.pop(self.sensors.index(s))
                    self.curves.pop(s)
                except KeyError:
                    pass
            else:
                if s not in self.sensors:
                    self.sensors.append(s)
                if s not in self.curves:
                    self.curves[s] = self.raw_data.plot(
                        self.data[s], pen=SENSORS[s]['color'],
                        scale=100)

    def set_legend_style(self):
        legendLabelStyle = {
            'color': '#FFF', 'size': '6pt', 'bold': True, 'italic': False}
        for item in self.legend.items:
            for single_item in item:
                if isinstance(
                        single_item, pg.graphicsItems.LabelItem.LabelItem):
                    single_item.setText(single_item.text, **legendLabelStyle)

    def _draw_main_window(self):
        self.goon.emit()
        self.show()
        self.legend = self.raw_data.addLegend([50, 15], (520, 2))
        for sensor in sorted(self.sensors):
            name = sensor[:2] if sensor == 'unknown' else sensor
            self.curves[sensor] = self.raw_data.plot(
                self.data[sensor], pen=SENSORS[sensor]['color'], scale=100,
                name=name.upper())

        self.set_legend_style()
        self.raw_data.setDownsampling(mode='peak')
        self.raw_data.setClipToView(True)
        self.raw_data.autoRange()
        self.raw_data.setXRange(-1000, 1000)
        self.raw_data.setYRange(-5, 85)

    async def update_curves(self):
        ptr = -1
        while self.device.running:

            self.check_classify()
            if self.ptr != ptr:
                ptr = self.ptr
                for sensor in self.curves:
                    self.curves[sensor].setData(self.data[sensor][:ptr])
                self.raw_data.setXRange(ptr - 100, ptr + 8)
            await asyncio.sleep(self.update_interval)

    async def check_buffer(self):
        if self.ptr >= self.data[self.sensors[0]].shape[0]:
            print("need more space")
            for sensor in self.data:
                tmp = self.data[sensor]
                self.data[sensor] = np.empty(self.data[sensor].shape[0] * 2)
                self.data[sensor][:tmp.shape[0]] = tmp

    async def read_data(self):
        packet = await self.device.data_to_send.get()
        for key in packet.sensors:
            self.data[key.lower()][self.ptr] = packet.sensors[key]['value']
        self.ptr += 1
        self.set_range(packet)
        self.set_connection_levels(packet)
        self.set_battery(packet.battery)
        await asyncio.sleep(self.update_interval)
        await self.check_buffer()

        while self.device.running:
            packet = await self.device.data_to_send.get()
            for key in packet.sensors:
                self.data[key.lower()][self.ptr] = packet.sensors[key]['value']
            self.ptr += 1
            self.set_connection_levels(packet)
            self.set_battery(packet.battery)
            await asyncio.sleep(self.update_interval)
            await self.check_buffer()

    def set_range(self, packet):
        min_ = 0
        max_ = 100
        for key in packet.sensors:
            if packet.sensors[key]['value'] < min_:
                min_ = packet.sensors[key]['value']
            if packet.sensors[key]['value'] > max_:
                max_ = packet.sensors[key]['value']
        space = abs(min_) + abs(max_) / 20
        self.raw_data.setYRange(min_ - space, max_ + space)
