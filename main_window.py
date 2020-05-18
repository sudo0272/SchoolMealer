from PyQt5 import QtWidgets, QtGui, QtCore
import datetime
from meal_table_item import MealTableItem


class MainWindow(QtWidgets.QWidget):
    def __init__(self, school_data, meal):
        super().__init__()

        self.school_data = school_data
        self.meal = meal

        self.container = QtWidgets.QVBoxLayout()

        self.refresh_db_container = QtWidgets.QHBoxLayout()
        self.refresh_db_button = QtWidgets.QPushButton('DB 업데이트')
        self.refresh_db_button.clicked.connect(self.refresh_db)
        self.refresh_db_container.addStretch()
        self.refresh_db_container.addWidget(self.refresh_db_button)
        self.container.addLayout(self.refresh_db_container)

        self.search_container = QtWidgets.QHBoxLayout()

        self.search_container.addStretch()

        self.school_container = QtWidgets.QHBoxLayout()
        self.school = QtWidgets.QLineEdit()
        school_candidates = [i[1] for i in self.school_data.get_db()]
        self.school.setCompleter(QtWidgets.QCompleter(school_candidates))
        self.school_container.addWidget(self.school)
        self.search_container.addLayout(self.school_container)

        today = datetime.datetime.now()
        self.min_year = 2019
        self.max_year = today.year + 1

        self.year_container = QtWidgets.QHBoxLayout()
        self.year = QtWidgets.QSpinBox()
        self.year.setRange(self.min_year, self.max_year)
        self.year.setValue(today.year)
        self.year_label = QtWidgets.QLabel()
        self.year_label.setText('년')
        self.year_label.setFont(QtGui.QFont('', 13))
        self.year_container.addStretch()
        self.year_container.addWidget(self.year)
        self.year_container.addWidget(self.year_label)
        self.search_container.addLayout(self.year_container)

        self.month_container = QtWidgets.QHBoxLayout()
        self.month = QtWidgets.QSpinBox()
        self.month.setRange(1, 12)
        self.month.setValue(today.month)
        self.month_label = QtWidgets.QLabel()
        self.month_label.setText('월')
        self.month_label.setFont(QtGui.QFont('', 13))
        self.month_container.addStretch()
        self.month_container.addWidget(self.month)
        self.month_container.addWidget(self.month_label)
        self.search_container.addLayout(self.month_container)

        self.search_button = QtWidgets.QPushButton('검색')
        self.search_button.setFont(QtGui.QFont('', 13))
        self.search_button.clicked.connect(self.search)
        self.search_container.addWidget(self.search_button)
        
        self.search_container.addStretch()

        self.container.addLayout(self.search_container)
        
        self.date_navigator_container = QtWidgets.QHBoxLayout()
        self.date_navigator_container.addStretch()
        
        self.previous_month_arrow = QtWidgets.QPushButton()
        self.previous_month_arrow.setText('<<')
        self.previous_month_arrow.setFont(QtGui.QFont('', 13))
        self.previous_month_arrow.clicked.connect(self.move_to_previous_month)
        self.date_navigator_container.addWidget(self.previous_month_arrow)

        self.current_date = QtWidgets.QLabel()
        self.current_date.setText(' 년 월')
        self.current_date.setFont(QtGui.QFont('', 20))
        self.date_navigator_container.addWidget(self.current_date)

        self.next_month_arrow = QtWidgets.QPushButton()
        self.next_month_arrow.setText('>>')
        self.next_month_arrow.setFont(QtGui.QFont('', 13))
        self.next_month_arrow.clicked.connect(self.move_to_next_month)
        self.date_navigator_container.addWidget(self.next_month_arrow)

        self.date_navigator_container.addStretch()

        self.container.addLayout(self.date_navigator_container)

        self.search_result_container = QtWidgets.QStackedLayout()

        self.calendar = QtWidgets.QTableWidget()
        self.calendar.setColumnCount(7)
        self.calendar.setRowCount(6)
        self.calendar.setHorizontalHeaderLabels(['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'])
        self.calendar.verticalHeader().setVisible(False)
        for i in range(7):
            self.calendar.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.search_result_container.addWidget(self.calendar)

        self.no_search_result = QtWidgets.QLabel()
        self.no_search_result.setText('검색 결과가 없습니다\n날짜가 잘못되었는지 확인해보시거나\nDB를 업데이트해주세요')
        self.no_search_result.setAlignment(QtCore.Qt.AlignCenter)
        self.no_search_result.setFont(QtGui.QFont('', 20))

        self.search_result_container.addWidget(self.no_search_result)

        self.search_result_container.setCurrentIndex(0)

        self.container.addLayout(self.search_result_container)

        self.setLayout(self.container)
        self.setWindowTitle('급식')
        self.setGeometry(50, 50, 800, 600)

    def refresh_db(self):
        self.refresh_db_button.setText('DB 업데이트 중...')
        self.refresh_db_button.setEnabled(False)
        self.refresh_db_button.repaint()

        self.school_data.crawl_db()

        self.refresh_db_button.setText('DB 업데이트')
        self.refresh_db_button.setEnabled(True)
        self.refresh_db_button.repaint()

    def search(self):
        self.search_button.setText('검색 중...')
        self.search_button.setEnabled(False)
        self.search_button.repaint()

        data = tuple(self.school_data.get_db(schl_nm=(self.school.text(), '=')))
        data = data[0] if len(data) else None
        year = int(self.year.text())
        month = int(self.month.text())

        self.current_date.setText('%d년 %d월' % (year, month))

        self.previous_month_arrow.setEnabled(False if year == self.min_year and month == 1 else True)
        self.previous_month_arrow.repaint()
        self.next_month_arrow.setEnabled(False if year == self.max_year and month == 12 else True)
        self.next_month_arrow.repaint()

        if data is None:
            self.search_result_container.setCurrentIndex(1)
        else:
            start_day, meal_data = self.meal.get_month(data[0], year, month)

            row_count, i_end = divmod(start_day + len(meal_data), 7)
            j_start = start_day

            for i in range(j_start):
                self.calendar.setCellWidget(0, i, MealTableItem('', None, None))

            for i in range(row_count):
                base_index = i * 7 - start_day

                for j in range(j_start, 7):
                    index = base_index + j
                    self.calendar.setCellWidget(i, j, MealTableItem(str(index + 1), meal_data[index]['lunch'], meal_data[index]['dinner']))

                j_start = 0

            for i in range(0, i_end):
                index = row_count * 7 - start_day + i

                self.calendar.setCellWidget(row_count, i, MealTableItem(str(index + 1), meal_data[index]['lunch'], meal_data[index]['dinner']))

            for i in range(row_count, 6):
                for j in range(i_end, 7):
                    self.calendar.setCellWidget(i, j, MealTableItem('', None, None))

                i_end = 0

            self.calendar.resizeRowsToContents()

            self.search_result_container.setCurrentIndex(0)

        self.search_button.setText('검색')
        self.search_button.setEnabled(True)
        self.search_button.repaint()

    def move_to_previous_month(self):
        month = int(self.month.text())
        year = int(self.year.text())

        if year == self.min_year:
            if month == 1:
                return
            else:
                self.month.setValue(int(month) - 1)
        else:
            if month == 1:
                self.year.setValue(int(year) - 1)
                self.month.setValue(12)
            else:
                self.month.setValue(int(month) - 1)

        self.search()

    def move_to_next_month(self):
        month = self.month.text()
        year = self.year.text()

        if year == self.max_year:
            if month == 12:
                return
            else:
                self.month.setValue(int(month) + 1)
        else:
            if month == 12:
                self.year.setValue(int(year) + 1)
                self.month.setValue(1)
            else:
                self.month.setValue(int(month) + 1)

        self.search()
