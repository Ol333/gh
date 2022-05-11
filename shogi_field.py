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

    def moveFigure(self, x, y):
        fu = self.selected_figure[0]
        pol = self.selected_figure[1]
        newx =(x // 50)*50
        newy =(y // 50)*50
        lasti = 9 - self.selected_figure[2]
        lastj = self.selected_figure[3]
        self.selectFigureDop(fu, pol, newx, newy)
        usi_move = str(lasti)+'abcdefghi'[lastj]+str(9-int(x // 50))+'abcdefghi'[int(y // 50)]
        self.transl.addMove(usi_move)
        self.comm.updMoves.emit(usi_move)

    def selectFigure(self, fu, x, y):
        fu.setVisible(False)
        pol = self.itemAt(x, y, QTransform())
        fu.setVisible(True)
        if pol.data(0) == "Figure":
            if self.selected_figure != None:
                self.selectFigureDop(self.selected_figure[0], self.selected_figure[1])
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

