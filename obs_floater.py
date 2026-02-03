# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from obswebsocket import obsws, requests

# --- CONFIGURATION ---
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASS = "your_secret_password" 

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

class GameBarOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.ws = None
        self.initUI()
        self.connect_obs()
        
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.update_status)
        self.check_timer.start(1000)

    def connect_obs(self):
        try:
            self.ws = obsws(OBS_HOST, OBS_PORT, OBS_PASS)
            self.ws.connect()
        except:
            self.ws = None

    def format_time(self, time_val):
        if isinstance(time_val, str):
            return time_val[:8]
        try:
            seconds = int(time_val)
            if seconds > 10000: seconds //= 1000
            h = seconds // 3600
            m = (seconds % 3600) // 60
            s = seconds % 60
            return f"{h:02d}:{m:02d}:{s:02d}"
        except:
            return "00:00:00"

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # BAR SIZE    
        self.setFixedSize(340, 80) 
        
        # MAIN CONTAINER
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 340, 48)
        self.container.setStyleSheet("""
            background-color: rgba(18,18,18,0.6); 
            border-radius: 24px; 
            border: 1px solid #333;
        """)

        # Shared Style for clean labels (No borders, no outline)
        self.label_style = "border: none; outline: none; background: transparent; margin: 0; padding: 0;"

        # Load icons
        self.record_off_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "icons", "record-off.png"))
        self.record_on_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "icons", "record-on.png"))
        self.stream_off_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "icons", "stream-off.png"))
        self.stream_on_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "icons", "stream-on.png"))

        # RECORDING UI
        self.record_dot = QLabel(self.container)
        self.record_dot.setPixmap(self.record_off_pixmap)
        self.record_dot.setScaledContents(True)
        self.record_dot.setFixedSize(13, 13)
        self.record_dot.move(27, 17)
        self.record_dot.setStyleSheet(self.label_style)
        self.record_label = QLabel("Not Recording", self.container)
        self.record_label.setFixedWidth(160)
        self.record_label.move(48, 14)

        # SEPARATOR
        self.sep = QLabel(" ", self.container)
        self.sep.setStyleSheet(f"color: #444; font-size: 18px; {self.label_style}")
        self.sep.move(205, 14)

        # STREAMING UI
        self.stream_dot = QLabel(self.container)
        self.stream_dot.setPixmap(self.stream_off_pixmap)
        self.stream_dot.setScaledContents(True)
        self.stream_dot.setFixedSize(27, 20)
        self.stream_dot.move(180, 14)
        self.stream_dot.setStyleSheet(self.label_style)
        self.stream_label = QLabel("Not Streaming", self.container)
        self.stream_label.setFixedWidth(160)
        self.stream_label.move(214, 14)

        self.update_styles(False, False, "00:00:00", "00:00:00")

        #BAR POSITION: 
        #If you want to put in the middle use this calculation example 1080p (1920-340)/2=790, the bar will be on the center.
        #2560 Center, change to: 
        #self.move(1110, 10)
        
        #Top Left Corner works on all monitor resolution
        self.move(10, 10)
        self.show()

    def update_styles(self, rec_active, stream_active, rec_time, stream_time):
        # RECORDING STYLES
        if rec_active:
            self.record_dot.setPixmap(self.record_on_pixmap)
            self.record_label.setText(f"{rec_time}")
            self.record_label.setStyleSheet(f"color: white; font-family: 'Segoe UI'; font-weight: bold; font-size: 14px; {self.label_style}")
        else:
            self.record_dot.setPixmap(self.record_off_pixmap)
            self.record_label.setText("Not Recording")
            self.record_label.setStyleSheet(f"color: #777; font-family: 'Segoe UI'; font-weight: bold; font-size: 14px; {self.label_style}")

        # STREAMING STYLES
        if stream_active:
            self.stream_dot.setPixmap(self.stream_on_pixmap)
            self.stream_label.setText(f"{stream_time}")
            self.stream_label.setStyleSheet(f"color: white; font-family: 'Segoe UI'; font-weight: bold; font-size: 14px; {self.label_style}")
        else:
            self.stream_dot.setPixmap(self.stream_off_pixmap)
            self.stream_label.setText("Not Streaming")
            self.stream_label.setStyleSheet(f"color: #777; font-family: 'Segoe UI'; font-weight: bold; font-size: 14px; {self.label_style}")

    def update_status(self):
        if not self.ws or not self.ws.ws.connected:
            self.record_label.setText("[DISCONNECTED]")
            self.connect_obs()
            return
        try:
            r = self.ws.call(requests.GetRecordStatus())
            s = self.ws.call(requests.GetStreamStatus())
            self.update_styles(r.getOutputActive(), s.getOutputActive(), self.format_time(r.getOutputDuration()), self.format_time(s.getOutputTimecode()))
        except Exception as e:
            print(f"Update error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameBarOverlay()
    sys.exit(app.exec())