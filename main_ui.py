# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1245, 679)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 40, 711, 561))
        self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(880, 10, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(440, 10, 261, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(730, 40, 501, 561))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1245, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionPasteGame = QtWidgets.QAction(MainWindow)
        self.actionPasteGame.setObjectName("actionPasteGame")
        self.actionConnectEngine = QtWidgets.QAction(MainWindow)
        self.actionConnectEngine.setObjectName("actionConnectEngine")
        self.actionConnectDB = QtWidgets.QAction(MainWindow)
        self.actionConnectDB.setObjectName("actionConnectDB")
        self.actionAboutProgram = QtWidgets.QAction(MainWindow)
        self.actionAboutProgram.setObjectName("actionAboutProgram")
        self.actionNewGame = QtWidgets.QAction(MainWindow)
        self.actionNewGame.setObjectName("actionNewGame")
        self.actionSetGame = QtWidgets.QAction(MainWindow)
        self.actionSetGame.setObjectName("actionSetGame")
        self.actionSaveGame = QtWidgets.QAction(MainWindow)
        self.actionSaveGame.setObjectName("actionSaveGame")
        self.actionCopyGame = QtWidgets.QAction(MainWindow)
        self.actionCopyGame.setObjectName("actionCopyGame")
        self.actionChangePlayerName = QtWidgets.QAction(MainWindow)
        self.actionChangePlayerName.setObjectName("actionChangePlayerName")
        self.menu.addAction(self.actionConnectEngine)
        self.menu_2.addAction(self.actionConnectDB)
        self.menu_3.addAction(self.actionSetGame)
        self.menu_3.addAction(self.actionSaveGame)
        self.menu_4.addAction(self.actionNewGame)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.actionCopyGame)
        self.menu_4.addAction(self.actionPasteGame)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.actionChangePlayerName)
        self.menu_5.addAction(self.actionAboutProgram)
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wakaranai"))
        self.label.setText(_translate("MainWindow", "Ходы партии и анализ"))
        self.label_3.setText(_translate("MainWindow", "Следующий ход первого игрока"))
        self.menu.setTitle(_translate("MainWindow", "Движок"))
        self.menu_2.setTitle(_translate("MainWindow", "БД"))
        self.menu_3.setTitle(_translate("MainWindow", "Файл"))
        self.menu_4.setTitle(_translate("MainWindow", "Правка"))
        self.menu_5.setTitle(_translate("MainWindow", "Помощь"))
        self.actionPasteGame.setText(_translate("MainWindow", "Вставить игру (.kif)"))
        self.actionConnectEngine.setText(_translate("MainWindow", "Подключение"))
        self.actionConnectDB.setText(_translate("MainWindow", "Подключение"))
        self.actionAboutProgram.setText(_translate("MainWindow", "О программе"))
        self.actionNewGame.setText(_translate("MainWindow", "Начать новую игру"))
        self.actionSetGame.setText(_translate("MainWindow", "Загрузить игру"))
        self.actionSaveGame.setText(_translate("MainWindow", "Сохранить игру"))
        self.actionCopyGame.setText(_translate("MainWindow", "Копировать игру"))
        self.actionChangePlayerName.setText(_translate("MainWindow", "Изменить имя игрока"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
