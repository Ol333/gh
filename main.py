import sys
import os
import numpy as np
import subprocess
from datetime import datetime, timedelta

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QCheckBox,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit, QRadioButton,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow, QProgressBar,
QAction, QFileDialog, QDialog, QGraphicsScene, QGraphicsItem, QTableWidgetItem,
QHeaderView, QDialogButtonBox, QFormLayout, QToolTip)
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
        self.engAddr = os.getcwd() + "\\" + engNam  # ?
        self.eng = ec.Engine(engNam)
        self.rwd = rab_with_db.DbConnection("shogi_db10000.db")
        self.analisis = sas.SomeAnalisisStuff(self.eng)
        # self.eng = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")
        self.tableWidget.setColumnCount(4)
        self.newGame()

    def aboutProgram(self):
        mb = QMessageBox()
        mb.setWindowTitle("О программе")
        mb.setText("Это программа.\nАвтор - Бобровская О.П.")
        mb.exec()

    def connect_slots(self):
        self.actionSaveGame.triggered.connect(self.saveKifuToDB)
        self.actionSetGame.triggered.connect(self.downloadKifuFromDB)
        self.actionPasteGame.triggered.connect(self.pasteGame)
        self.actionCopyGame.triggered.connect(self.copyGame)
        self.actionChangePlayerName.triggered.connect(self.changePlayerName)
        self.actionConnectEngine.triggered.connect(self.showDialog_connectEngine)
        self.actionConnectDB.triggered.connect(self.showDialog_connectDB)
        self.actionAboutProgram.triggered.connect(self.aboutProgram)
        self.comm.updMoves.connect(self.updateMoves)
        self.comm.autoGame.connect(self.engineMove)
        self.graphicsView.setScene(shogi_field.MvScene(self.comm))
        self.tableWidget.currentItemChanged.connect(self.changeMove) # list -> graph
        self.actionNewGame.triggered.connect(self.newGame)

    def newGame(self):
        self.last_cp = 0
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['Ход', 'Выигрыш', 'Рейтинг по Ферреире', 'Класс хода'])
        self.tableWidget.horizontalHeaderItem(0).setToolTip('Ход в координатах \nдоски.')
        self.tableWidget.horizontalHeaderItem(1).setToolTip('Изменение позиции. \nПоложительное число \n- выигрыш, отрицательное \n- проигрыш.')
        self.tableWidget.horizontalHeaderItem(2).setToolTip('Рейтинг игрока по Ферреире. Рассчитан\n на основании всех известных ходов игрока.')
        self.tableWidget.horizontalHeaderItem(3).setToolTip('Класс хода.')
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tableWidget.setVerticalHeaderItem(0, QTableWidgetItem('0'))        
        self.tableWidget.setRowCount(0)
        self.graphicsView.scene().drawAll([''])
            
    def saveKifuToDB(self):
        print('save')

    def downloadKifuFromDB(self):
        print('download')

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
        self.graphicsView.scene().fspm.setPlainText(self.analisis.yamashita_fp())
        self.graphicsView.scene().sspm.setPlainText(self.analisis.yamashita_sp())
        self.engineAnalisis()

    def engineMove(self):
        start_pos = self.graphicsView.scene().transl.getBoard()
        bst_mov = self.eng.cp_of_next_move(start_pos, depth=17)[0]
        self.updateMoves(bst_mov)
        self.tableWidget.setCurrentCell(self.tableWidget.rowCount()-1, 0)
        
    def engineAnalisis(self):
        mov_cp, mov_cp_diff = self.analisis.moveDiffrence(self.graphicsView.scene().transl.getBoard(), self.last_cp, self.tableWidget.rowCount() - 1)
        self.tableWidget.setItem(self.tableWidget.currentRow(), 1, QTableWidgetItem(str(mov_cp_diff)))
        
        pl_str = []
        if self.tableWidget.rowCount()%2 == 0:
            for i in range(1, self.tableWidget.rowCount(), 2):
                pl_str.append(int(self.tableWidget.item(i,1).text()))
        else:
            for i in range(2, self.tableWidget.rowCount(), 2):
                pl_str.append(int(self.tableWidget.item(i,1).text()))
        ferreira = self.analisis.ferreira(pl_str)
        self.tableWidget.setItem(self.tableWidget.currentRow(), 2, QTableWidgetItem(str(ferreira)))

        if self.tableWidget.rowCount()%2 == 0:
            bad_moves_count = 0
            for i in range(1, self.tableWidget.rowCount(), 2):
                if int(self.tableWidget.item(i,1).text()) < 0:
                    bad_moves_count += 1
            self.graphicsView.scene().fspm.setPlainText(str(self.analisis.yamashita(0, mov_cp_diff)))
        else:
            bad_moves_count = 0
            for i in range(2, self.tableWidget.rowCount(), 2):
                if int(self.tableWidget.item(i,1).text()) < 0:
                    bad_moves_count += 1
            self.graphicsView.scene().sspm.setPlainText(str(self.analisis.yamashita(1, mov_cp_diff)))

        self.tableWidget.setItem(self.tableWidget.currentRow(), 3, QTableWidgetItem(str(self.analisis.moveClass(mov_cp, mov_cp_diff, self.graphicsView.scene().transl.getBoard()))))
        
        self.last_cp = mov_cp

    def showDialog_connectEngine(self):
        path = QFileDialog.getOpenFileName(self.form,
            'Выберите файл движка (нажмите Enter)', self.engAddr, "Executable (*.exe)")
        if path:
            print(path[0].split('/')[-1])

    def showDialog_connectDB(self):
        mb = QMessageBox()
        mb.setWindowTitle("Подключение БД")
        mb.setText("Подключен файл БД  'shogi_db10000.db'.")
        mb.exec()

    def pasteGame(self):
        mb = QMessageBox()
        mb.setWindowTitle("Вставить игру")
        mb.setText("Можно вставить в формате KIF или последовательность ходов...")
        mb.exec()

    def copyGame(self): # копируются только ходы, экспорта в KIF не предусмотрено
        res = []
        for i in range(self.tableWidget.rowCount()):
            res.append(self.tableWidget.item(i,0).text())
        print('\n'.join(res[1:]))

    def changePlayerName(self):
        dialog = InputDialog()
        if dialog.exec():
            print(dialog.getInputs())

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        layout = QFormLayout(self)
        layout.addRow("Первый игрок", QLineEdit(self))
        layout.addRow("Второй игрок", QLineEdit(self))
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())

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