from school_data import SchoolData
from meal import Meal
from PyQt5.QtWidgets import QApplication
import sys
from main_window import MainWindow


school_data = SchoolData()
meal = Meal()

# school_data.crawl_db()

# print(meal.get_month(list(school_data.get_db(schl_nm=('천안쌍용고등학교', '=')))[0], 2020, 5))

app = QApplication(sys.argv)
main_window = MainWindow(school_data, meal)
main_window.show()
sys.exit(app.exec_())
