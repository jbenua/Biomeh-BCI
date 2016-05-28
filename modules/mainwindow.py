from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
import pyqtgraph as pg
import sys
import asyncio

from .login import LoginDialog
from .training import TrainingDialog
from .emotiv import Emotiv, EmotivPacket
from .tests.magic_emotiv import MagicEmotiv, MagicPacket

MAINWINDOW_UI = './ui/main_window.ui'
GO_LEFT_PIC = './img/go_left.png'
GO_RIGHT_PIC = './img/go_right.png'
UPDATE_INTERVAL = 0.25

# TODO: add curve- and timeout- and buffer size selectors


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
    def __init__(self, current_user, loop):
        self.sensors = list(SENSORS.keys())
        self.curves = {}
        self.data = {name: np.empty(100) for name in self.sensors}
        self.login_dialog = LoginDialog(current_user)
        self.loop = loop
        QMainWindow.__init__(self)

        self.user = current_user
        uic.loadUi(MAINWINDOW_UI, self)

        self.train_button.clicked.connect(self.train)
        self.filter_apply_button.clicked.connect(self.change_filter)
        self.filter_slider.sliderPressed.connect(self.set_echo_filter)
        self.filter_slider.sliderReleased.connect(self.unset_echo_filter)
        self.filter_value_edit.textEdited.connect(self.update_slider_val)
        self.change_sensors_button.clicked.connect(self.change_sensor_list)
        self.login_dialog.logged.connect(self._draw_main_window)
        self.loop.run_until_complete(self._log_in())

    def train(self):
        training_dialog = TrainingDialog()
        training_dialog.show()
        training_dialog.exec_()

    async def setup_device(self):
        """Connect device to ui"""
        self.ptr = 0
        if len(sys.argv) > 1:
            device = MagicEmotiv(self.ptr, UPDATE_INTERVAL)
        else:
            device = Emotiv(display_output=True, filter=0.5, pointer=self.ptr)

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
        ...
        # TODO: implement

    def set_battery(self, level):
        self.battery_level.setText(str(level))
        if 50 <= level <= 100:
            self.battery_level.setStyleSheet('color: green')
        elif level >= 30:
            self.battery_level.setStyleSheet('color: orange')
        else:
            self.battery_level.setStyleSheet('color: red')

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
        # QObject.connect(
        #     self.login_dialog, SIGNAL("logged()"), self._draw_main_window)
        self.login_dialog.show()
        self.login_dialog.exec_()

    def _init_pixmaps(self):
        self.left_pixmap = QPixmap(GO_LEFT_PIC).scaledToWidth(
            self.walking_man.width())
        self.right_pixmap = QPixmap(GO_RIGHT_PIC).scaledToWidth(
            self.walking_man.width())

    def set_go_left(self):
        self.walking_man.setPixmap(self.left_pixmap)

    def set_go_right(self):
        self.walking_man.setPixmap(self.right_pixmap)

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
        self.show()
        self.legend = self.raw_data.addLegend([50, 20], (480, 10))
        for sensor in sorted(self.sensors):
            name = sensor[:2] if sensor == 'unknown' else sensor
            self.curves[sensor] = self.raw_data.plot(
                self.data[sensor], pen=SENSORS[sensor]['color'], scale=100,
                name=name.upper())

        self.set_legend_style()

        self._init_pixmaps()
        self.set_go_left()
        self.raw_data.setDownsampling(mode='peak')
        self.raw_data.setClipToView(True)
        self.raw_data.autoRange()
        self.raw_data.setXRange(-1000, 1000)
        self.raw_data.setYRange(-5, 85)

    async def update_curves(self):

        ptr = -1
        while self.device.running:
            if self.ptr != ptr:
                ptr = self.ptr
                print(ptr)
                for sensor in self.curves:
                    self.curves[sensor].setData(self.data[sensor][:ptr])
                self.raw_data.setXRange(ptr - 100, ptr + 8)
                await asyncio.sleep(UPDATE_INTERVAL)

    async def check_buffer(self):
        print("check_buffer")
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
        self.set_range(packet)
        self.ptr += 1
        while self.device.running:
            packet = await self.device.data_to_send.get()
            for key in packet.sensors:
                self.data[key.lower()][self.ptr] = packet.sensors[key]['value']
            self.ptr += 1
            await self.check_buffer()

    def set_range(self, packet):
        min_ = 0
        max_ = 0
        for key in packet.sensors:
            if packet.sensors[key]['value'] < min_:
                min_ = packet.sensors[key]['value']
            if packet.sensors[key]['value'] > max_:
                max_ = packet.sensors[key]['value']
        space = abs(min_) + abs(max_)/10
        self.raw_data.setYRange(min_ - space, max_ + space)

