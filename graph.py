import sympy as sp
from parser import parser
from matplotlib.pyplot import plot
from mpl_toolkits import mplot3d
from matplotlib import contour
from numpy.fft import fft, fft2, fftfreq
import numpy as np
# from matplotlib import rcParams

# определяем класс для хранения данных графиков
class dataGraph():

    def __init__(self, name, num, parser, parent):  # перечисляем все параметры
        self.name = name  # number
        self.num = num
        self.parseEqn = parser
        self.parent = parent
        self.initParam()
    def initParam(self):
        self.symbolsType = type(sp.symbols(']'))
        self.show = True
        self.color = None  # use как cmap lkz 3d surface
        self.leftPart = ''
        self.rightPart = ''
        self.xposition = 0  # координаты в сетке
        self.yposition = 0  # корды при входе надо ПУТАТЬ!!!
        self.origxpos = 0
        self.origypos = 0  # начальные корды
        self.parametric = {}
        self.axis = []
        self.xlim = ()  # (f,f)
        self.ylim = ()
        self.zlim = ()
        self.recognizeFuncLeft = None
        self.recognizeFuncRight = None
        self.plotData = None  # список координат
        self.graphDem = '2D'
        self.graphType = 'Norm'
        self.stride = (10, 10)  # размер ячейки, только для 3D wireframe
        # cParams.update({'figure.autolayout': True})
        # данные для построения графика
        self.x = None
        self.y = None
        self.z = None
        # данные для fft
        self.SigFFT = []
        self.SFreq = []
        self.fftxpos = None
        self.fftypos = None
        self.userDefineFFT = False
        self.fftshow = True
        # данные для суммы
        self.infoPart = None
        self.NeedSubs = False
        self.expressedVar = None
        self.listType2d = ['norm', 'implicit']
        self.listType3d =['norm', 'contour', 'wireframe']
        
    def updateFunc(self, eqn):
        self.parseEqn.parseParam(self, eqn)
        if self.leftPart == '' or self.rightPart == '':
            return  # ошибка
        '''
        if self.leftPart != self.list_param['leftPart']:
            self.leftPart = self.list_param['leftPart']
            self.recognizeFuncLeft, self.recognizeVarLeft = self.parseEqn.parserEqn(
                self.list_param['leftPart'], self.num)
        if self.rightPart != self.list_param['rightPart']:
            self.rightPart = self.list_param['rightPart']
            recognizeFunc = self.parseEqn.parserEqn(
                self.list_param['rightPart'], self.num)
            if recognizeFunc != None:
                self.recognizeFuncRight, self.recognizeVarRight = recognizeFunc
        '''
        self.parseEqn.parserEqn(self, 'left')
        self.parseEqn.parserEqn(self, 'right')
        
        if self.NeedSubs:
            # self.ListSubs = self.list_param['ListSubs']
            keysObj = list(self.parent.KnownAxis.keys())  # объекты
            keys = list([i.name for i in keysObj])
            # self.ListSubs = list(sp.symbols(' '.join(self.ListSubs)))
            # проверяем правую часть
            print('need subs')
            print(self.ListSubs)
            for currAx in self.recognizeVarRight:
                print(currAx, currAx in self.ListSubs) 
                if currAx in self.ListSubs:  # надо ли заменять
                    print(currAx)
                    if currAx in keys:
                        ind=keys.index(currAx)
                    else:
                        continue
                    if len(self.parent.KnownAxis[keysObj[ind]]) == 1:
                        self.recognizeFuncRight = self.recognizeFuncRight.subs(
                            keysObj[ind], self.parent.list_eqn[list(self.parent.KnownAxis[keysObj[ind]])[0]].infoPart)
                        print('Subs')
                    elif len(self.parent.KnownAxis[keysObj[ind]]) > 1:
                        self.parent.parent.showErrorEqn(
                            self.num, 'Переменная ' + str(currAx) + ' была определена несколько раз')
            # проверяем левую часть
            for currAx in self.recognizeVarLeft:
                if currAx in self.ListSubs:  # надо ли заменять
                    if currAx in self.parent.KnownAxis.keys() and len(self.parent.KnownAxis[currAx]) == 1:
                        self.recognizeFuncLeft = self.recognizeFuncLeft.subs(
                            currAx, self.parent.list_eqn[self.parent.KnownAxis[currAx][0]].infoPart)
            # добавить проверки на количество осей и параметры
        self.plotGraph()
    def plotGraph(self):
        if self.recognizeFuncLeft == None or self.recognizeFuncRight == None:
            return 0
        if type(self.recognizeFuncLeft) == self.symbolsType:
            plotPart=self.recognizeFuncRight
            self.infoPart=self.recognizeFuncRight
            self.expressedVar=self.recognizeFuncLeft
        elif type(self.recognizeFuncRight) == self.symbolsType:
            plotPart = self.recognizeFuncLeft
            self.infoPart = self.recognizeFuncLeft
            self.expressedVar = self.recognizeFuncRight
        elif self.graphType != 'implicit':
            self.graphType = 'implicit'
            self.infoPart = 0
        match self.graphDem:
            case '2D':
                if self.graphType == 'implicit':
                    self.plotData = sp.plot_implicit(
                        sp.Eq(self.recognizeFuncLeft, self.recognizeFuncRight), xlim=self.xlim, ylim=self.ylim, show=False)
                else:
                    self.plotData = sp.plot(
                        plotPart, show=False)
                    # (self.recognizeFuncRight, self.xlim[0], self.xlim[1])
                    # self.plotData.show()
            case '3D':
                self.plotData = sp.plot3d(
                    plotPart, xlim=self.xlim, ylim=self.ylim, zlim=serlf.zlim, show=False)
            case _:
                self.parent.parent.showErrorEqn(
                    self.num, 'Неизвестная размерность графика')
    def move_sympyplot_to_axes(p, ax):
        backend = p.backend(p)
        backend.ax = ax
        backend._process_series(
            backend.parent._series, ax, backend.parent)
        plt.close(backend.fig)
        
    def plotPLTGraph(self, ax):
        if self.plotData == None or self.show == False:
            return 0
        if not (self.fftshow):
            return
            '''
            if self.graphDem == '3D':
                ax.plot_surface()
            else:
                ax.plot()
            '''
        if self.graphDem == '2D':
            if self.graphType == 'Norm':
                if self.x == None or self.y == None:
                    self.x, self.y = self.plotData[0].get_data()
                ax.plot(self.x, self.y, color=self.color)
                '''
                if len(self.xlim) == 2:
                    ax.set_xlim(self.xlim)
                if len(self.ylim) == 2:
                    ax.set_ylim(self.ylim)
                    '''
            elif self.graphType == 'implicit':
                # не придумал как менять его цвет
                self.move_sympyplot_to_axes(self.plotData, ax) 
        elif self.graphDem == '3D':
            if self.graphType == 'Norm':
                if self.x == None or self.y == None or self.z == None:
                    self.x, self.y, self.z = self.plotData[0].get_meshes()
                ax.plot_surface(self.x, self.y, self.z, cmap=self.color)
            elif self.graphType == 'contour':
                if self.x == None or self.y == None or self.z == None:
                    self.x, self.y, self.z = self.plotData[0].get_meshes()
                ax.contour(self.x, self.y, self.z, cmap=self.color)
            elif self.graphType == 'wireframe':
                if self.x == None or self.y == None or self.z == None:
                    self.x, self.y, self.z = self.plotData[0].get_meshes()
                ax.plot_wireframe(self.x, self.y, self.z, color=self.color,
                                  rstride=self.stride[0], cstride=self.stride[1])

    def plotFFT(self, ax):
        if self.show == False:
            return
        elif self.x == None or self.y == None:
            return
        elif self.graphDem == '3D' and self.z == None:
            return 
        if self.graphDem == '2D' and self.graphType != 'implicit':
            if len(self.SigFFT) == 0 or len(self.SFreq) == 0:
                if len(self.y) < 1024:  # zero pathing
                    ffty = np.append(self.y, [0] * (1024 - len(self.y)))
                    fftx = np.append(self.x, [0] * (1024 - len(self.x)))
                else:
                    fftx = self.x
                    ffty = self.y
                self.SigFFT = fft(ffty)
                self.SigFFT = self.SigFFT / np.sum(np.abs(self.SigFFT))
                self.SFreq = fftfreq(len(fftx), d=(
                    max(fftx) - min(fftx)) / len(fftx))
            # дописать возможность изменения представления числа
            if 'real' in self.parent.complexPart:
                ax.plot(self.SFreq[1:-1], self.SigFFT.real[1:-1])
            if 'imag' in self.parent.complexPart:
                ax.plot(self.SFreq[1:-1], self.SigFFT.imag[1:-1])
            if 'abs' in self.parent.complexPart:
                ax.plot(self.SFreq[1:-1], np.abs(self.SigFFT[1:-1]))
 
        elif self.graphDem == '3D':
            pass  # я пока вообще хз как