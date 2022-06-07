import sys
import os
import numpy as np
import subprocess
from datetime import datetime, timedelta
import webbrowser

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QCheckBox,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit, QRadioButton,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow, QProgressBar,
QAction, QFileDialog, QDialog, QGraphicsScene, QGraphicsItem, QTableWidgetItem,
QHeaderView)
from PyQt5.QtCore import (QRect, QCoreApplication, pyqtSignal, QObject, Qt,
QTranslator, QLocale)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap)

from main_ui import Ui_MainWindow
import rab_with_db
import shogi_field
import engine_connection as ec
import some_analisis_stuff as sas

class Example(Ui_MainWindow, QObject, object):
    def __init__(self, form1, com, app):
        super().__init__()
        self.form = form1
        self.app = app
        self.comm = com
        self.setupUi(form1)
        self.window_main = form1
        self.connect_slots()
        engNam = [f for f in os.listdir() if 'YaneuraOu' in f][0].split('.')[0]
        self.engAddr = os.getcwd() + engNam  # ?
        self.eng = ec.Engine(engNam)
        self.rwd = rab_with_db.DbConnection("shogi_db10000.db")
        self.analisis = sas.SomeAnalisisStuff(self.eng)
        # self.eng = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")
        self.tableWidget.setColumnCount(2)
        self.newGame()

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
        self.comm.autoGame.connect(self.engineMove)
        self.graphicsView.setScene(shogi_field.MvScene(self.comm))
        self.tableWidget.currentItemChanged.connect(self.changeMove) # list -> graph
        self.actionNewGame.triggered.connect(self.newGame)

    def newGame(self):
        self.last_cp = 0
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['Ход', 'Выигрыш'])
        self.tableWidget.setVerticalHeaderItem(0, QTableWidgetItem('0'))        
        self.tableWidget.setRowCount(0)
        self.graphicsView.scene().drawAll([''])
            
    def saveKifuToDB(self):
        print('save')

    def updateMoves(self, s):
        self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
        self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QTableWidgetItem(s))
        self.tableWidget.setVerticalHeaderItem(self.tableWidget.rowCount()-1, QTableWidgetItem(str(self.tableWidget.rowCount()-1)))

        # self.tableWidget.setCurrentCell(self.tableWidget.rowCount()-1, 0) # вызывает ошибку
        
        if self.tableWidget.rowCount()%2 == 0:
            self.label_3.setText(self.label_3.text().replace('первого', 'второго'))
        else:
            self.label_3.setText(self.label_3.text().replace('второго', 'первого'))

    def changeMove(self):
        startpos = []
        for row in range(self.tableWidget.currentRow()+1):
            if self.tableWidget.item(row, 0) == None:
                startpos.append('')
            else:
                startpos.append(self.tableWidget.item(row, 0).text())
        self.graphicsView.scene().drawAll(startpos, silence=True)
        self.engineAnalisis()

    def engineMove(self):
        start_pos = self.graphicsView.scene().transl.getBoard()
        bst_mov = self.eng.cp_of_next_move(start_pos, depth=17)[0]
        self.updateMoves(bst_mov)
        self.tableWidget.setCurrentCell(self.tableWidget.rowCount()-1, 0)
        
    def engineAnalisis(self):
        mov_cp, mov_cp_diff = self.analisis.moveDiffrence(self.graphicsView.scene().transl.getBoard(), self.last_cp, self.tableWidget.rowCount() - 1)
        self.tableWidget.setItem(self.tableWidget.currentRow(), 1, QTableWidgetItem(str(mov_cp_diff)))
        # как определяет позиция?              
        self.last_cp = mov_cp

    def showDialog_connectEngine(self):
        qwe1 = QWidget()
        t = QInputDialog()
        t.setOkButtonText("OK")
        t.setCancelButtonText("Cancel")
        print(t.cancelButtonText())
        text1, ok1 = t.getText(qwe1, 'Движок',
            'Введите название движка:')
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
    autoGame = pyqtSignal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    com = Communicate()

    window = QMainWindow()
    ui = Example(window, com, app)
    window.show()

    sys.exit(app.exec_())

# C:\Users\Olga\Documents\for_gh>pyuic5 -x main.ui -o main_ui.py 
# для перегенерации интерфейса