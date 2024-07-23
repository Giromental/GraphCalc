import sympy as sp
import sympy.plotting as spp
from graph import dataGraph
from parser import parser
from matplotlib.pyplot import subplot, subplots, subplots_adjust


class plotter():
    
    def __init__(self, parent):
        # super().__init__(None)
        self.parent = parent
        self.parseEqn = parser(self)
        self.list_eqn = [None]  # все уравнения подряд
        self.set_axis = [set()]
        self.plotGrid = dict()  # список списков объектов
        # позиционнирование x/y начиная с 0
        self.maxxPos = 0
        self.maxyPos = 0
        self.cntEqn = 0
        self.fig, self.ax = subplots(
            self.maxxPos + 1, self.maxyPos + 1)  # , figsize=(1, 1))
        self.moveAxis(self.ax)
        subplots_adjust(top=1, bottom=0, right=1, left=0)
        # при очистке фигура удаляется и пересоздается, поэтому флаг показывает необходимость пересвязать canvas
        self.neededReDrow = False
        self.KnownAxis = dict()
        self.listType2d = ['norm', 'implicit']
        self.listType3d =['norm', 'contour', 'wireframe', 'implicit']        
        
    def addNewEqn(self, eqn, name):
        number = int(name[3:])
        new = False
        # проверка на пустое
        if eqn.strip() == '':
            if number <= self.cntEqn and self.list_eqn[number] != None:
                self.removeEqnInPlot(number)
            return
        # проверяем новизну графика
        if number > self.cntEqn:
            self.list_eqn.extend([None] * (number - self.cntEqn))
            self.cntEqn = number
            new = True
        if self.list_eqn[number] == None:
            obj = dataGraph(name, number, self.parseEqn, self)
            self.list_eqn[number] = obj
            new = True
        self.list_eqn[number].updateFunc(eqn, new)
        self.add2plot(number,
                      self.list_eqn[number].xposition, self.list_eqn[number].yposition, new)

    def add2plot(self, eqnNum, xpos, ypos, new):
        self.defineFFTPos(self.list_eqn[eqnNum])
        # определяем надобность изменения размеров
        xpos, ypos = self.list_eqn[eqnNum].xposition, self.list_eqn[eqnNum].yposition
        xfftPos, yfftPos = self.list_eqn[eqnNum].fftxpos, self.list_eqn[eqnNum].fftypos
        if xfftPos != None and yfftPos != None:
            if max(xfftPos, xpos) > self.maxxPos or max(yfftPos, ypos) > self.maxyPos:
                self.maxyPos = max(yfftPos, ypos, self.maxyPos)
                self.maxxPos = max(xfftPos, xpos, self.maxxPos)
                self.resizeSubPlot()
                # self.updateDict(eqnNum)
        else:
            if xpos > self.maxxPos or ypos > self.maxyPos:
                self.maxyPos = max(ypos, self.maxyPos)
                self.maxxPos = max(xpos, self.maxxPos)
                self.resizeSubPlot()
                # self.updateDict(eqnNum)
# определяем наличие уравнения в списке
        # if (xpos, ypos) not in self.plotGrid.keys() or (xfftPos, yfftPos) not in self.plotGrid.keys():
        #    self.updateDict(eqnNum)
        # if eqnNum not in self.plotGrid[(xpos, ypos)]['numbers']:
        #    self.plotGrid[(xpos, ypos)]['numbers'].append(eqnNum)
        # if xfftPos != None and yfftPos != None:
        #    if eqnNum not in self.plotGrid[(xfftPos, yfftPos)]['numbers']:
        #        self.plotGrid[(xfftPos, yfftPos)]['numbers'].append(eqnNum)
        self.updateDict(eqnNum)
        if new:
            if self.list_eqn[eqnNum].graphDem != self.plotGrid[(xpos, ypos)]:
                if self.checkNewEqn(eqnNum, False):  # все мб быть плохо
                    self.list_eqn[eqnNum].plotPLTGraph(
                        self.plotGrid[(xpos, ypos)]['ax'])
            if xfftPos != None and yfftPos != None:
                if self.checkNewEqn(eqnNum, True):
                    self.list_eqn[eqnNum].plotFFT(
                        self.plotGrid[(xfftPos, yfftPos)]['ax'])
        else:
            # перестраиваем все графики в это окне
            self.plotCurrEqn(xpos, ypos, True)
            self.plotCurrEqn(xfftPos, yfftPos, True)
        var = self.list_eqn[eqnNum].expressedVar
        if var != None:
            if var in self.KnownAxis.keys():
                self.KnownAxis[var].add(eqnNum)
            else:
                self.KnownAxis.update({var: {eqnNum}})
        # self.fig.close()
        # self.fig.show()
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.draw()
        # self.fig.show()
    def defineax(self, xpos, ypos):
        if self.maxxPos == 0:
            if self.maxyPos == 0:
                return self.ax
            else:
                return self.ax[ypos]
        elif self.maxyPos == 0:
            return self.ax[xpos]
        else:
            return self.ax[xpos, ypos]

    def resizeSubPlot(self):
        self.fig.clear()
        # self.fig.cla()
        # self.neededReDrow = True
        self.fig, self.ax = subplots(
            self.maxxPos + 1, self.maxyPos + 1)  # , figsize=(100, 100))
        # self.fig.show()
        subplots_adjust(top=1, bottom=0, right=1, left=0)
        for cyrrX in range(self.maxxPos + 1):
            for cyrrY in range(self.maxyPos + 1):
                if (cyrrX, cyrrY) in self.plotGrid.keys():
                    self.plotGrid[(cyrrX, cyrrY)]['ax'] = self.defineax(
                        cyrrX, cyrrY)
                    self.moveAxis(self.plotGrid[(cyrrX, cyrrY)]['ax'],
                                  self.plotGrid[(cyrrX, cyrrY)]['graphDem'] == '3D')
                else:
                    self.moveAxis(self.defineax(cyrrX, cyrrY))
        for currEqn in self.plotGrid.keys(): # строим графики
            self.plotCurrEqn(*currEqn)

    def checkType(self, dictEqn):  # переписать целиком
        lType, lDem = [], []
        for i in dictEqn['numbers']:
            lType.append(self.list_eqn[i].graphType)
            lDem.append(self.list_eqn[i].graphDem)
        sType = set(lType)
        sDem = set(lDem)
        fNorm = any(
            x in self.listType2d or x in self.listType3d for x in sType)
        # fImp = 'implicit' in sType
        fFFT = 'fft' in sType or 'fft2' in sType
        fImp = 'implicit' in sType
        if len(sDem) == 1 and len(sType) == 1:  # все хорошо
            # if list(sDem)[0] != dictEqn['graphDem']:
            dictEqn['graphDem'] = list(sDem)[0]
           # if list(sType)[0] != dictEqn['graphType']:
            #    dictEqn['graphType'] = list(sType)[0]
            return True
        elif len(sDem) == 2:
            if len(sType) == 1:
                return True
            # elif fImp:
            #    return False
            elif fFFT and fNorm:
                return False
            else:
                dictEqn['graphDem']='3D'
                dictEqn['graphType'] = 'norm'
                self.convert23D(dictEqn['numbers'])
                return True
        elif len(sType) > 1:
            if fFFT and fNorm:
                return False
            else:
                return True
        else:
            dictEqn['graphDem'] = '3D'
            dictEqn['graphType'] = 'norm'
            self.convert23D(dictEqn['numbers'])
            return True
        
    def moveAxis(self, ax, d3d=False):
        if d3d:
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)

        else:
            ax.grid(visible=True)
            ax.spines['left'].set_position('center')
            ax.spines['bottom'].set_position('center')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

    def plotCurrEqn(self, currX, currY, clear=False):
        if (currX, currY) not in self.plotGrid.keys():
            ax = self.defineax(currX, currY)
            if clear:
                ax.clear()            
            self.moveAxis(ax)
            return
        listEqn = self.plotGrid[(currX, currY)]['numbers']
        ax = self.plotGrid[(currX, currY)]['ax']
        if clear:
            ax.clear()
            # ax.cla()
            self.moveAxis(
                ax, self.plotGrid[(currX, currY)]['graphDem'] == '3D')
        # self.moveAxis(ax, self.plotGrid[(currX, currY)]['graphDem']=='3D')
        if listEqn == None or len(listEqn) == 0:
            # строим пустой график с сеткой и сдвигаем оси в центр
            # ax.plot()
            self.moveAxis(ax)
        else:
            if self.checkType(self.plotGrid[(currX, currY)]):
                # if self.plotGrid[(currX, currY)]['graphDem'] == '3D':
                #    self.
                if self.plotGrid[(currX, currY)]['graphType'] == 'fft' or self.plotGrid[(currX, currY)]['graphType'] == 'fft2':
                    for cEqn in listEqn:
                        self.list_eqn[cEqn].plotFFT(ax)
                else:
                    for cEqn in listEqn:
                        self.list_eqn[cEqn].plotPLTGraph(ax)
        # self.fig.show()
        # self.plotGrid[(currX, currY)]['ax'] = ax

    # если включить отображение - true, иначе false
    def changeVisible(self, name, visible):
        number = int(name[7:])  # IconEnN
        if number < len(self.list_eqn) and self.list_eqn[number] != None:
            if visible:
                self.list_eqn[number].show = True
                self.list_eqn[number].plotPLTGraph(self.defineax(
                    self.list_eqn[number].xposition, self.list_eqn[number].yposition))
                self.list_eqn[number].plotFFT(self.defineax(
                    self.list_eqn[number].fftxpos, self.list_eqn[number].fftypos))
            else:
                self.list_eqn[number].show = False
                self.plotCurrEqn(  # перестраиваем окно графика
                    self.list_eqn[number].xposition, self.list_eqn[number].yposition, True)
                if self.list_eqn[number].fftxpos != None and self.list_eqn[number].fftypos != None:
                    self.plotCurrEqn(  # перестраиваем окно графика fft
                        self.list_eqn[number].fftxpos, self.list_eqn[number].fftypos, True)

    def replotGraph(self):
        self.plotGrid = dict()
        maxx, maxy = 0, 0
        for currEqn in range(len(self.list_eqn)):
            if self.list_eqn[currEqn] != None:
                self.defineFFTPos(self.list_eqn[currEqn])
                if self.list_eqn[currEqn].fftxpos != None and self.list_eqn[currEqn].fftypos != None:
                    maxx = max(
                        maxx, self.list_eqn[currEqn].xposition, self.list_eqn[currEqn].fftxpos)
                    maxy = max(
                        maxy, self.list_eqn[currEqn].yposition, self.list_eqn[currEqn].fftypos)
                else:
                    maxx = max(maxx, self.list_eqn[currEqn].xposition)
                    maxy = max(maxy, self.list_eqn[currEqn].yposition)
        self.maxxPos, self.maxyPos = maxx, maxy
        self.fig, self.ax = subplots(
            maxx + 1, maxy + 1)  # , figsize=(1, 1))
        subplots_adjust(top=1, bottom=0, right=1, left=0)
        for currEqn in range(len(self.list_eqn)):
                self.updateDict(currEqn)
                self.list_eqn[currEqn].plotPLTGraph(self.plotGrid[(
                    self.list_eqn[currEqn].xposition, self.list_eqn[currEqn].yposition)]['ax'])
                if self.list_eqn[currEqn].fftxpos != None and self.list_eqn[currEqn].fftypos != None:
                    self.list_eqn[currEqn].plotFFT(self.plotGrid[(
                        self.list_eqn[currEqn].fftxpos, self.list_eqn[currEqn].fftypos)]['ax'])

    def defineFFTPos(self, Eqn):
        if not (Eqn.userDefineFFT):
            if self.fftPlot == 'bottom':
                Eqn.xposition, Eqn.yposition = Eqn.origxpos * 2, Eqn.origypos
                Eqn.fftxpos, Eqn.fftypos = Eqn.xposition + 1, Eqn.yposition
            elif self.fftPlot == 'right':
                Eqn.xposition, Eqn.yposition = Eqn.origxpos, Eqn.origypos * 2
                Eqn.fftxpos, Eqn.fftypos = Eqn.xposition, Eqn.yposition + 1
            elif self.fftPlot == 'top':
                Eqn.fftxpos, Eqn.fftypos = Eqn.origxpos * 2, Eqn.origypos
                Eqn.xposition, Eqn.yposition = Eqn.fftxpos + 1, Eqn.fftypos
            elif self.fftPlot == 'left':
                Eqn.fftxpos, Eqn.fftypos = Eqn.origxpos, Eqn.origypos * 2
                Eqn.xposition, Eqn.yposition = Eqn.xposition, Eqn.yposition + 1
            else:
                Eqn.fftxpos, Eqn.fftypos = None, None
                Eqn.xposition, Eqn.yposition = Eqn.origxpos, Eqn.origypos

    def updateDict(self, eqnNum):
        '''обновляет self.PlotGrid для графика и его fft если нет записи, то добавляет ее'''
        eqn = self.list_eqn[eqnNum]
        xpos, ypos = eqn.xposition, eqn.yposition
        if (xpos, ypos) in self.plotGrid.keys():
            if eqnNum not in self.plotGrid[(xpos, ypos)]['numbers']:
                self.plotGrid[(xpos, ypos)]['numbers'].append(eqnNum)
        else:
            self.plotGrid.update({(xpos, ypos): {
                                 'graphDem': eqn.graphDem, 'graphType': eqn.graphType, 'numbers': [eqnNum], 'ax': self.defineax(xpos, ypos)}})
            self.moveAxis(self.defineax(xpos, ypos),
                          eqn.graphDem == '3D')
        # разбираемся c fft
        # здесь мб ошибка с наложением графиков на fft
        if eqn.fftxpos != None and eqn.fftypos != None:
            if (eqn.fftxpos, eqn.fftypos) in self.plotGrid.keys():
                self.plotGrid[(eqn.fftxpos, eqn.fftypos)
                              ]['numbers'].append(eqnNum)
            else:
                if self.plotGrid[(xpos, ypos)]['graphDem'] == '3D':
                    self.plotGrid.update({(eqn.fftxpos, eqn.fftypos): {
                                         'graphDem': '3D', 'graphType': 'fft2', 'numbers': [eqnNum], 'ax': self.defineax(eqn.fftxpos, eqn.fftypos)}})
                    self.moveAxis(self.defineax(
                        eqn.fftxpos, eqn.fftypos), True)
                else:
                    self.plotGrid.update({(eqn.fftxpos, eqn.fftypos): {
                        'graphDem': '2D', 'graphType': 'fft', 'numbers': [eqnNum], 'ax': self.defineax(eqn.fftxpos, eqn.fftypos)}})
                    self.moveAxis(self.defineax(
                        eqn.fftxpos, eqn.fftypos), False)
                    
    def convertAxes23D(self, ax):
        ax.clear()
        ax.set_axis_off()
        gridSpec = ax.get_subplotspec()
        xpos, ypos = gridSpec.colspan[0], gridSpec.rowspan[0]
        ind = ypos * self.maxxPos + xpos
        if self.maxxPos == 0:
            if self.maxyPos == 0:
                self.ax = self.fig.add_subplot(
                    self.maxxPos + 1, self.maxyPos + 1, ind + 1, projection='3d')
                if (xpos, ypos) in self.plotGrid.keys():
                    self.plotGrid[(xpos, ypos)]['ax'] = self.ax
                return self.ax
            else:
                self.ax[ypos] = self.fig.add_subplot(
                    self.maxxPos + 1, self.maxyPos + 1, ind + 1, projection='3d')
                if (xpos, ypos) in self.plotGrid.keys():
                    self.plotGrid[(xpos, ypos)]['ax'] = self.ax[ypos]
                return self.ax[ypos]
        elif self.maxyPos == 0:
            self.ax[xpos] = self.fig.add_subplot(
                self.maxxPos + 1, self.maxyPos + 1, ind+1, projection='3d')
            if (xpos, ypos) in self.plotGrid.keys():
                self.plotGrid[(xpos, ypos)]['ax'] = self.ax[xpos]
            return self.ax[xpos]
        else:
            self.ax[xpos, ypos] = self.fig.add_subplot(
                self.maxxPos + 1, self.maxyPos + 1, ind + 1, projection='3d')
            if (xpos, ypos) in self.plotGrid.keys():
                self.plotGrid[(xpos, ypos)]['ax'] = self.ax[xpos, ypos]
            return self.ax[xpos, ypos]

    def convert23D(self, numbers):

        for i in numbers:
            eqn = self.list_eqn[i]
            if eqn.graphDem != '3D':  # оптимизируем
    
                if eqn.graphType != 'implicit':
                    eqn.graphDem = '3D'
                    eqn.graphType = 'norm'
                    eqn.plotGraph()
                else:
                    eqn.show = False
                    self.parent.showErrorEqn(
                        eqn.num, 'Невозможно представить неявную функцию в 3х мерном пространстве')

    def removeEqnInPlot(self, num):
        ''' удаляет максимум информации об обекте graph, при его удалении '''
        var = self.list_eqn[num].expressedVar
        xpos, ypos = self.list_eqn[num].xposition, self.list_eqn[num].yposition
        xfftpos, yfftpos = self.list_eqn[num].fftxpos, self.list_eqn[num].fftypos
        for i in self.plotGrid.keys():
            if num in self.plotGrid[i]['numbers']:
                self.plotGrid[i]['numbers'].remove(num)
        if len(self.KnownAxis.keys()) == 0:
            for i in self.KnownAxis.keys():
                if i.name == var.name:
                    if len(self.KnownAxis[i]) < 2:
                        del self.KnownAxis[i]
                    else:
                        self.KnownAxis[i].remove(num)
        self.list_eqn[num] = None
        self.plotCurrEqn(xpos, ypos, True)
        self.plotCurrEqn(xfftpos, yfftpos, True)

    def checkNeedResize(self):
        maxx, maxy = 0, 0
        if len(self.plotGrid.keys()) != 0:
            for i in self.plotGrid.keys():
                if len(self.plotGrid[i]['numbers']) == 0:
                    del self.plotGrid[i]  # чистим мусор
                else:
                    maxx, maxy = max(maxx, i[0]), max(maxy, i[1])
            if maxx != self.maxxPos or maxy != self.maxyPos:
                self.maxxPos, self.maxyPos = maxx, maxy
                self.resizeSubPlot()
        else:
            self.maxxPos, self.maxyPos = 0, 0
            self.resizeSubPlot()

    def checkNewEqn(self, num, fft):
        eqn = self.list_eqn[num]
        if not (fft):
            xpos, ypos = eqn.xposition, eqn.yposition
            if eqn.graphDem == self.plotGrid[(xpos, ypos)]['graphDem']:
                return True
            else:
                if eqn.graphType == 'implicit':
                    self.parent.showErrorEqn(
                        eqn.num, 'Невозможно представить неявную функцию в 3х мерном пространстве')
                    return False
                elif eqn.graphDem == '2D':
                    self.parent.showErrorEqn(
                        eqn.num, 'Невозможно преобразовать 3х мерный график в 2х')
                else:
                    eqn.graphDem = '3D'
                    if self.plotGrid[(xpos, ypos)]['graphDem'] == '2D':
                        self.plotGrid[(xpos, ypos)]['graphDem'] == '3D'
                        self.plotGrid[(xpos, ypos)]['graphType'] == 'norm'
                        self.convert23D(self.plotGrid[(xpos, ypos)]['numbers'])
                        self.plotCurrEqn(xpos, ypos, True)
                        return False
                    else:
                        eqn.graphDem = '3D'
                        return True
        else:
            xpos, ypos = eqn.fftxpos, eqn.fftypos
            if eqn.graphDem == self.plotGrid[(xpos, ypos)]['graphDem']:
                return True
            else:
                if self.plotGrid[(xpos, ypos)]['graphDem'] == '2D':
                    self.plotGrid[(xpos, ypos)]['graphDem'] == '3D'
                    self.plotGrid[(xpos, ypos)]['graphType'] == 'fft2'
                    self.plotCurrEqn(xpos, ypos, True)
                    return False
                else:
                    return True
