import sympy as sp
import re

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
        self.dict_replace = {}
        self.str_sign = ""
        for i in range(len(self.list_sign)):  # скажем, что все знаки экранируются
            if len(self.list_sign[i]) > 1:
                self.list_sign[i] = '\\'.join(self.list_sign[i])
        self.list_func.sort(key=len, reverse=True)
        self.list_Ffunc.sort(key=len, reverse=True)
        self.list_sign.sort(key=len, reverse=True)
        self.mega_regexp = r'(' + "|".join(self.list_Ffunc) + "|" + "|".join(self.list_func) + "|" + "|".join(self.list_const) + "|\\" + \
            "|\\".join(self.list_brace) + "|\\" + \
            "|\\".join(self.list_sign) + '|' + '|'.join(self.list_num) + ')'
        self.strFfunc = r'(' + "|".join(self.list_Ffunc) + ')'
        self.strNum = r'(' + '|'.join(self.list_num) + ')'
        self.dictParam = {
            'color': None,
            'leftPart': '',
            'rightPart': '',
            'xpos': 0,
            'ypos': 0,
            'param': {},
            'axis': [],
            'xlim': (),
            'ylim': (),
            'zlim': (),
            'plotData': None,
            'NeedSubs': False,
            'ListSubs': []
        }
    def parserEqn(self, eqn, number):
        # проверяем скобки
        eqn.lower()
        # list_eqn = eqn.split("=")
        # left_part, right_part = list_eqn[0], list_eqn[2]
        # парсим доп параметры
        list_param = []  # получакм из ввода
        # проверяем необходимость подстановок
        list_var=[]
        operandList=re.split(self.mega_regexp, eqn)
        operandList=filter(None, operandList)
        operandList=list(filter((" ").__ne__, operandList))
        recognizeStr=''
        cntDrwdedBrace=0
        skipIter=False
        lenPart = len(operandList)
        for cO in range(lenPart):
            if skipIter:  # символ уже обработан
                skipIter=False
                continue
            if re.search(self.strNum, operandList[cO]):
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
                    return None
            elif operandList[cO] in self.list_brace:
                if operandList[cO] in '<{[(' and cO != lenPart - 1:
                    recognizeStr += '('
                elif operandList[cO] in '>]})':
                    recognizeStr += ')'
                else:
                    self.parent.parent.showErrorEqn(
                        number, 'Пропущена закрывающая скобка')
                    return None
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
                    return None
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
                # print(operandList[cO])
                operand = operandList[cO].replace(' ', '')
                print(operand == operandList[cO])
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
        return recEqn, list_var
    def parseParam(self, eqn, number):
        dictParamEqn = self.dictParam.copy()
        list_subs = []  # перечень всего, что нужно подставить
        iSum = eqn.find('sum(')  # replace to find_all
        if iSum != -1: 
            SSum = self.checkBraceNext(eqn[iSum + 4:], number)
            lSum = re.split(',|\.|;', SSum)
            eqn = eqn.replace('sum(' + SSum + ')', '+'.join(lSum))
            list_subs.extend(lSum)
            list_subs = list(set(list_subs))  # убираем повторения
            list_subs = filter(None, list_subs)
            list_subs = list(filter((" ").__ne__, list_subs))
        # парсим по частям выражение
        if len(list_subs) > 1:
            dictParamEqn['NeedSubs'] = True,
            dictParamEqn['ListSubs'] = list_subs
        dictParamEqn['leftPart'], dictParamEqn['rightPart'] = eqn.split('=')
        # print(dictParamEqn['leftPart'], dictParamEqn['rightPart'])
        return dictParamEqn
        
        
    def sorWithLen(x, y):
        if len(x) > len(y):
            return True
        return False
    def checkBrace(s):
        pass
    def checkBraceNext(self, s, num):
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
                num, 'Пропещены открывающие скобки х' + str(abs(BraceOpen)))
            return None
        sOut = re.sub(r'\[|\<|\{', '(', sOut)
        sOut = re.sub(r'\]|\>|\}', ')', sOut)
        return sOut
    




