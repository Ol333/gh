from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QCheckBox,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit, QRadioButton,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow, QProgressBar,
QAction, QFileDialog, QDialog, QGraphicsScene, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsItemGroup)
from PyQt5.QtCore import (QRect, QCoreApplication, pyqtSignal, QObject, Qt,
QTranslator, QLocale, QPointF)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QColor, QPixmap, QPen, QBrush, QPolygonF, QFont, QTransform)

import kifu_translation

class MvScene(QGraphicsScene, QObject):
    worker = None
    selected_figure = None
    komodai_dict_0 = {'歩':[0, 460, 400], '桂':[0,510,400], '香':[0,460,350], '銀':[0,510,350], '金':[0,460,300], '角':[0,510,300],  '飛':[0,460,250]}
    komodai_dict_1 = {'歩':[0,-50,0], '桂':[0,-100,0], '香':[0,-50,50], '銀':[0,-100,50], '金':[0,-50,100], '角':[0,-100,100],  '飛':[0,-50,150]}
    figures_list_jp = ['歩', '王','玉', '飛', '角', '金', '銀', '桂', '香']
    figures_list_en = ['p', 'k', 'K', 'r', 'b', 'g', 's', 'n', 'l']

    def __init__(self, com):
        super().__init__()
        self.createDesk()
        self.transl = kifu_translation.Kifu_translator()
        self.comm = com
        figures = self.transl.posToDesk('7g7f')
        for f in figures:
            self.addFigure(f[0],f[1],f[2],f[3])
        for i in range(9):
            t = self.addText(str(i+1))
            t.setPos(420-i*50,450)
            t = self.addText('abcdefghi'[i])
            t.setPos(450,i*50+20)
        for k in self.komodai_dict_0:
            self.komodai_dict_0[k][0] = self.addText(str(0))
            self.komodai_dict_0[k][0].setPos(self.komodai_dict_0[k][1]-8, self.komodai_dict_0[k][2]-3)
        for k in self.komodai_dict_1:
            self.komodai_dict_1[k][0] = self.addText(str(0))
            self.komodai_dict_1[k][0].setPos(self.komodai_dict_1[k][1]-5, self.komodai_dict_1[k][2]-3)
        self.comm.updMoves.emit('7g7f') #вызов функции из главного окна
            
    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() == Qt.RightButton):
            self.placeBox(mouseEvent.scenePos().x(), mouseEvent.scenePos().y())
        if (mouseEvent.button() == Qt.LeftButton):
            item = self.itemAt(mouseEvent.scenePos(), QTransform())
            if (item):
                if (item.data(0) == "Figure"):
                    self.selectFigure(item, mouseEvent.scenePos().x(), mouseEvent.scenePos().y())
                if (item.data(0) == "Desk" and self.selected_figure != None):
                    self.moveFigure(mouseEvent.scenePos().x(), mouseEvent.scenePos().y())

    def createDesk(self):
        brush = QBrush(QColor(255, 255, 255), QPixmap("graphics/desk.jpg"))
        for i in range(9):
            for j in range(9):
                item = self.addRect(i*50.0,j*50.0,50.0,50.0, QPen(QColor(255, 255, 255)), brush)
                item.setData(0, "Desk")
        left_komodai = self.addRect(-105.0,0.0,100.0,200.0, QPen(QColor(255, 255, 255)), brush)
        left_komodai.setData(0, "Left komodai")
        right_komodai = self.addRect(455.0,250.0,100.0,200.0, QPen(QColor(255, 255, 255)), brush)
        right_komodai.setData(0, "Right komodai")
    
    def addFigure(self, side, i, j, name):
        polygon = QPolygonF()
        font = QFont()
        font.setPointSize(20)
        polygon << QPointF(20.0, 0.0) << QPointF(35.0, 6.0) << QPointF(40.0, 40.0) << QPointF(0.0, 40.0) << QPointF(5.0, 6.0) << QPointF(20.0, 0.0)
        pol = self.addPolygon(polygon)
        pol.setPos(5.0+i*50, 5.0+j*50)       
        fu = self.addText(name,font)
        fu.setPos(8.0+i*50, 5.0+j*50)
        if side == 1:
            pol.setTransform(QTransform(-1, 0, 0, -1, 40.0, 40.0))
            fu.setTransform(QTransform(-1, 0, 0, -1, 34.0, 40.0))
        pol.setData(0, "Figure")
        fu.setData(0, "Figure")
        fu.setData(1, side)
        fu.setData(2, name)
        fu.setData(3, False)
        fu.setData(4, False) # переворот

    def moveFigure(self, x, y):
        figure = self.selected_figure[0].data(2)
        figure = self.figures_list_en[self.figures_list_jp.index(figure)]
        if self.selected_figure[0].data(1) == 0:
            figure = figure.upper()
        figure_side = self.selected_figure[0].data(1)
        fu = self.selected_figure[0]
        pol = self.selected_figure[1]
        old_pos = self.selected_figure[2:]
        newx = (x // 50)*50
        newy = (y // 50)*50
        self.selectFigureDop(fu, pol, newx, newy)
        if 0 <= old_pos[0] < 9 and 0 <= old_pos[1] < 9:
            self.posSend(str(9-old_pos[0])+'abcdefghi'[old_pos[1]], int(x // 50), int(y // 50))
        else:
            self.posSend(figure+'*', int(x // 50), int(y // 50))
            if figure_side == 0:
                labelWidget = self.komodai_dict_0[self.figures_list_jp[self.figures_list_en.index(figure.lower())]][0]
            else:
                labelWidget = self.komodai_dict_1[self.figures_list_jp[self.figures_list_en.index(figure.lower())]][0]
            labelWidget.setPlainText(str(int(labelWidget.toPlainText())-1))

    def posSend(self, old_or_figure, new_i, new_j):
        usi_move = old_or_figure+str(9-new_i)+'abcdefghi'[new_j]
        self.transl.addMove(usi_move)
        self.comm.updMoves.emit(usi_move)

    def selectFigure(self, fu, x, y):
        fu.setVisible(False)
        pol = self.itemAt(x, y, QTransform())
        fu.setVisible(True)
        if pol.data(0) == "Figure":
            if self.selected_figure == None: # выбор фигуры
                self.selectFigureDop(fu, pol)            
                self.selected_figure = [fu, pol, int(x // 50), int(y // 50)]
            else:
                if self.selected_figure[0] == fu:
                    self.selectFigureDop(self.selected_figure[0], self.selected_figure[1]) # выбор другой фигуры
                else:
                    if self.selected_figure[0].data(1) != fu.data(1): # захват
                        self.posSend(str(9-self.selected_figure[2])+'abcdefghi'[self.selected_figure[3]], int(x // 50), int(y // 50))
                        self.selectFigureDop(self.selected_figure[0], self.selected_figure[1], int(x // 50)*50, int(y // 50)*50)
                        if fu.data(1) == 0:
                            fu.setData(1,1)
                            new_x, new_y = self.komodai_dict_1[fu.data(2)][1:]
                            self.komodai_dict_1[fu.data(2)][0].setPlainText(str(int(self.komodai_dict_1[fu.data(2)][0].toPlainText())+1))
                            self.selectFigureDop(fu, pol, new_x, new_y)
                            self.selectFigureDop(fu, pol)
                        else:
                            fu.setData(1,0)
                            new_x, new_y = self.komodai_dict_0[fu.data(2)][1:]
                            self.komodai_dict_0[fu.data(2)][0].setPlainText(str(int(self.komodai_dict_0[fu.data(2)][0].toPlainText())+1))
                            self.selectFigureDop(fu, pol, new_x, new_y)
                            self.selectFigureDop(fu, pol)
                    else:
                        self.selectFigureDop(self.selected_figure[0], self.selected_figure[1]) # сброс выделения
                        self.selectFigureDop(fu, pol)            
                        self.selected_figure = [fu, pol, int(x // 50), int(y // 50)]
    
    def selectFigureDop(self, fu, pol, dopx=0, dopy=0):
        new_value = 1.0
        if not fu.data(3):
            new_value = 1.1
        else:
            self.selected_figure = None
            
        if fu.data(1) == 0:
            fu.setTransform(QTransform(new_value, 0, 0, new_value, 0.0, 0.0))
            pol.setTransform(QTransform(new_value, 0, 0, new_value, 0.0, 0.0))
        else:
            fu.setTransform(QTransform(-new_value, 0, 0, -new_value, 34.0, 40.0))
            pol.setTransform(QTransform(-new_value, 0, 0, -new_value, 40.0, 40.0))
        fu.setData(3, not fu.data(3))

        if dopx != 0:
            pol.setPos(5.0+dopx, 5.0+dopy)
            fu.setPos(8.0+dopx, 5.0+dopy)
        

