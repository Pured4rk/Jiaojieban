import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QCalendarWidget, QMessageBox
from PyQt5.QtCore import QTimer, Qt, QDate
from PyQt5.QtGui import QFont

class ShiftHandoverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('交接班系统')
        self.setGeometry(100, 100, 800, 600)

        # 主布局
        main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 标题标签
        title_label = QLabel('交接班记录', self)
        title_label.setFont(QFont("Arial", 20))
        main_layout.addWidget(title_label)

        # 值班席位输入框
        self.position_input = QLineEdit(self)
        main_layout.addWidget(self.position_input)

        # 交班记录表格
        self.shift_table = QTableWidget(self)
        self.shift_table.setColumnCount(3)
        self.shift_table.setHorizontalHeaderLabels(['席位', '上班时间', '下班时间'])
        main_layout.addWidget(self.shift_table)

        # 日历控件
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.on_date_selected)
        main_layout.addWidget(self.calendar)

        # 提醒按钮
        reminder_button = QPushButton('添加提醒', self)
        reminder_button.clicked.connect(self.add_reminder)
        main_layout.addWidget(reminder_button)

        # 日程提醒显示区域
        self.reminders_label = QLabel('', self)
        main_layout.addWidget(self.reminders_label)

        # 初始化定时器用于检查提醒
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(60000)  # 每分钟检查一次

        self.reminders = []

    def add_reminder(self):
        selected_date = self.calendar.selectedDate().toString(Qt.ISODate)
        message = f'日程提醒: {selected_date}'
        self.reminders.append(message)
        self.update_reminders_label()

    def update_reminders_label(self):
        self.reminders_label.setText('\n'.join(self.reminders))

    def check_reminders(self):
        current_date = QDate.currentDate().toString(Qt.ISODate)
        for reminder in self.reminders:
            if current_date in reminder:
                QMessageBox.information(self, '提醒', reminder)

    def on_date_selected(self, date):
        print(f"Selected date: {date.toString(Qt.ISODate)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShiftHandoverApp()
    ex.show()
    sys.exit(app.exec_())