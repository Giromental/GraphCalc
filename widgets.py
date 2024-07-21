# from  __init__.py import *#импортируем все импорты
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QMenu,
    QLabel, QToolBar, QAction, QStatusBar,
    QVBoxLayout, QFrame, QSplitter, QStyleFactory,
    QGridLayout, QLineEdit, QWidget, QPushButton,
    QScrollArea, QFormLayout, QGroupBox, QWidget
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from PyQt5.QtGui import QKeySequence, QFont
#from graph import dataGraph
# from parser import parser
from plotter import plotter
# from pyqtgraph import PlotWidget
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
import sympy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# import resources.qrc

# наследуемся от некоторых объектов

class Window(QMainWindow): #Создаем главное окно приложения
    def __init__(self, parent=None): 
        super().__init__(parent)
        Font = QFont("Courier", 12)
        app.setFont(Font)
        self.setWindowTitle("Cos calc")
        self.PlotGraph = plotter(self)
        self.resize(MainWindowSize[0], MainWindowSize[1])  # размеры
        self._initialData()
        self._createActions()
        self._createMenuBar()
        # self._createToolBarActions()
        # self._createToolBars()
        self._createStatusBar()
        self._connectActions()
        self._createFrames()
        
        # self._createContextMenu()
    # @property
    def _initialData(self):
        # здесь гениальным образом загружаем данные их xml
        # и переопределяем параметры
        self.countEqn = 1
        self.eqnDict = {}

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Вкладка - Файл
        fileMenu = menuBar.addMenu("&Файл")
        
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        # Вкладка Правка
        editMenu = menuBar.addMenu("&Правка")
        
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        # Вкладка Помощь
        helpMenu = menuBar.addMenu("&Помощь")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)
        
    def _createToolBars(self):  # создаем toolBar
        MainToolBar = QToolBar()
        MainToolBar.setIconSize(QSize(32, 32))
        MainToolBar.setFloatable(False)  # нельзя перетаскивать
        # MainToolBar.floating(False)
        # MainToolBar.setNativeToolBar(False)
        MainToolBar.setMovable(False)
        self.addToolBar(MainToolBar)
        # self.Toolbars.setContextMenuPolicy(Qt.ActionsContextMenu)
        

        MainToolBar.addAction(self.runAction)
        MainToolBar.addAction(self.breakAction)
        

        #editToolBar = QToolBar("Edit", self)
        #self.addToolBar(editToolBar)
        #helpToolBar = QToolBar("Help", self)
        #self.addToolBar(Qt.LeftToolBarArea, helpToolBar)

    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready", 3000)
        
    def _createActions(self):
        self.newAction = QAction("&Новый", self)
        self.openAction = QAction("&Открыть...", self)  # пример
        self.saveAction = QAction("&Сохранить", self)
        self.exitAction = QAction("&Выход", self)
        self.copyAction = QAction("&Копировать", self)
        self.pasteAction = QAction("&Вставить", self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.cutAction = QAction("&Вырезать", self)
        self.helpContentAction = QAction(
            "&Инструкция по началу работы", self)
        self.aboutAction = QAction("&О программе", self)
        
        self.copyAction.setShortcut(QKeySequence.Copy)
        self.pasteAction.setShortcut(QKeySequence.Paste)
        self.cutAction.setShortcut(QKeySequence.Cut)

    def _createToolBarActions(self):
        # Действия на tolbar
        self.runAction = QAction(
            QIcon("resources/PLAY.svg"), "Построить графики", self)
        self.breakAction = QAction(
            QIcon("resources/STOP.svg"), "Остановить выполнение", self)
        
    def _createContextMenu(self):
        # Определяем контекстное меню
        self.centralWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        # добавляем действия в контекстное меню
        self.centralWidget.addAction(self.newAction)
        self.centralWidget.addAction(self.openAction)
        self.centralWidget.addAction(self.saveAction)
        self.centralWidget.addAction(self.copyAction)
        self.centralWidget.addAction(self.pasteAction)
        self.centralWidget.addAction(self.cutAction)

    @pyqtSlot()
    def _connectActions(self):
        self.exitAction.triggered.connect(self.close)

    def _createFrames(self):
        global eqn_list  # eqnLayout
        hbox = QGridLayout(self)
        
        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)
        topleft.setMinimumHeight(200)
        topleft.setMinimumWidth(100)
        
        '''
        topleft = QScrollArea(self)
        topleft.setFrameShape(QFrame.StyledPanel)
        topleft.setMinimumHeight(200)
        topleft.setMinimumWidth(100)
        '''
        
        self.right = QFrame(self)
        self.right.setFrameShape(QFrame.StyledPanel)

        self.bottomleft = QFrame(self)
        self.bottomleft.setFrameShape(QFrame.StyledPanel)
        self.bottomleft.setMinimumWidth(100)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(topleft)
        #splitter1.addWidget(scroll)
        splitter1.addWidget(self.bottomleft)

        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.right)

        box_list = QVBoxLayout(topleft)
        self.eqn_list = QGroupBox()
        
        # добавляем поля ввода
        eqn = QLineEdit(self.eqn_list)
        self.QSizeEqnLine = eqn.sizeHint().height()
        # eqn.setAlignment(Qt.AlignTop)
        new_eqn = QPushButton(self)
        new_eqn.setIcon(QIcon("resources/PLUS.svg"))
        new_eqn.setIconSize(QSize(32, 32))

        showEqn = QPushButton(self.eqn_list)
        showEqn.setIcon(QIcon("resources/SHOW.svg"))
        showEqn.setIconSize(QSize(self.QSizeEqnLine, self.QSizeEqnLine))
        # добавляем действия
        showEqn.clicked.connect(self.eqnShow)
        # showEqn.released.connect(self.eqnShowOn)
        
        self.eqnLayout = QFormLayout()  # поле для полей ввода
        self.eqnLayout.addRow(showEqn, eqn)
        eqn.setObjectName("eqn0")
        showEqn.setObjectName("IconEqn0")
       # print(showEqn.isChecked())
        showEqn.setCheckable(True)
        showEqn.setChecked(False)
        showEqn.setStyleSheet('border: none')
        # print(showEqn.isChecked())

        self.eqn_list.setLayout(self.eqnLayout)
        scroll = QScrollArea()
        scroll.setWidget(self.eqn_list)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)

        box_list.addWidget(scroll)
        box_list.addWidget(new_eqn, alignment=Qt.AlignHCenter |
                           Qt.AlignTop)  # выравниваем фигуру

        # инициализируем сигналы
        new_eqn.clicked.connect(self.addNewEqn)
        eqn.editingFinished.connect(self.myfunc)
        # new_eqn.linkHovered.connect(self.linkHovered)

        # graphBox = QVBoxLayout(self.right)
        # self.GraphLayout = QLabel()
        # self.fig = Figure()
        # self.fig.add_gridspec(sp.plotting.PlotGrid(1, 1, grid=True))
        # self.canvas = FigureCanvas(self.fig)
        # self.plotObject = fig.add_subplot()
        # s = sp.plot('', show=False)
        # self.plotObject.plot(s)
        # Graph = QPixmap('resources/warning.svg')
        #Graph.scaled(0, 0, Qt.IgnoreAspectRatio)
        # self.GraphLayout.setPixmap(Graph)
        #self.GraphLayout.resize(right.sizeHint())
        # self.GraphLayout.adjustSize()
        #self.GraphLayout.setAlignment(Qt.AlignCenter)
        # graphBox.addWidget(self.GraphLayout)
        # self.GraphLayout.setScaledContents(True)
        # self.GraphLayout.sca

        hbox.addWidget(splitter2)
        central_widget=QWidget()
        central_widget.setLayout(hbox)
        self.setCentralWidget(central_widget)
        self.createGraphFrame()
        self.createToolFrame()
        
    def createGraphFrame(self):
        self.canvas = FigureCanvas(self.PlotGraph.fig)
        self.canvas.figure = self.PlotGraph.fig
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.GraphLayout = QVBoxLayout()
        self.GraphLayout.addWidget(self.toolbar)
        self.GraphLayout.addWidget(self.canvas)
        self.right.setLayout(self.GraphLayout)
        self.canvas.draw()
        self.canvas.flush_events()

    def createToolFrame(self):
        # self.bottomleft.setStyleSheet('QFrame {border: none}')
        self.settingLayout = QVBoxLayout()  # self.bottomleft)
        self.settingLayout.setSpacing(0)
        self.settingLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        settingWidget = QWidget(self.bottomleft)
        settingWidget.setLayout(self.settingLayout)
        # settingWidget.setStyleSheet('border: none')
        
        ScrollArea = QScrollArea(self.bottomleft)
        ScrollArea.setWidget(settingWidget)
        ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        ScrollArea.setWidgetResizable(True)
        ScrollArea.setStyleSheet('QScrollArea {border:none;}')

        widget = QVBoxLayout(self.bottomleft)
        widget.addWidget(ScrollArea)
        widget.setContentsMargins(0, 0, 0, 0)
        # widget.setStyleSheet('border: none')
        self.setDict = dict()  # {buttonName:(group_box, button)}
        self.createFFTList()
        self.createComplexIntList()
        # self.PlotGraph.fftPlot = 'on_bottom'  # создать под это выпадающее меню

    def createFFTList(self):
        group_box = QGroupBox()  # 'Настройки отображения спектра')
        buttonList = []
        toggle_button = QPushButton('Отображение спектра')
        toggle_button.setIcon(QIcon('resources/MINUS.svg'))
        
        SpectrumShow = QVBoxLayout()
        self.settingLayout.addWidget(
            toggle_button, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.settingLayout.addWidget(group_box, alignment=Qt.AlignLeft |
                           Qt.AlignTop)
        # self.setBoxes.append(group_box)
        # content = QWidget()
        # создаем кнопки
        ShowBottom = QPushButton(
            'Отображать спектр под графиком')
        ShowRight = QPushButton(
            'Отображать спектр справа от графика')
        ShowTop = QPushButton(
            'Отображать спектр над графиком')
        ShowLeft = QPushButton(
            'Отображать спектр слева от графика')
        ShowOff = QPushButton(
            'Отключить отображение спектра')
        # добавляем иконки
        ShowBottom.setIcon(QIcon('resources/CIRCLECHECK-ON.svg'))
        ShowLeft.setIcon(QIcon('resources/CIRCLECHECK-OFF.svg'))
        ShowRight.setIcon(QIcon('resources/CIRCLECHECK-OFF.svg'))
        ShowTop.setIcon(QIcon('resources/CIRCLECHECK-OFF.svg'))
        ShowOff.setIcon(QIcon('resources/CIRCLECHECK-OFF.svg'))
        self.PlotGraph.fftPlot = 'bottom'
        # присваиваем имена
        ShowBottom.setObjectName('bottom')
        ShowTop.setObjectName('top')
        ShowLeft.setObjectName('left')
        ShowRight.setObjectName('right')
        ShowOff.setObjectName('FFTOff')
        toggle_button.setObjectName('SpectrumShow')
        # задаем стили
        toggle_button.setStyleSheet("border:none")
        ShowBottom.setStyleSheet("border:none")
        ShowLeft.setStyleSheet("border:none")
        ShowRight.setStyleSheet("border:none")
        ShowTop.setStyleSheet("border:none")
        ShowOff.setStyleSheet("border:none")
        group_box.setStyleSheet(
            "QWidget {border:none; border-left: 2px solid gray; padding-left: 10px;}")
        # подключаем действия
        ShowBottom.clicked.connect(self.changeSpectrumShow)
        ShowLeft.clicked.connect(self.changeSpectrumShow)
        ShowRight.clicked.connect(self.changeSpectrumShow)
        ShowTop.clicked.connect(self.changeSpectrumShow)
        ShowOff.clicked.connect(self.changeSpectrumShow)
        # добавляем проверки
        ShowBottom.setCheckable(True)
        ShowLeft.setCheckable(True)
        ShowRight.setCheckable(True)
        ShowTop.setCheckable(True)
        ShowOff.setCheckable(True)
        # устанавливам начальные состояния
        ShowBottom.setChecked(True)
        ShowLeft.setChecked(False)
        ShowRight.setChecked(False)
        ShowTop.setChecked(False)
        ShowOff.setChecked(False)
        # отображаем
        SpectrumShow.addWidget(ShowOff, alignment=Qt.AlignLeft |
                           Qt.AlignTop)
        SpectrumShow.addWidget(ShowBottom, alignment=Qt.AlignLeft |
            Qt.AlignTop)
        SpectrumShow.addWidget(ShowTop, alignment=Qt.AlignLeft |
                           Qt.AlignTop)
        SpectrumShow.addWidget(ShowRight, alignment=Qt.AlignLeft |
                           Qt.AlignTop)
        SpectrumShow.addWidget(ShowLeft, alignment=Qt.AlignLeft |
                           Qt.AlignTop)
        group_box.setLayout(SpectrumShow)

        # Добавление кнопки для управления видимостью группы
        # toggle_button.setAl
        self.setDict.update({toggle_button.objectName(): (group_box, toggle_button)})
        toggle_button.clicked.connect(self.changeGroupVisible)
        toggle_button.click()  # скрываем кнопки
        self.SpecShowButtonList = [ShowBottom, ShowLeft, ShowOff, ShowRight, ShowTop] 
        
    def createComplexIntList(self):
        group_box = QGroupBox()  # 'Настройки отображения спектра')
        buttonList = []
        toggle_button = QPushButton('Отображение комплексных величин')
        toggle_button.setIcon(QIcon('resources/MINUS.svg'))
        # toggle_button.setParent(toggle_button)
        
        ComplexPart = QVBoxLayout()  # toggle_button)  # content)
        self.settingLayout.addWidget(
            toggle_button, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.settingLayout.addWidget(group_box, alignment=Qt.AlignLeft |
                           Qt.AlignTop)
        # self.setBoxes.append(group_box)
        # content = QWidget()
        # создаем кнопки
        imagPart = QPushButton(
            'Отображать мнимую часть спектра')
        realPart = QPushButton(
            'Отображать действительную часть спектра')
        absPart = QPushButton(
            'Отображать модуль спектра (по умолчанию)')
        # добавляем иконки
        imagPart.setIcon(QIcon('resources/SQUARECHECK-OFF.svg'))
        realPart.setIcon(QIcon('resources/SQUARECHECK-OFF.svg'))
        absPart.setIcon(QIcon('resources/SQUARECHECK-ON.svg'))
        self.PlotGraph.complexPart = ['abs']
        # присваиваем имена
        imagPart.setObjectName('imag')
        realPart.setObjectName('real')
        absPart.setObjectName('abs')
        toggle_button.setObjectName('Complexpart')
        # задаем стили
        toggle_button.setStyleSheet("border:none")
        imagPart.setStyleSheet("border:none")
        realPart.setStyleSheet("border:none")
        absPart.setStyleSheet("border:none")
        group_box.setStyleSheet(
            "QWidget {border:none; border-left: 2px solid gray; padding-left: 10px;}")
        # подключаем действия
        imagPart.clicked.connect(self.changeComplexPart)
        realPart.clicked.connect(self.changeComplexPart)
        absPart.clicked.connect(self.changeComplexPart)
        # добавляем проверки
        imagPart.setCheckable(True)
        realPart.setCheckable(True)
        absPart.setCheckable(True)
        # устанавливам начальные состояния
        imagPart.setChecked(False)
        realPart.setChecked(False)
        absPart.setChecked(True)
        # отображаем
        ComplexPart.addWidget(imagPart, alignment=Qt.AlignLeft |
                           Qt.AlignTop)
        ComplexPart.addWidget(realPart, alignment=Qt.AlignLeft |
            Qt.AlignTop)
        ComplexPart.addWidget(absPart, alignment=Qt.AlignLeft |
                           Qt.AlignTop)
        group_box.setLayout(ComplexPart)

        # Добавление кнопки для управления видимостью группы
        # toggle_button.setAl
        self.setDict.update({toggle_button.objectName(): (group_box, toggle_button)})
        toggle_button.clicked.connect(self.changeGroupVisible)
        toggle_button.click()  # скрываем кнопки

    @pyqtSlot()
    def changeSpectrumShow(self):
        name = self.sender().objectName()
        QButton = self.sender()
        if QButton.isChecked():
            for i in self.SpecShowButtonList:
                if i.objectName() != name and i.isChecked():
                    i.setChecked(False)
                    i.setIcon(QIcon('resources/CIRCLECHECK-OFF.svg'))
            QButton.setIcon(QIcon('resources/CIRCLECHECK-ON.svg'))
            self.PlotGraph.fftPlot = name
        else:
            for i in self.SpecShowButtonList:
                if i.objectName() == 'FFTOff':
                    i.setChecked(True)
                    i.setIcon(QIcon('resources/CIRCLECHECK-ON.svg'))
                    self.PlotGraph.fftPlot = 'FFTOff'
                elif i.objectName() == name:
                    i.setIcon(QIcon('resources/CIRCLECHECK-OFF.svg'))
        self.PlotGraph.replotGraph()
        self.ReDrawCanvas()
    @pyqtSlot()
    def changeComplexPart(self):
        QButton = self.sender()
        if QButton.isChecked():
            self.PlotGraph.complexPart.append(QButton.objectName())
            QButton.setIcon(QIcon('resources/SQUARECHECK-ON.svg'))
        else:
            self.PlotGraph.complexPart.remove(QButton.objectName())
            QButton.setIcon(QIcon('resources/SQUARECHECK-OFF.svg'))
        self.PlotGraph.resizeSubPlot()  # перестраиваем все в соот с новыми настроками
        self.ReDrawCanvas()
    @pyqtSlot()
    def changeGroupVisible(self):
        name = self.sender().objectName()
        CDict = self.setDict[name]
        if CDict[0].isHidden():
            CDict[1].setIcon(QIcon('resources/MINUS.svg'))  # not black
            CDict[0].setHidden(False)
        else:
            CDict[1].setIcon(QIcon('resources/PLUS.svg'))
            CDict[0].setHidden(True)



    @pyqtSlot()
    def addNewEqn(self):
        eqn1 = QLineEdit(self.eqn_list)
        showEqn = QPushButton(self.eqn_list)
        showEqn.setIcon(QIcon("resources/SHOW.svg"))
        showEqn.setIconSize(QSize(self.QSizeEqnLine, self.QSizeEqnLine))
        showEqn.setCheckable(True)
        showEqn.setStyleSheet('border: none')
        # добавляем действия
        showEqn.clicked.connect(self.eqnShow)
        
        self.eqnLayout.addRow(showEqn, eqn1)
        eqn1.editingFinished.connect(self.myfunc)
        eqn1.setObjectName(str("eqn" + str(self.countEqn)))
        showEqn.setObjectName(str("IconEqn" + str(self.countEqn)))
        self.countEqn += 1

    @pyqtSlot()
    def myfunc(self):
        name = self.sender().objectName()
        newEquation = self.sender().text()
        Button = self.eqn_list.findChildren(
            QPushButton, 'IconEqn' + name[3:])[0]
        if not (Button.isEnabled()):
            Button.setEnabled(True)
            Button.click()
        self.PlotGraph.addNewEqn(newEquation, name)
        self.ReDrawCanvas()
        # переадресация на парсер
    @pyqtSlot()
    def eqnShow(self):
        QButton = self.sender()
        if not(QButton.isChecked()):
            # print('Кнопка вверх')
            QButton.setIcon(QIcon("resources/SHOW.svg"))
            QButton.setIconSize(QSize(self.QSizeEqnLine, self.QSizeEqnLine))
            QButton.setToolTip('')
            self.PlotGraph.changeVisible(QButton.objectName(), True)
        else:
            #print('Кнопка вниз')
            QButton.setIcon(QIcon("resources/SHOW-OFF.svg"))
            QButton.setIconSize(QSize(self.QSizeEqnLine, self.QSizeEqnLine))
            QButton.setToolTip('')
            self.PlotGraph.changeVisible(QButton.objectName(), False)
        self.ReDrawCanvas()
    def showErrorEqn(self, number, strErr):
        # ErrEqn = self.eqn_list.findChildren(QLineEdit, 'eqn' + str(number))
        ErrQButton = self.eqn_list.findChildren(
            QPushButton, 'IconEqn' + str(number))
        ErrQButton = ErrQButton[0]
        if ErrQButton.isChecked() == False:
            ErrQButton.click()
        ErrQButton.setIcon(QIcon("resources/warning.svg"))
        ErrQButton.setIconSize(QSize(self.QSizeEqnLine, self.QSizeEqnLine))
        ErrQButton.setToolTip(strErr)
        ErrQButton.setEnabled(False)  # отключаем кнопку
    def ReDrawCanvas(self):
        self.GraphLayout.removeWidget(self.canvas)
        self.GraphLayout.removeWidget(self.toolbar)
        self.canvas = FigureCanvas(self.PlotGraph.fig)
        self.canvas.figure = self.PlotGraph.fig
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.GraphLayout.addWidget(self.toolbar)
        self.GraphLayout.addWidget(self.canvas)
        self.canvas.draw()
        self.canvas.flush_events()
# убрать в xml
global MainWindowSize
MainWindowSize = (1200, 800)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # menuBar = QMenu(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
    
