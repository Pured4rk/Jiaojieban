import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                            QVBoxLayout, QMenuBar, QAction, QTabWidget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('交接班管理系统')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建菜单栏
        menubar = self.menuBar()
        
        # 添加界面切换菜单
        switch_menu = menubar.addMenu('切换界面')
        
        # 创建两个界面容器
        self.main_widget = QTabWidget()
        self.interface1 = QWidget()
        self.interface2 = QWidget()
        
        # 初始化界面
        self.initInterface1()
        self.initInterface2()
        
        # 添加界面到主窗口
        self.main_widget.addTab(self.interface1, "交接班记录")
        self.main_widget.addTab(self.interface2, "统计报表")
        
        self.setCentralWidget(self.main_widget)
        self.show()
        
    def initInterface1(self):
        # 初始化交接班记录界面
        layout = QVBoxLayout()
        self.interface1.setLayout(layout)
        
    def initInterface2(self):
        # 初始化统计报表界面
        layout = QVBoxLayout()
        self.interface2.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


# test for git

# test for git 2
