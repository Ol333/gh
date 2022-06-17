import sys
import os
from telnetlib import TM
from tracemalloc import start
from turtle import color
import numpy as np
import subprocess
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Qt5Agg')
# import matplotlib.pyplot as plt
from matplotlib.figure import SubplotParams
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QCheckBox,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit, QRadioButton,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow, QProgressBar,
QAction, QFileDialog, QDialog, QGraphicsScene, QGraphicsItem, QTableWidgetItem,
QHeaderView, QDialogButtonBox, QFormLayout, QToolTip, QDialogButtonBox)
from PyQt5.QtCore import (QRect, QCoreApplication, pyqtSignal, QObject, Qt,
QTranslator, QLocale)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap, QImage)

from main_ui import Ui_MainWindow
from db_ui import Ui_Form
import rab_with_db
import shogi_field
import engine_connection as ec
import some_analisis_stuff as sas

class Example(Ui_MainWindow, Ui_Form, QObject, object):
    def __init__(self, form1, form2, com, app):
        super().__init__()
        self.form = form1
        self.db_form = form2
        self.app = app
        self.comm = com
        self.setupUi(form1)
        self.window_main = form1
        self.moves_cp_f = []
        self.moves_cp_s = []
        self.moves_cp = []
        self.rec_cp = []
        self.connect_slots()
        engNam = [f for f in os.listdir() if 'YaneuraOu' in f][0].split('.')[0]
        self.engAddr = os.getcwd() + "\\" + engNam  # ?
        self.eng = ec.Engine(engNam)
        
        self.analisis = sas.SomeAnalisisStuff(self.eng)
        self.restartFlag = False
        # self.eng = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")
        self.tableWidget.setColumnCount(5)
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
        self.comm.gameOver.connect(self.gameOver)
        self.comm.kifDownl.connect(self.kifDownload)
        self.graphicsView.setScene(shogi_field.MvScene(self.comm))
        self.graphicsView_2.setScene(QGraphicsScene())
        self.tableWidget.currentItemChanged.connect(self.changeMove) # list -> graph
        self.actionNewGame.triggered.connect(self.newGame)
        self.actionContinueGame.triggered.connect(self.continueGame)

    def newGame(self):
        self.restartFlag = True
        self.last_cp = 0
        start_row_count = self.tableWidget.rowCount() - 1
        for i in range(start_row_count,-1,-1):
            self.tableWidget.removeRow(i)
        self.tableWidget.setHorizontalHeaderLabels(['Ход', 'Выигрыш', 'Рейтинг по Ферреире', 'Класс хода', 'Рекомендация'])
        self.tableWidget.horizontalHeaderItem(0).setToolTip('Ход в координатах \nдоски.')
        self.tableWidget.horizontalHeaderItem(1).setToolTip('Изменение позиции. \nПоложительное число \n- выигрыш, отрицательное \n- проигрыш.')
        self.tableWidget.horizontalHeaderItem(2).setToolTip('Рейтинг игрока по Ферреире. Рассчитан\n на основании всех известных ходов игрока.')
        self.tableWidget.horizontalHeaderItem(3).setToolTip('Класс хода.')
        self.tableWidget.horizontalHeaderItem(4).setToolTip('Рекомендуемый наилучший ход.')
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tableWidget.setVerticalHeaderItem(0, QTableWidgetItem('0'))        
        self.tableWidget.setRowCount(0)
        self.graphicsView.scene().drawAll([''])
        self.graphicsView_2.scene().clear()
        self.moves_cp_f = []
        self.moves_cp_s = []
        self.moves_cp = []
        self.rec_cp = []
        self.restartFlag = False

    def continueGame(self):
        startpos = []
        for row in range(1, self.tableWidget.currentRow()+1):
            startpos.append(self.tableWidget.item(row, 0).text())
        self.newGame()
        self.graphicsView.scene().drawAll(startpos)
        self.graphicsView.scene().fspm.setPlainText(self.analisis.yamashita_fp())
        self.graphicsView.scene().sspm.setPlainText(self.analisis.yamashita_sp())
            
    def saveKifuToDB(self):
        dlg = QDialog()
        buttonBox = QDialogButtonBox(dlg)
        buttonBox.setGeometry(QRect(90, 70, 156, 23))
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.save)
        buttonBox.rejected.connect(dlg.close)
        dlg.setWindowTitle("Сохранение партии")
        label = QLabel(dlg)
        label.setText(('Вы уверены, что хотите сохранить эту игру? \n'
                    + 'Первый игрок: ' + self.graphicsView.scene().fpn.toPlainText() + '\n'
                    + 'Второй игрок: '+ self.graphicsView.scene().spn.toPlainText() + '\n'
                    + str(self.tableWidget.rowCount()-1) + ' ходов.'))
        label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        label.setMargin(5)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

    def save(self):
        moves = []
        for row in range(1, self.tableWidget.currentRow()+1):
            moves.append([row,
                        # self.tableWidget.item(row, 0).text(), # упс
                        self.rec_cp[row-1],
                        self.tableWidget.item(row, 4).text(),
                        self.moves_cp[row-1]])
        self.rwd.save_game(self.graphicsView.scene().fpn.toPlainText(), 
                            self.graphicsView.scene().spn.toPlainText(),
                            moves)

    def downloadKifuFromDB(self):
        self.db_form.show()

    def updateMoves(self, s):
        self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
        self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QTableWidgetItem(s))
        self.tableWidget.setVerticalHeaderItem(self.tableWidget.rowCount()-1, QTableWidgetItem(str(self.tableWidget.rowCount()-1)))
        # self.tableWidget.setCurrentCell(self.tableWidget.rowCount()-1, 0) # вызывает ошибку  
        if self.tableWidget.rowCount()%2 == 0:
            self.label_3.setText(self.label_3.text().replace('первого', 'второго'))
        else:
            self.label_3.setText(self.label_3.text().replace('второго', 'первого'))
        self.graphicsView_2.scene().clear()
        self.graphicsView_2.scene().addPixmap(self.plotCPChange())

    def plotCPChange(self):
        rcp_mas_f = np.array(self.moves_cp_f)
        rcp_mas_s = np.array(self.moves_cp_s)
        x_f = range(1, 2*len(rcp_mas_f), 2)
        x_s = range(2, 2*len(rcp_mas_s)+1, 2)
        fig = Figure((5.4, 2.1), dpi=100)
        fig.suptitle("Оценка позиции движком", fontsize=8)        
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)        
        ax.set_xlabel("Номер хода", fontsize=6)
        ax.set_ylabel("Оценка позиции", fontsize=6)
        ax.minorticks_on()
        ax.grid(which="major",linewidth=1.2)
        ax.grid(which="minor",linestyle = ':')
        ax.bar(x_f, rcp_mas_f, color='yellow')
        ax.bar(x_s, rcp_mas_s, color='green')
        canvas.draw()
        size = canvas.size()
        width, height = size.width(), size.height()
        im = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
        return QPixmap(im)

    def changeMove(self):
        if not self.restartFlag:
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

    def gameOver(self, s):
        mb = QMessageBox()
        mb.setWindowTitle("Сообщение")
        mb.setText("Игра закончена.\nПричина:\n"+ s +"\nПобедитель - "
                    + (self.graphicsView.scene().fpn.toPlainText() if self.tableWidget.rowCount()%2 == 0 else 'второй')+' игрок.')
        mb.exec()

    def kifDownload(self, kif):
        self.graphicsView.scene().drawAll(kif)

    def engineMove(self):
        start_pos = self.graphicsView.scene().transl.getBoard()
        bst_mov = self.eng.cp_of_next_move(start_pos, depth=17)[0]
        if bst_mov == 'resign':
            self.gameOver('Игрок сдался.')
        else:
            self.updateMoves(bst_mov)
            self.tableWidget.setCurrentCell(self.tableWidget.rowCount()-1, 0)
        
    def engineAnalisis(self):
        if self.tableWidget.rowCount() > 1:
            # if self.tableWidget.item(self.tableWidget.rowCount()-2,1) == None:
            #     temp_iter = self.tableWidget.rowCount()-2
            #     while self.tableWidget.item(temp_iter,1) == None and temp_iter > 1:
            #         temp_iter -= 1
            #     for i in range(temp_iter, self.tableWidget.rowCount()-1):
            #         self.tableWidget.setCurrentCell(i,0)
            mov_cp, mov_cp_diff = self.analisis.moveDiffrence(self.graphicsView.scene().transl.getBoard(), self.last_cp, self.tableWidget.rowCount() - 1)
            if self.tableWidget.currentRow()%2==1:
                self.moves_cp_f.append(-mov_cp)
            else:
                self.moves_cp_s.append(mov_cp)
            self.moves_cp.append(mov_cp)
            self.tableWidget.setItem(self.tableWidget.currentRow(), 1, QTableWidgetItem(str(mov_cp_diff)))
            
            pl_str = []
            if self.tableWidget.currentRow()%2 == 1:
                for i in range(1, self.tableWidget.currentRow()+1, 2):
                    pl_str.append(int(self.tableWidget.item(i,1).text()))
            else:
                for i in range(2, self.tableWidget.currentRow()+1, 2):
                    pl_str.append(int(self.tableWidget.item(i,1).text()))
            ferreira = self.analisis.ferreira(pl_str)
            self.tableWidget.setItem(self.tableWidget.currentRow(), 2, QTableWidgetItem(str(ferreira)))

            if self.tableWidget.currentRow()%2 == 1:
                bad_moves_count = 0
                for i in range(1, self.tableWidget.currentRow()+1, 2):
                    if int(self.tableWidget.item(i,1).text()) < 0:
                        bad_moves_count += 1
                self.graphicsView.scene().fspm.setPlainText(str(self.analisis.yamashita(0, mov_cp_diff)))
            else:
                bad_moves_count = 0
                for i in range(2, self.tableWidget.currentRow()+1, 2):
                    if int(self.tableWidget.item(i,1).text()) < 0:
                        bad_moves_count += 1
                self.graphicsView.scene().sspm.setPlainText(str(self.analisis.yamashita(1, mov_cp_diff)))

            moveClass, rec_cp = self.analisis.moveClass(mov_cp, mov_cp_diff, self.graphicsView.scene().transl.getBoard())
            self.tableWidget.setItem(self.tableWidget.currentRow(), 3, QTableWidgetItem(str(moveClass)))
            self.rec_cp.append(rec_cp)
            self.tableWidget.setItem(self.tableWidget.currentRow(), 4, QTableWidgetItem(str(self.eng.cp_of_next_move(self.graphicsView.scene().transl.getBoard(), depth=17)[0])))
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
        mb.setText("Можно вставить игру в формате KIF или в виде последовательности ходов...")
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

class dbWindow(Ui_Form, QObject):
    def __init__(self, form, com):
        super().__init__()
        self.window = form
        self.comm = com
        self.setupUi(form)
        self.connect_slots()
        self.kif_id_list = []
        self.rwd = rab_with_db.DbConnection("shogi_db10000.db")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Первый игрок', 'Второй игрок', 'Кифу'])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
    
    def connect_slots(self):
        self.pushButton.clicked.connect(self.find)
        self.pushButton_2.clicked.connect(self.load)
        # self.comm.kifDownl.connect(self.load)
        
    def find(self):
        fpl = ''
        spl = ''
        self.kif_id_list = []
        if self.textEdit.toPlainText() != '':
            fpl = self.textEdit.toPlainText()
            for r in self.rwd.pl_and_kifu(self.rwd.player_idbylogin(fpl)):
                self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QTableWidgetItem(self.rwd.player_loginbyid(r[2])))
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 1, QTableWidgetItem(self.rwd.player_loginbyid(r[3])))
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 2, QTableWidgetItem(r[0]))
                self.kif_id_list.append(r[1])
        if self.textEdit_2.toPlainText() != '':
            spl = self.textEdit_2.toPlainText()
            for r in self.rwd.pl_and_kifu(self.rwd.player_idbylogin(spl)):
                self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QTableWidgetItem(self.rwd.player_loginbyid(r[2])))
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 1, QTableWidgetItem(self.rwd.player_loginbyid(r[3])))
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 2, QTableWidgetItem(r[0]))
                self.kif_id_list.append(r[1])

    def load(self):
        s = self.rwd.get_kifu(self.kif_id_list[self.tableWidget.currentRow()])[0]
        self.comm.kifDownl.emit(s)

class Communicate(QObject):
    updMoves = pyqtSignal(str)
    autoGame = pyqtSignal()
    gameOver = pyqtSignal(str)
    kifDownl = pyqtSignal(str)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    com = Communicate()

    window = QMainWindow()
    db_window = QWidget()
    db_wind = dbWindow(db_window, com)
    ui = Example(window, db_window, com, app)
    window.show()

    sys.exit(app.exec_())

# C:\Users\Olga\Documents\for_gh>pyuic5 -x main.ui -o main_ui.py 
# для перегенерации интерфейса