from __future__ import print_function
from desktopmagic.screengrab_win32 \
import(getDisplayRects,saveScreenToBmp,getScreenAsImage,getRectAsImage,getDisplaysAsImages)
import sys
import threading
import time
import schedule
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from datetime import datetime

form_class = uic.loadUiType("DA ALA_GUI.ui")[0]

class WindowClass(QMainWindow, form_class) :
    capture_screen = 0
    meeting_start_hour = 00
    meeting_start_minute = 00
    meeting_end_hour = 00
    meeting_end_minute = 00
    capture_cycle = 5

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

    #모니터 콤보박스 아이템 추가
        self.monitor_selector.addItem("모니터 1")
        self.monitor_selector.addItem("모니터 2")
    # 모니터 콤보박스 아이템 변경시
        self.monitor_selector.activated[str].connect(self.ComboBoxOnActivated)

    # 시간 설정 관련. TimeEdit의 값이 현재 날짜/시간으로 설정되게 하기
        current_time = QTime.currentTime()
        self.meeting_start_time.setTime(current_time)
        self.meeting_end_time.setTime(current_time)
    # 시간을 사용자가 변경시
        self.meeting_start_time.timeChanged.connect(self.Start_QTimeEditOnActivated)
        self.meeting_end_time.timeChanged.connect(self.End_QTimeEditOnActivated)

    # 회의시작, 종료 버튼
        self.start_meeting.clicked.connect(self.Start_buttonOnActivated)
        self.end_meeting.clicked.connect(self.End_buttonOnActivated)

    def ComboBoxOnActivated(self, text):
        if text == "모니터 1":
            capture_screen = 0

        elif text == "모니터 2":
            capture_screen = 1

    def Start_QTimeEditOnActivated(self, text):
        hour_var = text.toString()
        self.meeting_start_hour = int(hour_var[0:2])
        self.meeting_start_minute = int(hour_var[3:5])

    def End_QTimeEditOnActivated(self, text):
        hour_var = text.toString()
        self.meeting_end_hour = int(hour_var[0:2])
        self.meeting_end_minute = int(hour_var[3:5])

    def Start_buttonOnActivated(self):
        if (self.meeting_start_hour, self.meeting_end_hour) < (self.meeting_end_hour, self.meeting_end_hour):
            screens = (getDisplayRects())
            rect = getRectAsImage(screens[self.capture_screen])
            # 요기 부분은 피드백을 위해 사진을 보여주는 부분이에여 나중에 서버로 전송하면 돼요!!
            # rect.save()
            rect.show()
            print("returned from function capture")


    def End_buttonOnActivated(self):
        # 출석부 전송
        self.close()

    def closeEvent(self, event):
        self.deleteLater()


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

# GUI 종료

