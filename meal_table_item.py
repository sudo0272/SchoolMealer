from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget


class MealTableItem(QtWidgets.QWidget):
    def __init__(self, date, lunch, dinner):
        super(MealTableItem, self).__init__()
        self.container = QtWidgets.QVBoxLayout()

        self.date_label = QtWidgets.QLabel(date)
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.container.addWidget(self.date_label)

        self.container.addStretch()

        alergies = ['난류', '우유', '메밀', '땅콩', '대두', '밀', '고등어', '게', '새우', '돼지고기', '복숭아', '토마토', '아황산염', '호두', '소고기', '생선', '해산물', '수박류', '키위', '인스턴트']
        
        self.lunch_container = QtWidgets.QVBoxLayout()
        self.lunch_menus = [QtWidgets.QVBoxLayout() for i in range(len(lunch) if lunch is not None else 0)]
        self.lunch_labels = [QtWidgets.QLabel() for i in range(len(lunch) if lunch is not None else 0)]
        self.lunch_alergies = [QtWidgets.QHBoxLayout() for i in range(len(lunch) if lunch is not None else 0)]
        self.lunch_alergies_label = [[] for i in range(len(lunch) if lunch is not None else 0)]
        
        for i in range(len(lunch) if lunch is not None else 0):
            self.lunch_labels[i].setText(lunch[i][0])  
            self.lunch_labels[i].setAlignment(QtCore.Qt.AlignCenter)

            self.lunch_menus[i].addWidget(self.lunch_labels[i])

            if lunch[i] is not None:
                self.lunch_alergies[i].addStretch()
                for j in lunch[i][1]:
                    self.lunch_alergies_label[i].append(QtWidgets.QLabel())
                    self.lunch_alergies_label[i][-1].setText(str(j))
                    self.lunch_alergies_label[i][-1].setToolTip(alergies[j - 1])
                    self.lunch_alergies[i].addWidget(self.lunch_alergies_label[i][-1])
                self.lunch_alergies[i].addStretch()

                self.lunch_menus[i].addLayout(self.lunch_alergies[i])

            self.lunch_container.addLayout(self.lunch_menus[i])

        self.container.addLayout(self.lunch_container)

        self.container.addSpacerItem(QtWidgets.QSpacerItem(20, 40))
        
        self.dinner_container = QtWidgets.QVBoxLayout()
        self.dinner_menus = [QtWidgets.QVBoxLayout() for i in range(len(dinner) if dinner is not None else 0)]
        self.dinner_labels = [QtWidgets.QLabel() for i in range(len(dinner) if dinner is not None else 0)]
        self.dinner_alergies = [QtWidgets.QHBoxLayout() for i in range(len(dinner) if dinner is not None else 0)]
        self.dinner_alergies_label = [[] for i in range(len(dinner) if dinner is not None else 0)]

        for i in range(len(dinner) if dinner is not None else 0):
            self.dinner_labels[i].setText(dinner[i][0])
            self.dinner_labels[i].setAlignment(QtCore.Qt.AlignCenter)
            self.dinner_menus[i].addWidget(self.dinner_labels[i])

            if dinner[i] is not None:
                self.dinner_alergies[i].addStretch()
                for j in dinner[i][1]:
                    self.dinner_alergies_label[i].append(QtWidgets.QLabel)
                    self.dinner_alergies_label[i][-1].setText(str(j))
                    self.dinner_alergies_label[i][-1].setToolTip(alergies[j - 1])
                    self.dinner_alergies[i].addWidget(self.dinner_alergies_label[i][-1])
                self.dinner_alergies[i].addStretch()

                self.dinner_menus[i].addLayout(self.dinner_alergies[i])

            self.dinner_container.addLayout(self.dinner_menus[i])

        self.container.addLayout(self.dinner_container)

        self.setLayout(self.container)
