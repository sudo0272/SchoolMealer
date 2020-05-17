from PyQt5 import QtWidgets, QtGui


class MainWindow(QtWidgets.QWidget):
    def __init__(self, school_data, meal):
        super().__init__()

        self.container = QtWidgets.QVBoxLayout()

        self.refresh_db_container = QtWidgets.QHBoxLayout()
        self.refresh_db = QtWidgets.QPushButton('DB 업데이트')
        self.refresh_db_container.addStretch()
        self.refresh_db_container.addWidget(self.refresh_db)
        self.container.addLayout(self.refresh_db_container)

        self.search_container = QtWidgets.QHBoxLayout()

        self.search_container.addStretch()

        self.school_container = QtWidgets.QHBoxLayout()
        self.school = QtWidgets.QLineEdit()
        self.school_container.addWidget(self.school)
        self.search_container.addLayout(self.school_container)

        self.year_container = QtWidgets.QHBoxLayout()
        self.year = QtWidgets.QLineEdit()
        self.year_label = QtWidgets.QLabel()
        self.year_label.setText('년')
        self.year_label.setFont(QtGui.QFont('', 13))
        self.year_container.addStretch()
        self.year_container.addWidget(self.year)
        self.year_container.addWidget(self.year_label)
        self.search_container.addLayout(self.year_container)

        self.month_container = QtWidgets.QHBoxLayout()
        self.month = QtWidgets.QLineEdit()
        self.month_label = QtWidgets.QLabel()
        self.month_label.setText('월')
        self.month_label.setFont(QtGui.QFont('', 13))
        self.month_container.addStretch()
        self.month_container.addWidget(self.month)
        self.month_container.addWidget(self.month_label)
        self.search_container.addLayout(self.month_container)

        self.search = QtWidgets.QPushButton('검색')
        self.search.setFont(QtGui.QFont('', 13))
        self.search_container.addWidget(self.search)
        
        self.search_container.addStretch()

        self.container.addLayout(self.search_container)
        
        self.date_navigator_container = QtWidgets.QHBoxLayout()
        self.date_navigator_container.addStretch()
        
        self.previous_month_arrow = QtWidgets.QPushButton()
        self.previous_month_arrow.setText('<<')
        self.previous_month_arrow.setFont(QtGui.QFont('', 13))
        self.date_navigator_container.addWidget(self.previous_month_arrow)

        self.current_date = QtWidgets.QLabel()
        self.current_date.setText(' 년 월')
        self.current_date.setFont(QtGui.QFont('', 20))
        self.date_navigator_container.addWidget(self.current_date)

        self.next_month_arrow = QtWidgets.QPushButton()
        self.next_month_arrow.setText('>>')
        self.next_month_arrow.setFont(QtGui.QFont('', 13))
        self.date_navigator_container.addWidget(self.next_month_arrow)

        self.date_navigator_container.addStretch()

        self.container.addLayout(self.date_navigator_container)

        self.calendar_container = QtWidgets.QHBoxLayout()

        self.calendar = QtWidgets.QTableWidget()
        self.calendar.setColumnCount(7)
        self.calendar.setRowCount(5)
        self.calendar.setHorizontalHeaderLabels(['일요일', '월요일', '화요일', '수요일', '목요일', '금요일','토요일'])
        self.calendar.verticalHeader().setVisible(False)

        self.calendar_container.addWidget(self.calendar)

        self.container.addLayout(self.calendar_container)

        self.setLayout(self.container)
        self.setWindowTitle('급식')
        self.setGeometry(50, 50, 800, 600)
