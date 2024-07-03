import re
from sympy import symbols, plot, sympify, plot_implicit, Eq
from sympy.plotting.plot import plot3d, PlotGrid
import matplotlib.pyplot as plt
from timeit import timeit
import units
from PyQt5.QtGui import QIcon, QPixmap
import sympy as sp
import numpy as np
# Тестовая строка

test_string = "15.5+2,4sin(145,4x+15) ()}]> sum(y1, y2, y3)"

# Регулярное выражение для поиска функций
# pattern = r'(sin|cos|tg|ctg|i|sinc)'
# pattern1 = r'(sqrt\d+[.,]?\d*|sinc|i|sin|cos|ctg|tg|\d+[.,]\d*|\d+|\[|\]|\(|\)|\<|\>|\+|\-|\*)'
test_string = re.sub(r'\[|\<|\{', '(', test_string)
print(test_string)
pattern1 = '(sqrt\d+|log\d+|arccosec|atan2sh|arcsech|arcsech|arcsin|arccos|arcctg|arcsec|cosec|arctg|arcth|arsch|powln|sinc|csch|arsh|arch|arth|sign|sqrt|root|sin|cos|ctg|sec|cth|sch|abs|exp|tg|ch|th|re|im|lg|i|pi|e|\(|\)|\[|\]|\<|\>|\{|\}|\*\*|\+|\-|\*|\/|\^|\s*|\d+[.,]\d*|\d+)'
# Поиск всех совпадений
# matches = re.split(pattern, test_string)
v = test_string.replace('sum(y1, y2, y3)', 'y1+y2+y3')
print(v)
print(test_string)
matches1 = re.split(pattern1, test_string)
print(matches1)
# print(matches1)
# print(re.split(r'(sqrt\d+|ctg)', ('ctgxsqrt10(x)')))
x, y = symbols('x y')
# print(sympify('cosec(x)*I'))
# print(sympify('cosec(x)*I').subs(x, 1))

matches1 = filter(None, matches1)
matches1 = filter((" ").__ne__, matches1)
# print(matches1)
for k in matches1:
    m = re.match(pattern1, k)
    if m:
        print(m.group(), m.group().isdigit())
    else:
        print(k)

'''
list_func = ['cos', 'tg', 'ctg', 'sec', 'cosec', 'sinc',  # тригономатрические функции
             # обратные тригонометрические функции
             'arcsin', 'arccos', 'arctg', 'arcctg', 'arcsec', 'arccosec',
             'atan2'  # atan2(x, y) = -ilog((x+iy)/sqrt(x**2+y**2))
             'sh', 'ch', 'th', 'cth', 'sch', 'csch',  # гиперболические функции
             # обратные гиперболические функции
             'arsh', 'arch', 'arth', 'arcth', 'arsch', 'arcsech', 'arcsech',
             're', 'im', 'abs', 'sign', 'exp', 'pow'  # некоторые мат. функции
             'i', 'pi', 'e',  # константы
             'ln', 'lg', 'log\d+', 'sqrt', 'root', 'sqrt\d+', 'sin',]
mega_regexp = r'(' + "|".join(list_func) + ')'
# print(timeit(lambda: 'sin' in list_func))
# print(timeit(lambda: re.search(mega_regexp, 'sin')))
#print(timeit(lambda: re.match(mega_regexp, 'sin')))
# print('i' in list_func)
l = [1, 2, 3]
for i in l:
    i = 5
print(l)
'''
'''
fig, ax = plt.subplots(nrows=2, ncols=2)
x, y = symbols('x y')
z = xlim=(-5, 5)
# Создание нескольких графиков с помощью sympy.plot
p1 = plot(x, xlim=(), show=False)  # График x
bc1 = p1.backend(p1)
bc1.ax = ax
bc1._process_series(bc1.parent._series, ax, bc1.parent)
p2 = plot(x**2, z, (x, -5, 5), show=False)  # График x^2
bc2 = p2.backend(p2)
p3 = plot3d(x * y, (x, -5, 5), (y, -5, 5), show=False)  # График 3D x*y
bc3 = p3.backend(p3)
p4 = plot(x**3, show=False)
bc4 = p4.backend(p4)

# Использование PlotGrid для объединения графиков в один фигурный объект
# l = [p1, p2, p3, p4]
# grid = PlotGrid(2, 2, *l)

vertices = bc1.patches[0].get_path().vertices
ax[0,0].plot(vertices[:, 0], vertices[:, 1], ls=':', color='gold', lw=10, alpha=0.5, zorder=0)

# ax[0, 0].
'''
'''
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sympy as sp

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Создание главного окна
        self.setWindowTitle("Sympy Plot in PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Создание виджета для отображения графика
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Создание фигуры и холста для графика
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Создание графика с использованием sympy
        x = sp.symbols('x')
        y = sp.sin(x)
        ax = fig.add_subplot(111)
        ax.plot(x, y)

        # Установка виджета в качестве центрального виджета главного окна
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())'''
'''
import matplotlib.pyplot as plt
from sympy.abc import x
import sympy as sp
# Определение функций
f_sin = sp.sin(x)
f_cos = sp.cos(x)

# Создание графиков sympy
p_sin = sp.plot(f_sin, (x, -10, 10), show=False)
p_cos = sp.plot(f_cos, (x, -10, 10), show=False)
psin = p_sin.backend(p_sin)
psin = psin.process_series()

# Извлечение данных из графиков sympy для использования в matplotlib


# Построение графиков с использованием matplotlib
plt.figure(figsize=(12, 6))
print(psin)
plt.plot(psin)
plt.plot(x_data, y_data_cos, label="cos(x)")

# Настройка графика
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Графики синуса и косинуса")
plt.legend()
plt.grid(True)
plt.show()
'''
'''
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import sympy as sp
from sympy.abc import x, y, z
import ctypes
def move_sympyplot_to_axes(p, ax):
    backend = p.backend(p)
    backend.ax = ax
    backend._process_series(backend.parent._series, ax, backend.parent)
    backend.ax.grid(True)
    #backend.ax.spines['right'].set_color('none')
    # backend.ax.spines['top'].set_color('none')
    #backend.ax.spines['bottom'].set_position('zero')
    plt.close(backend.fig)

def z(x, y):
    return (x ** 2 + y ** 2 - 1) ** 3 - x ** 2 * y ** 3

p1 = sp.plot_implicit(z(x, y), (x, -1.5, 1.5), (y, -1.5, 1.5), show=False)

fig, ax = plt.subplots()

move_sympyplot_to_axes(p1, ax)
# ax.patches[0].set_label("my label")
handles = [Line2D([], [], color=ax.patches[0].get_facecolor())]
ax.legend(handles=handles, labels=["my label"], loc='upper left')

vertices = ax.patches[0].get_path().vertices
ax.plot(vertices[:, 0], vertices[:, 1], ls=':', color='gold', lw=10, alpha=0.5, zorder=0)

# plt.gca().set_axis_on()

plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)
#plt.gca().xaxis.set_major_locator(plt.NullLocator())
# plt.gca().yaxis.set_major_locator(plt.NullLocator())
# plt.savefig("filename.pdf", bbox_inches='tight', pad_inches=0)
plt.grid()
plt.show()
'''
'''
def move_sympyplot_to_axes(p, ax):
    backend = p.backend(p)
    backend.ax = ax
    backend._process_series(backend.parent._series, ax, backend.parent)
    # backend.ax.spines['right'].set_color('none')
    # backend.ax.spines['top'].set_color('black')
    # backend.ax.spines['bottom'].set_position('zero')
    plt.close(backend.fig)

x, y = symbols('x y')
z = xlim=(-5, 5)
# Создание нескольких графиков с помощью sympy.plot
p1 = plot_implicit(Eq(x + 1, y**2 + x), facecolor='blue',
                   show=False)  # График x
p1[0].line_color = 'red'

xx1, yy1 = p1[0].get_points()
p2 = plot3d(x**2, (x, -5, 5), show=False)  # График x^2
# p2.append(p1[0])
xx2, yy2, zz2 = p2[0].get_meshes()
p3 = plot3d(x * y, (x, -5, 5), (y, -5, 5), show=False)  # График 3D x*y
xx3, yy3, zz3 = p3[0].get_meshes()
p4 = plot(x**3, show=False)
xx4, yy4 = p4[0].get_data()

fig, ax = plt.subplots(2, 2)
#sp1 = fig.add_subplot(121)
# sp2 = fig.add_subplot(122)
move_sympyplot_to_axes(p1, ax[0, 0])
ax[0, 0].grid()
ax[0, 0].spines['left'].set_position('center')
ax[0, 0].spines['bottom'].set_position('center')
ax[0, 0].spines['top'].set_visible(False)
ax[0, 0].spines['right'].set_visible(False)
ax[1, 0] = fig.add_subplot(222, projection='3d')
ax[1, 0].plot_wireframe(xx2, yy2, zz2, rstride=10, cstride=10)

# ax[0, 1].plot(xx1, yy1)
# ax[1, 0].spines['left'].set_position('center')
#ax[1, 0].spines['bottom'].set_position('center')
# ax[1, 0].spines['top'].set_visible(False)
# ax[1, 0].spines['right'].set_visible(False)
ax[1, 1].set_axis_off()
ax[1, 1] = fig.add_subplot(223, projection='3d')
ax[1, 1].plot_surface(xx3, yy3, zz3, cmap=None)
def f(ax, x, y):
    ax.plot(x, y)
# ax[3, 0] = f(ax[3, 0], xx4, yy4)
fft_result = np.fft.fft2([xx2, yy2])
magnitude_spectrum = np.abs(fft_result)
# , hspace=0, wspace=0)
ax[0, 1].plot_surface(*magnitude_spectrum)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0)
# plt.gca().set_axis_on()
# plt.margins(0, 0)
# ax[1, 0].autoscale_view('tight')
# plt.tight_layout()


fig.show()
p1.show()  # yt трогать, иначе окно закрывается
'''
'''
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random

# main window
# which inherits QDialog
class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to 'plot' method
        self.button = QPushButton('Plot')

        # adding action to the button
        self.button.clicked.connect(self.plot)

        # creating a Vertical Box layout
        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # adding canvas to the layout
        layout.addWidget(self.canvas)

        # adding push button to the layout
        layout.addWidget(self.button)

        # setting layout to the main window
        self.setLayout(layout)

    # action called by the push button
    def plot(self):

        # random data
        data = [random.random() for i in range(10)]

        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

# driver code
if __name__ == '__main__':

    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())
    '''
'''
import numpy as np
import matplotlib.pyplot as plt
from sympy import plot, Symbol, sin
# Генерация сигнала
t = Symbol('t')
s = sin(t)
p1 = plot(s, adaptive=True, show=False)
s, t = p1[0].get_data()

sampling_rate = 100  # Частота дискретизации
sampling_interval = 1.0 / sampling_rate
t = np.arange(0, 5, sampling_interval)
freq = 1
x = 3 * np.sin(2 * np.pi * freq * t) + np.sin(2 * np.pi *
               4 * t) + 0.5 * np.sin(2 * np.pi * 7 * t)

import numpy as np
# Вычисление FFT
X = np.fft.fft(s)

# Сдвиг FFT в центр
# Xs = X[len(X) // 2:]
X_shifted = np.fft.fftshift(X)


# Нормирование спектра
X_normalized = X_shifted / np.sum(np.abs(X_shifted))

# Построение графика FFT после сдвига и нормирования
plt.figure(figsize=(12, 6))
plt.subplot(211)
plt.stem(np.abs(X_normalized), 'b', markerfmt=" ", basefmt="-b")

plt.xlabel('Frequency (Hz)')
plt.ylabel('Normalized FFT Amplitude |X(freq)|')
plt.title('Normalized FFT Spectrum After Shift')
plt.grid(True)

# Построение графика восстановленного сигнала

reconstructed_signal = np.fft.ifft(X_normalized)
plt.subplot(132)
plt.plot(t, reconstructed_signal, 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Init Signal')
plt.grid(True)

plt.subplot(133)
plt.plot(t, x, 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Init Signal')
plt.grid(True)

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
# t = np.arange(256)
x = 3 * np.sin(2 * np.pi * freq * t) + np.sin(2 * np.pi *
               4 * t) + 0.5 * np.sin(2 * np.pi * 7 * t)
sp = np.fft.fft(x)
freq = np.fft.fftfreq(t.shape[-1])
plt.subplot(212)
plt.plot(freq, sp.real, freq, sp.imag)
plt.show()
'''
'''from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGroupBox

app = QApplication([])

main_window = QWidget()
layout = QVBoxLayout(main_window)

group_boxes = []

for i in range(5):
    group_box = QGroupBox(f"Group Box {i}")
    layout.addWidget(group_box)
    group_boxes.append(group_box)

    content = QWidget()
    layout_for_content = QVBoxLayout(content)
    layout_for_content.addWidget(QPushButton(f"Content Button {i}"))
    group_box.setLayout(layout_for_content)

    # Добавление кнопки для управления видимостью группы
    toggle_button = QPushButton(f"Toggle Group {i}")
    toggle_button.clicked.connect(lambda _, index=i: group_boxes[index].setHidden(not group_boxes[index].isHidden()))
    layout.addWidget(toggle_button)

main_window.show()
app.exec_()
'''
'''
def m(ax):
    return ax
fig, ax = plt.subplots()
myax = m(ax)
myax.plot([1, 2, 3], [2, 3, 4])
myax.plot([2, 3, 4], [1, 2, 3])
fig.show()
x = symbols('x')
p = plot(sp.sin(x))
'''
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton('Toggle', self)
        self.button.setGeometry(100, 100, 100, 40)
        self.button.setCheckable(True)
        self.button.clicked.connect(self.toggle_state)

        self.setWindowTitle('Toggle Button Example')

    def toggle_state(self):
        if self.button.isChecked():
            self.button.setStyleSheet("background-color: green;")
        else:
            self.button.setStyleSheet("background-color: red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())'''