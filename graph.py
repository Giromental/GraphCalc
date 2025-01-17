import sympy as sp
from sympy.plotting import plot3d
from parser import parser
from matplotlib.pyplot import plot
from matplotlib import contour
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from numpy.fft import fft, fft2, fftfreq
import numpy as np
# from matplotlib import rcParams

# определяем класс для хранения данных графиков
class dataGraph():
    ''' объект отвечает за параметры отдельно взятого уравнения - размерность, коорд точек итд '''
    def __init__(self, name, num, parser, parent):  # перечисляем все параметры
        self.name = name  # number
        self.num = num
        self.parseEqn = parser
        self.parent = parent
        self.initParam()
    def initParam(self):
        ''' задаем начальное состояние параметров '''
        self.symbolsType = type(sp.symbols(']'))
        self.show = True
        self.color = None  # use как cmap lkz 3d surface
        self.cmap = None
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
        self.usergraphDem = None
        self.fftshow = True
        # данные для суммы
        self.infoPart = None
        self.NeedSubs = False
        self.expressedVar = None

        
    def updateFunc(self, eqn, new):
        ''' получаем параметры уравнения '''
        xp, yp = self.xposition, self.yposition
        xfft, yfft = self.fftxpos, self.fftypos
        self.varOld = self.expressedVar
        if not (new):
            self.initParam()
        self.parseEqn.parseParam(self, eqn)
        checkedResize = False
        if xp != None and yp != None:
            if xp != self.xposition or yp != self.yposition:
                if (xp, yp) in self.parent.plotGrid.keys():
                    if len(self.parent.plotGrid[(xp, yp)]['numbers']) == 1:
                        del self.parent.plotGrid[(xp, yp)]
                        if xp == self.parent.maxxPos or yp == self.parent.maxyPos:
                            checkedResize = True
                    else:
                        self.parent.plotGrid[(xp, yp)]['numbers'].remove(
                            self.num)
                    self.parent.plotCurrEqn(xp, yp, True)
        if xfft != None and yfft != None:
            if xfft != self.fftxpos or yfft != self.fftypos:
                if (xfft, yfft) in self.parent.plotGrid.keys():
                    if len(self.parent.plotGrid[(xfft, yfft)]['numbers']) == 1:
                        del self.parent.plotGrid[(xfft, yfft)]
                        if xfft == self.parent.maxxPos or yfft == self.parent.maxyPos:
                            checkedResize = True
                    else:
                        self.parent.plotGrid[(xfft, yfft)
                                             ]['numbers'].remove(self.num)
                    self.parent.plotCurrEqn(xfft, yfft, True)
        if checkedResize:
            self.parent.checkNeedResize()
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
        if self.recognizeFuncLeft == None or self.recognizeFuncRight == None:
            return
        
        if self.NeedSubs:
            # self.ListSubs = self.list_param['ListSubs']
            keysObj = list(self.parent.KnownAxis.keys())  # объекты
            keys = list([i.name for i in keysObj])
            # self.ListSubs = list(sp.symbols(' '.join(self.ListSubs)))
            # проверяем правую часть
            for currAx in self.recognizeVarRight:
                if currAx in self.ListSubs:  # надо ли заменять

                    if currAx in keys:
                        ind=keys.index(currAx)
                    else:
                        continue
                    if len(self.parent.KnownAxis[keysObj[ind]]) == 1:
                        self.recognizeFuncRight = self.recognizeFuncRight.subs(
                            keysObj[ind], self.parent.list_eqn[list(self.parent.KnownAxis[keysObj[ind]])[0]].infoPart)
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
        self.defineDem()
        self.plotGraph()
    def plotGraph(self):
        ''' строим график sympy, как опорный при выводе графика на экран'''
        if self.recognizeFuncLeft == None or self.recognizeFuncRight == None:
            return
        if type(self.recognizeFuncLeft) == self.symbolsType:
            plotPart = self.recognizeFuncRight
            self.infoPart=self.recognizeFuncRight
            self.expressedVar=self.recognizeFuncLeft
        elif type(self.recognizeFuncRight) == self.symbolsType:
            plotPart = self.recognizeFuncLeft
            self.infoPart = self.recognizeFuncLeft
            self.expressedVar = self.recognizeFuncRight
        elif self.graphType != 'implicit':
            self.graphType = 'implicit'
            self.infoPart = 0
        if self.expressedVar != None and self.varOld != None:
            if self.expressedVar.name != self.varOld.name:
                if self.varOld in self.parent.KnownAxis:
                    del self.parent.KnownAxis[self.varOld]
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
                self.plotData = plot3d(
                    plotPart, xlim=self.xlim, ylim=self.ylim, zlim=self.zlim, show=False)
            case _:
                self.parent.parent.showErrorEqn(
                    self.num, 'Неизвестная размерность графика')
    def move_sympyplot_to_axes(self, p, ax):
        backend = p.backend(p)
        backend.ax = ax
        backend._process_series(
            backend.parent._series, ax, backend.parent)
        plt.close(backend.fig)
        
    def plotPLTGraph(self, ax):
        ''' строим график для отображения на экране'''
        if self.plotData == None or self.show == False:
            return 
        if not (self.fftshow):
            return
        if self.graphDem == '2D':
            if self.graphType == 'norm':
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
                self.move_sympyplot_to_axes(self.plotData, ax) 
        elif self.graphDem == '3D':
            if not (hasattr(ax, 'get_zlim')):
                ax = self.parent.convertAxes23D(ax)
                ind = ax.get_subplotspec()
                xpos, ypos = ind.colspan[0], ind.rowspan[0]
                if (xpos, ypos) in self.parent.plotGrid.keys():
                    self.parent.plotCurrEqn(xpos, ypos, True)
                    # return
            if self.graphType == 'norm':
                if type(self.x) == type(None) or type(self.y) == type(None) or type(self.z) == type(None):
                    self.x, self.y, self.z = self.plotData[0].get_meshes()
                if self.cmap == None:
                    ax.plot_surface(self.x, self.y, self.z)
                else:
                    ax.plot_surface(self.x, self.y, self.z, cmap=self.cmap)
                    plt.show()
            elif self.graphType == 'contour':
                if type(self.x) == type(None) or type(self.y) == type(None) or type(self.z) == type(None):
                    self.x, self.y, self.z = self.plotData[0].get_meshes()
                if self.cmap == None:
                    ax.contour(self.x, self.y, self.z)
                else:
                    ax.contour(self.x, self.y, self.z, cmap=self.cmap)
                #ax.contour(self.x, self.y, self.z, cmap=self.color)
            elif self.graphType == 'wireframe':
                if type(self.x) == type(None) or type(self.y) == type(None) or type(self.z) == type(None):
                    self.x, self.y, self.z = self.plotData[0].get_meshes()
                if self.color != None:
                    ax.plot_wireframe(self.x, self.y, self.z, color=self.cmap,
                                  rstride=self.stride[0], cstride=self.stride[1])
                else:
                    ax.plot_wireframe(self.x, self.y, self.z,
                                  rstride=self.stride[0], cstride=self.stride[1])

    def plotFFT(self, ax):
        ''' строим FFT '''
        if self.show == False:
            return
        elif type(self.x) == type(None) or type(self.y) == type(None):
            return
        elif self.graphDem == '3D' and type(self.z) == type(None):
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
                ax.set_xlabel('Real Part')
            if 'imag' in self.parent.complexPart:
                ax.plot(self.SFreq[1:-1], self.SigFFT.imag[1:-1])
                ax.set_xlabel('Imag Part')
            if 'abs' in self.parent.complexPart:
                ax.plot(self.SFreq[1:-1], np.abs(self.SigFFT[1:-1]))
                ax.set_xlabel('Abs Part')
            ax.set_ylabel('Magnitude')

        elif self.graphDem == '3D':
            if not (hasattr(ax, 'get_zlim')):
                ax = self.parent.convertAxes23D(ax)
                ind = ax.get_subplotspec().num1
                xpos, ypos = ind // (self.parent.maxxPos +
                                     1), ind % (self.parent.maxyPos + 1)
                if (xpos, ypos) in self.parent.plotGrid.keys():
                    self.parent.plotCurrEqn(xpos, ypos, True)            
            data_3d = np.stack((self.x, self.y, self.z), axis=-1)
            # Применяем FFT
            fft_data = np.fft.fftn(data_3d)
            # ax.plot_surface(*fft_result)
            normalized_fft_data = np.abs(fft_data) / data_3d.size
            # ax.scatter(normalized_fft_data.real, normalized_fft_data.imag, c=normalized_fft_data.real)
            ax.plot_surface(np.real(normalized_fft_data[:, :, 0]), np.imag(
                normalized_fft_data[:, :, 1]), np.abs(normalized_fft_data[:, :, 2]))
            # plt.show()
            ax.set_xlabel('Real Part')
            ax.set_ylabel('Imaginary Part')
            ax.set_zlabel('Intensity')            

    def defineDem(self):
        ''' определяет реальную размерность уравнения '''
        cVarR, cVarL = self.recognizeFuncRight.atoms(
                sp.Symbol), self.recognizeFuncLeft.atoms(sp.Symbol)
        cVar = set()
        cVar.update(cVarR)
        cVar.update(cVarL)
        if (self.xposition, self.yposition) in self.parent.plotGrid.keys():
            Dem = self.parent.plotGrid[self.xposition,
                self.yposition]['graphDem']
        else:
            Dem = None
            # сюда допилить проверку параметров
        if len(cVar) == 3 or Dem == '3D':
            self.graphDem='3D'
            if (len(cVarR) == 0 and len(cVarL) == 3) or (len(cVarR) == 3 and len(cVarL) == 0) or (len(cVarR) == 2 and len(cVarL) == 2):
                self.graphType = 'implicit'
            else:
                self.graphType = 'norm'
        elif len(cVar) == 2 or len(cVar) == 1:
            self.graphDem = '2D'
            # if (len(cVarR) == 0 and len(cVarL) == 2) or (len(cVarR) == 2 and len(cVarL) == 0):
            if len(cVarL) == 2 or len(cVarR) == 2:
                self.graphType = 'implicit'
            else:
                self.graphType = 'norm'
        elif len(cVar) == 0:
            self.parent.parent.showErrorEqn(
                    self.num, 'В уравнении не обнаружено переменных')
            return
        else:
            self.parent.parent.showErrorEqn(
                    self.num, 'В уравнении более 3х независимых переменных')
            return
        if self.usergraphDem != None and self.usergraphDem != self.graphDem:
            if self.graphDem == '2D':
                if self.graphType == 'implicit':
                    self.parent.parent.showErrorEqn(
                        self.num, 'Невозможно преобразовать неявное уравнение в 3D')
                    return
                self.graphDem = '3D'
                if (self.xposition, self.yposition) in self.parent.plotGrid.keys():
                    self.parent.plotCurrEqn(
                        self.xposition, self.yposition, True)
            else:
                self.parent.parent.showErrorEqn(
                    self.num, 'Невозможно преобразовать 3D в 2D')
                return