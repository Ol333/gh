import sys
import os
import subprocess
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import webbrowser

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QCheckBox,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit, QRadioButton,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow, QProgressBar,
QAction, QFileDialog, QDialog, QGraphicsScene, QGraphicsItem)
from PyQt5.QtCore import (QRect, QCoreApplication, pyqtSignal, QObject, Qt,
QTranslator, QLocale)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)

from main_ui import Ui_MainWindow
import rab_with_db
import shogi_field

class Example(Ui_MainWindow, QObject, object):
    def __init__(self, form1, com, app):
        super().__init__()
        self.form = form1
        self.engAddr = os.getcwd()+'\YaneuraOu_NNUE-tournament-clang++-avx2.exe'
        self.app = app
        self.comm = com
        self.setupUi(form1)
        self.window_main = form1
        self.connect_slots()
        self.rwd = rab_with_db.DbConnection("shogi_db10000.db")

    def aboutProgram(self):
        mb = QMessageBox()
        mb.setWindowTitle("О программе")
        mb.setText("Это программа.\nАвтор - Бобровская О.П.")
        mb.exec()

    # def open_diagram(self):
    #     new = 2
    #     webbrowser.open(self.url_report,new=new)

    def connect_slots(self):
        self.pushButton.clicked.connect(self.saveKifuToDB)        
        self.actionPasteGame.triggered.connect(self.pasteGame)
        self.actionConnectEngine.triggered.connect(self.showDialog_connectEngine)
        self.actionAboutProgram.triggered.connect(self.aboutProgram)
        self.comm.updMoves.connect(self.updateMoves)
        self.graphicsView.setScene(shogi_field.MvScene(self.comm))
        self.listWidget.currentItemChanged.connect(self.changeMove)
            
    def saveKifuToDB(self):
        print('save')

    def updateMoves(self, s):
        self.listWidget.addItem(s)

    def changeMove(self):
        # print(self.listWidget.currentItem().text())
        startpos = []
        for row in range(self.listWidget.currentRow()):
            startpos.append(self.listWidget.item(row).text())
        self.listWidget.clear()
        self.graphicsView.scene().drawAll(startpos)

    def showDialog_connectEngine(self):
        qwe1 = QWidget()
        t = QInputDialog()
        t.setOkButtonText("OK")
        t.setCancelButtonText("Cancel")
        print(t.cancelButtonText())
        text1, ok1 = t.getText(qwe1, 'New project',
            'Enter new project name:')
        if ok1:
            path = QFileDialog.getOpenFileName(self.form,
                'Выберите файл движка (нажмите Enter)', self.engAddr, "Executable (*.exe)")
            if path:
                print(path,text1)

    def pasteGame(self):
        mb = QMessageBox()
        mb.setWindowTitle("paste game")
        mb.setText("paste")
        mb.exec()

    def del_proj(self):
        d = QMessageBox.question(self.form, "Delete project",
                                "Are you sure?",
                                QMessageBox.Yes|QMessageBox.No,
                                QMessageBox.No)
        if d == QMessageBox.Yes:
            print('yes')

class Communicate(QObject):
    updMoves = pyqtSignal(str)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    com = Communicate()

    window = QMainWindow()
    ui = Example(window, com, app)
    window.show()

    sys.exit(app.exec_())

# C:\Users\Olga\Documents\for_gh>pyuic5 -x main.ui -o main_ui.py 
# для перегенерации интерфейса