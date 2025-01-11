import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QCalendarWidget, QMessageBox
from PyQt5.QtCore import QTimer, Qt, QDate
from PyQt5.QtGui import QFont

class ShiftHandoverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.init_ui()

    def init_db(self):
        self.conn = sqlite3.connect('shift_handover.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shifts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            position TEXT NOT NULL,
                            start_time TEXT NOT NULL,
                            end_time TEXT NOT NULL)''')
        self.conn.commit()

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
        self.position_input.setPlaceholderText('输入值班席位')
        main_layout.addWidget(self.position_input)

        # 交班记录表格
        self.shift_table = QTableWidget(self)
        self.shift_table.setColumnCount(3)
        self.shift_table.setHorizontalHeaderLabels(['席位', '上班时间', '下班时间'])
        self.shift_table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.shift_table)

        # 操作按钮
        button_layout = QVBoxLayout()
        
        add_button = QPushButton('添加记录', self)
        add_button.clicked.connect(self.add_shift_record)
        button_layout.addWidget(add_button)

        delete_button = QPushButton('删除记录', self)
        delete_button.clicked.connect(self.delete_shift_record)
        button_layout.addWidget(delete_button)

        print_button = QPushButton('打印记录', self)
        print_button.clicked.connect(self.print_records)
        button_layout.addWidget(print_button)

        main_layout.addLayout(button_layout)

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
        self.load_shifts()

    def load_shifts(self):
        self.shift_table.setRowCount(0)
        self.cursor.execute("SELECT position, start_time, end_time FROM shifts")
        rows = self.cursor.fetchall()
        for row in rows:
            row_position = self.shift_table.rowCount()
            self.shift_table.insertRow(row_position)
            for col, value in enumerate(row):
                self.shift_table.setItem(row_position, col, QTableWidgetItem(str(value)))

    def add_shift_record(self):
        position = self.position_input.text()
        if not position:
            QMessageBox.warning(self, '警告', '请输入值班席位')
            return

        current_time = QDate.currentDate().toString(Qt.ISODate)
        self.cursor.execute("INSERT INTO shifts (position, start_time, end_time) VALUES (?, ?, ?)",
                           (position, current_time, ''))
        self.conn.commit()
        self.load_shifts()

    def delete_shift_record(self):
        selected_row = self.shift_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, '警告', '请选择要删除的记录')
            return

        position = self.shift_table.item(selected_row, 0).text()
        self.cursor.execute("DELETE FROM shifts WHERE position=?", (position,))
        self.conn.commit()
        self.load_shifts()

    def print_records(self):
        # TODO: 实现打印功能
        QMessageBox.information(self, '提示', '打印功能待实现')

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

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShiftHandoverApp()
    ex.show()
    sys.exit(app.exec_())
