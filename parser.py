import sympy as sp
import re
from matplotlib.colors import to_rgba
import matplotlib.pyplot as plt

class parser:
    def __init__(self, parent):
        self.initConstList()
        self.parent = parent

    def initConstList(self):  # возможно, потом убрать в конфиги
        # определяем известные функции и символы
        self.list_func = ['sin', 'cos', 'tg', 'ctg', 'sec', 'cosec', 'sinc',  # тригономатрические функции
                     # обратные тригонометрические функции
                     'arcsin', 'arccos', 'arctg', 'arcctg', 'arcsec', 'arccosec',
                     'atan2'  # atan2(x, y) = -ilog((x+iy)/sqrt(x**2+y**2))
                     'sh', 'ch', 'th', 'cth', 'sch', 'csch',  # гиперболические функции
                     # обратные гиперболические функции
                     'arsh', 'arch', 'arth', 'arcth', 'arsch', 'arcsech', 'arcsech',
                     're', 'im', 'abs', 'sign', 'exp', 'pow'  # некоторые мат. функции
                     'ln', 'lg', 'sqrt', 'root']
        # функции-спонсоры выгорания программиста
        self.list_Ffunc = ['log\d+', 'sqrt\d+']
        self.list_num = ['\d+[.,]\d*', '\d+']
        self.list_const = ['i', 'pi', 'e']  # константы
        self.list_sign = ['+', '-', '*', '/', '**', '^']  # знаки
        self.list_brace = ['(', ')', '[', ']', '<', '>', '{', '}']  # скобки
        self.dict_replace = {'i': 'I'}
        self.str_sign = ""
        for i in range(len(self.list_sign)):  # скажем, что все знаки экранируются
            if len(self.list_sign[i]) > 1:
                self.list_sign[i] = '\\'.join(self.list_sign[i])
        self.list_func.sort(key=len, reverse=True)
        self.list_Ffunc.sort(key=len, reverse=True)
        self.list_sign.sort(key=len, reverse=True)
        self.mega_regexp = r'(' + "|".join(self.list_Ffunc) + "|" + "|".join(self.list_func) + "|" + "|".join(self.list_const) + "|\\" + \
            "|\\".join(self.list_brace) + "|\\" + \
            "|\\".join(self.list_sign) + ')'
        self.twice_reg = '([A-Za-z_]+[0-9]*[A-Za-z_]*|\d+[.,]\d*|\d+|.*)'
        self.strFfunc = r'(' + "|".join(self.list_Ffunc) + ')'
        self.strNum = r'(' + '|'.join(self.list_num) + ')'
    def parserEqn(self, graph, part):
        # проверяем скобки
        number = graph.num
        if part == 'left':
            eqn = graph.leftPart
        else:
            eqn = graph.rightPart
        # eqn.lower()
        # парсим доп параметры
        list_param = []  # получакм из ввода
        # проверяем необходимость подстановок
        list_var=[]
        splitList = re.split(self.mega_regexp, eqn)
        operandList = []
        for i in splitList:
            operandList.extend(re.split(self.twice_reg, i))
        operandList = filter(None, operandList)
        operandList=list(filter((" ").__ne__, operandList))
        recognizeStr=''
        cntDrwdedBrace=0
        skipIter=False
        lenPart = len(operandList)
        for cO in range(lenPart):
            if skipIter:  # символ уже обработан
                skipIter=False
                continue
            if self.isNum(operandList[cO]):
                if cO != lenPart - 1 and (operandList[cO + 1] not in ')]}>' and operandList[cO + 1] not in self.list_sign):
                    recognizeStr += operandList[cO].replace(',', '.') + '*'
                else:
                    recognizeStr += operandList[cO].replace(',', '.')
            elif operandList[cO] in self.list_func:
                if cO != lenPart - 1:
                    if operandList[cO + 1] in self.list_brace:
                        skipIter = True
                    else:
                        cntDrwdedBrace += 1
                    recognizeStr += operandList[cO] + '('
                else:
                    self.parent.parent.showErrorEqn(
                        number, 'У функции ' + str(operandList[cO]) + ' нет аргументов')
                    return 
            elif operandList[cO] in self.list_brace:
                if operandList[cO] in '<{[(' and cO != lenPart - 1:
                    recognizeStr += '('
                elif operandList[cO] in '>]})':
                    recognizeStr += ')'
                else:
                    self.parent.parent.showErrorEqn(
                        number, 'Пропущена закрывающая скобка')
                    return
            elif operandList[cO] in self.list_const:
                if cO != lenPart - 1 and (operandList[cO + 1] not in ')]}>' and operandList[cO + 1] not in self.list_sign):
                    recognizeStr += operandList[cO] + '*'
                else:
                    recognizeStr += operandList[cO]
            elif operandList[cO] in self.list_sign:
                if cO != lenPart - 1 and operandList[cO + 1] not in self.list_sign:
                    recognizeStr += operandList[cO]
                else:
                    self.parent.parent.showErrorEqn(
                        number, 'Пропущено выражение после оператора '+str(operandList[cO]))
                    return
            elif re.search(self.strFfunc, operandList[cO]):  # дописать потом
                pass
            elif operandList[cO] in list_param:
                if (operandList[cO + 1] not in ')]}>' and operandList[cO + 1] not in list_sign):
                    if cO != lenPart - 1:
                        recognizeStr += operandList[cO] + '*'
                    elif cntDrwdedBrace > 0:
                        recognizeStr += operandList[cO] + ')'
                        cntDrwdedBrace -= 1
                        if cO != lenPart - 2 and operandList[cO + 1] not in self.list_sign:
                            recognizeStr += '*'                        
                    else:
                        recognizeStr += operandList[cO]
                else:
                    recognizeStr += operandList[cO]
            else:
                operand = operandList[cO].replace(' ', '')
                if operand not in list_var:
                    list_var.append(operand)
                if cO != lenPart - 1 and operandList[cO + 1] not in ')]}>' and cntDrwdedBrace > 0:
                    recognizeStr += operandList[cO] + ')'
                    cntDrwdedBrace -= 1
                    if cO != lenPart - 2 and operandList[cO + 1] not in self.list_sign:
                        recognizeStr += '*'
                else:
                    recognizeStr += operandList[cO]
        recognizeStr += ')' * cntDrwdedBrace  # закрываем все скобки
        recEqn = sp.sympify(recognizeStr)
        print(recEqn)
        if part == 'right':
            graph.recognizeFuncRight = recEqn
            # graph.recognizeVarRight = list_eqn
            graph.recognizeVarRight = list_var
        else:
            graph.recognizeFuncLeft = recEqn
            # graph.recognizeVarLeft = list_eqn
            graph.recognizeVarLeft = list_var
        # return recEqn, list_var
    def parseParam(self, graph, eqn):
        # dictParamEqn = self.dictParam.copy()
        eqn.lower()
        list_subs = []  # перечень всего, что нужно подставить
        leqn = len(eqn)    
        # находим все индексы доп параметров
        icolor = eqn.find('color=')
        ixlim = eqn.find('xlim')
        iylim = eqn.find('ylim')
        izlim = eqn.find('zlim=')
        istride = eqn.find('stride')
        ipos = eqn.find('graphpos')
        ifftpos = eqn.find('spectrumpos')
        fftOn = eqn.find('specon')
        fftOff = eqn.find('specoff')
        iGDem = eqn.find('gdem=')
        iGType = eqn.find('type=')
        iparam = eqn.find('param')
        isubs= eqn.find('subs')
        #ixaxName = eqn.find('xaxisname')
        # iyaxName = eqn.find('yaxisname')
        #izaxName = eqn.find('zaxisname')
        # iaxName = eqn.find('axisname')
        iSum = eqn.find('sum(')  # replace to find_all
        # обработка
        imin = len(eqn) 
        if icolor != -1:
            if eqn.find('color', icolor + 1) == -1:
                imin = min(imin, icolor)
                itmp = icolor + len('color=')
                if itmp < leqn:
                    if eqn[itmp] == '#':
                        if leqn - 7 >= itmp:
                            colorstr = eqn[itmp:itmp + 7]
                        else:
                            self.parent.parent.showErrorEqn(
                                graph.num, 'Неверный аргумент параметра color')
                            return
                    elif eqn[itmp] == '(':
                        tmp = self.checkBraceNext(
                            eqn[itmp + 1:], graph.num).replace(',', '.').split(';')
                        colorstr = tuple(float(x) / 255 for x in tmp)
                    else:
                        colorstr = self.extractWord(eqn[itmp:])
                    '''
                    elif eqn[itmp].isalpha():
                    else:
                        self.parent.parent.showErrorEqn(
                            graph.num, 'Неверный аргумент параметра color')
                        return
                    '''
                    # проверка цвета
                    if colorstr in plt.colormaps():
                        graph.color == colorstr
                    else:
                        try:
                            rgba_color = to_rgba(colorstr)
                            graph.color = rgba_color
                        except:
                            self.parent.parent.showErrorEqn(
                                graph.num, 'Неверный аргумент параметра color')
                            return
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр color был переопределен')
                return
        '''
        if ixlim != -1:
            if eqn.find('xlim', ixlim + 2) == -1:
                if leqn >= 5 + ixlim:
                    imin = min(imin, ixlim)
                    tmp = self.checkBraceNext(
                        eqn[ixlim + 5:], graph.num).replace(',', '.').split(';')
                    try:
                        graph.xlim = tuple(map(float, tmp))
                    except:
                        self.parent.parent.showErrorEqn(
                            graph.num, 'Неверный аргумент параметра xlim')
                        return                         
                else:
                    self.parent.parent.showErrorEqn(
                        graph.num, 'Неверный аргумент параметра xlim')
                    return                    
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр xlim был переопределен')
                return
        if iylim != -1:
            if eqn.find('ylim', iylim + 2) == -1:
                if leqn >= 5 + iylim:
                    imin = min(imin, iylim)
                    tmp = self.checkBraceNext(
                        eqn[iylim + 5:], graph.num).replace(',', '.').split(';')
                    try:
                        graph.ylim = tuple(map(float, tmp))
                    except:
                        self.parent.parent.showErrorEqn(
                            graph.num, 'Неверный аргумент параметра ylim')
                        return                         
                else:
                    self.parent.parent.showErrorEqn(
                        graph.num, 'Неверный аргумент параметра ylim')
                    return                    
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр ylim был переопределен')
                return
        if izlim != -1:
            if eqn.find('zlim', izlim + 2) == -1:
                if leqn >= 5 + izlim:
                    imin = min(imin, izlim)
                    tmp = self.checkBraceNext(
                        eqn[izlim + 5:], graph.num).replace(',', '.').split(';')
                    try:
                        graph.zlim = tuple(map(float, tmp))
                    except:
                        self.parent.parent.showErrorEqn(
                            graph.num, 'Неверный аргумент параметра zlim')
                        return                         
                else:
                    self.parent.parent.showErrorEqn(
                        graph.num, 'Неверный аргумент параметра zlim')
                    return                    
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр zlim был переопределен')
                return
            '''
        if istride!= -1:
            if eqn.find('stride', istride + 2) == -1:
                if leqn >= 7 + istride:
                    imin = min(imin, istride)
                    tmp = self.checkBraceNext(eqn[istride+ 7:], graph.num)
                    tmp = tmp.replace(',', '.').split(';')
                    try:
                        graph.stride = tuple(map(float, tmp))
                    except:
                        self.parent.parent.showErrorEqn(
                            graph.num, 'Неверный аргумент параметра stride')
                        return
                else:
                    self.parent.parent.showErrorEqn(
                        graph.num, 'Неверный аргумент параметра stride')
                    return                    
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр stride был переопределен')
                return                
        if ipos != -1:
            if eqn.find('graphpos', ipos + 2):
                if leqn >= 8 + ipos:
                    imin = min(imin, ipos)
                    tmp = self.checkBraceNext(eqn[ipos + 9:], graph.num)
                    tmp = tmp.replace(',', '.').split(';')
                    try:
                        graph.origypos, graph.origxpos = int(
                            tmp[0]) - 1, int(tmp[1]) - 1
                    except:
                        self.parent.parent.showErrorEqn(
                            graph.num, 'Неверный аргумент параметра graphpos')
                        return
                else:
                    self.parent.parent.showErrorEqn(
                        graph.num, 'Неверный аргумент параметра graphpos')
                    return                    
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр graphpos был переопределен')
                return

        if ifftpos != -1:
            if eqn.find('spectrumpos', ifftpos + 2) == -1:
                if leqn >= 11 + ifftpos:
                    imin = min(imin, ifftpos)
                    tmp = self.checkBraceNext(eqn[ifftpos + 12:], graph.num)
                    tmp = tmp.replace(',', '.').split(';')
                    try:
                        graph.fftypos, graph.fftxpos = int(
                            tmp[0]) - 1, int(tmp[1]) - 1
                        graph.userDefineFFT = True
                    except:
                        self.parent.parent.showErrorEqn(
                            graph.num, 'Неверный аргумент параметра spectrumpos')
                        return
                else:
                    self.parent.parent.showErrorEqn(
                        graph.num, 'Неверный аргумент параметра spectrumpos')
                    return                    
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр spectrumpos был переопределен')
                return
        # пока не ясна идея
        if fftOn != -1:
            if fftOff == -1:
                imin = min(imin, fftOff)
                graph.fftshow = True
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Нельзя использовать specon и specoff одновременно')
                return
        if fftOff != -1:
            if fftOn == -1:
                imin = min(imin, fftOn)
                graph.fftshow = False
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Нельзя использовать specon и specoff одновременно')
                return
        if iGDem != -1:
            if eqn.find('gdem', iGDem + 2) == -1:
                if leqn >= 6 + iGDem:
                    imin = min(imin, iGDem)
                    tmp = self.extractWord(eqn[iGDem + 6:])
                    try:
                        tmp = int(tmp)
                        if tmp == 2:
                            graph.graphDem = '2D'
                        elif tmp == 3:
                            graph.graphDem == '3D'
                        else:
                            self.parent.parent.showErrorEqn(
                                graph.num, 'Аргумент параметра gdem должен быть целым числом от 2 до 3')
                            return
                    except:
                        self.parent.parent.showErrorEqn(
                            graph.num, 'Неверный аргумент параметра gdem')
                        return
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр gdem был переопределен')
                return
        if iGType != -1:
            if eqn.find('type', iGType + 2) == -1:
                if leqn >= 6 + iGtype:
                    imin = min(imin, iGType)
                    tmp = self.extractWord(eqn[iGType + 6:])
                    if graph.graphDem == '2D' and tmp in graph.parent.listType2d:
                            graph.graphDem = tmp
                    elif graph.graphDem == '2D' and tmp in graph.parent.listType3d:
                        # перерисовываем в 3d
                        graph.graphDem = '3D'
                        graph.graphType = tmp
                    elif graph.graphDem == '3D' and tmp in graph.parent.listType3d:
                        graph.graphType = tmp
                    else:
                            self.parent.parent.showErrorEqn(
                                graph.num, 'Неверный аргумент параметра type')
                            return
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр type был переопределен')
                return
        if iparam != -1:
            if eqn.find('param', iparam + 2) == -1:
                if leqn >= 6 + iparam:
                    imin = min(imin, iparam)
                    tmp = self.checkBraceNext(eqn[iparam + 5:], graph.num)
                    tmp = re.split(',|.|;', tmp)
                    # надо это как-то валидировать
                    for x in tmp:
                        graph.parametric.update({x: 1})  # базовое значение
                else:
                    self.parent.parent.showErrorEqn(
                        graph.num, 'Неверный аргумент параметра param')
                    return                    
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр param был переопределен')
                return
        if isubs != -1:
            if eqn.find('subs', isubs + 2) == -1:
                if leqn >= 5 + isubs:
                    imin = min(imin, isubs)
                    tmp = self.checkBraceNext(eqn[isubs + 5:], graph.num)
                    tmp = re.split(',|\.|;', tmp)
                    tmp = list(x.strip() for x in tmp)
                    # надо это как-то валидировать
                    graph.NeedSubs = True
                    graph.ListSubs = tmp
                else:
                    self.parent.parent.showErrorEqn(
                        graph.num, 'Неверный аргумент параметра subs')
                    return                  
            else:
                self.parent.parent.showErrorEqn(
                    graph.num, 'Параметр subs был переопределен')
                return
        eqn = eqn[:imin]
        eqn = eqn.strip()
        # убираем лишний разделитель
        if eqn[-1] in ';,.':
            eqn = eqn[:-2]
        # проверка на дурака
        if eqn.count('=') > 1:
            self.parent.parent.showErrorEqn(
                graph.num, 'В уравнении может быть только одно =')
            return
        elif eqn.count('=') == 0:
            self.parent.parent.showErrorEqn(
                graph.num, 'В уравнении должно быть =')
            return            
        if iSum != -1:
            SSum=self.checkBraceNext(eqn[iSum + 4:], number)
            lSum=re.split(',|\.|;', SSum)
            eqn=eqn.replace('sum(' + SSum + ')', '+'.join(lSum))
            list_subs.extend(lSum)
            list_subs=list(set(list_subs))  # убираем повторения
            list_subs=filter(None, list_subs)
            list_subs=list(filter((" ").__ne__, list_subs))
        if len(list_subs) > 1:
            graph.NeedSubs = True,
            graph.ListSubs = list_subs
            # парсим по частям выражение
        graph.leftPart, graph.rightPart = eqn.split('=')
        if graph.leftPart == '' or graph.rightPart == '':
            self.parent.parent.showErrorEqn(
                graph.num, 'Одна из частей уравнеия пустая')
            return              

    def sorWithLen(x, y):
        if len(x) > len(y):
            return True
        return False
    def checkBrace(s):
        pass
    def checkBraceNext(self, s, num):
        '''
        извлекает выражение из скобок, подавать без первой скобки, результат не имеет внешних скобок
        '''
        BraceOpen = 1
        sOut = ''
        for i in s:
            if i in '[{<(':
                BraceOpen += 1
            elif i in ']}>)':
                BraceOpen -= 1
            if BraceOpen != 0:
                sOut += i
            else:
                break
        if BraceOpen > 0:
            sOut += ')' * (BraceOpen - 1)
        elif BraceOpen < 0:
            self.parent.parent.showErrorEqn(
                num, 'Пропущены открывающие скобки х' + str(abs(BraceOpen)))
            return None
        sOut = re.sub(r'\[|\<|\{', '(', sOut)
        sOut = re.sub(r'\]|\>|\}', ')', sOut)
        return sOut
    def extractWord(self, s):
        itmp = 0
        sumstr = ''
        s = s.strip()
        while itmp < len(s) and s[itmp] not in ' ,.':  # s[itmp] != ' ':
            sumstr += s[itmp]
            itmp += 1
        return sumstr
    def isNum(self, eqn):
        eqn = eqn.replace(',', '.')
        try:
            t = float(eqn)
            return True
        except:
            return False




