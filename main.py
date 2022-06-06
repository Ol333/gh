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

class Example(Ui_MainWindow, QObject, object):
    def __init__(self, form1, com, app):
        super().__init__()
        self.form = form1
        self.engAddr = os.getcwd()+'\YaneuraOu_NNUE-tournament-clang++-avx2.exe'  # ?
        self.app = app
        self.comm = com
        self.setupUi(form1)
        self.window_main = form1
        self.connect_slots()
        self.rwd = rab_with_db.DbConnection("shogi_db10000.db")
        self.eng = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")
        self.last_cp = 0
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Ход', 'Выигрыш'])
        self.tableWidget.setVerticalHeaderItem(0, QTableWidgetItem('0'))

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
        # self.listWidget.currentItemChanged.connect(self.changeMove) # list -> graph
        self.tableWidget.currentItemChanged.connect(self.changeMove) # list -> graph
        self.actionNewGame.triggered.connect(self.newGame)

    def newGame(self):
        # self.listWidget.clear()
        self.tableWidget.clear()
        self.graphicsView.scene().drawAll([''])
            
    def saveKifuToDB(self):
        print('save')

    def updateMoves(self, s):
        # self.listWidget.addItem(s)
        self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
        self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QTableWidgetItem(s))
        self.tableWidget.setVerticalHeaderItem(self.tableWidget.rowCount()-1, QTableWidgetItem(str(self.tableWidget.rowCount()-1)))

        self.tableWidget.setCurrentCell(self.tableWidget.rowCount()-1, 0) # вызывает следущую ошибку
        ###
        # Traceback (most recent call last):
        #   File "gh\shogi_field.py", line 70, in mousePressEvent
        #     self.selectFigure(item, mouseEvent.scenePos().x(), mouseEvent.scenePos().y())
        #   File "gh\shogi_field.py", line 165, in selectFigure
        #     self.selectFigureDop(self.selected_figure[0], self.selected_figure[1], int(x // 50)*50, int(y // 50)*50)
        #   File "gh\shogi_field.py", line 185, in selectFigureDop
        #     if not fu.data(3):
        # RuntimeError: wrapped C/C++ object of type QGraphicsTextItem has been deleted
        ###
        
        # if self.radioButton_2.isChecked() and self.listWidget.count() % 2 == 0:
        #     print(self.listWidget.count())
        #     self.engineMove()
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
        # self.tableWidget.clear() #?
        self.graphicsView.scene().drawAll(startpos, silence=True)
        self.engineAnalisis()

    def engineMove(self):
        start_pos = self.graphicsView.scene().transl.getBoard()
        bst_mov = self.eng.cp_of_next_move(start_pos, depth=17)[0]
        self.updateMoves(bst_mov)
        # self.listWidget.setCurrentRow(self.listWidget.count()-1)
        self.tableWidget.setCurrentCell(self.tableWidget.rowCount()-1, 0)
        
    def engineAnalisis(self):
        # как определяет позиция? перенести в some_analisis_stuff
        start_pos = self.graphicsView.scene().transl.getBoard()
        bst_mov = ""
        # найти cp за лучший рекомендуемый следующий ход
        temp_because_yaneoura_besit = self.eng.cp_of_next_move(start_pos, depth=17)
        if temp_because_yaneoura_besit[1] == -111111111:
            bst_mov = temp_because_yaneoura_besit[0]
            mov_cp, mov_cp_40000, mov_cp_localMax = self.eng.cp_of_current_move(start_pos, bst_mov, depth=17)
        else:
            bst_mov,mov_cp = temp_because_yaneoura_besit
            mov_cp_40000 = mov_cp
            mov_cp_localMax = mov_cp
            mov_cp = int(min(abs(mov_cp),10000)*np.sign(mov_cp))
        if (self.tableWidget.rowCount() - 1) % 2 == 0:
            temp_sign = 1
        else:
            temp_sign = -1
        print(temp_sign, end=' ')
        if self.plainTextEdit.toPlainText() != '':
            # разберись со знаками...
            print(int(self.plainTextEdit.toPlainText().split()[-1]), mov_cp, self.last_cp, str(-temp_sign*(-self.last_cp - (np.sign(mov_cp)*temp_sign)*mov_cp)))
            self.plainTextEdit.setPlainText("Изменение оценки позиции в результате хода = " + str(-temp_sign*(-self.last_cp - (np.sign(mov_cp)*temp_sign)*mov_cp)))
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, 1, QTableWidgetItem(str(-temp_sign*(-self.last_cp - (np.sign(mov_cp)*temp_sign)*mov_cp))))
        else:
            self.plainTextEdit.setPlainText("Изменение оценки позиции в результате хода = " + str(mov_cp))
            self.tableWidget.setItem(self.tableWidget.rowCount()-1, 1, QTableWidgetItem(str(mov_cp)))
            print('-', mov_cp ,self.last_cp, '-')
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