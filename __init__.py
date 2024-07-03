def init():
    import sys
    from PyQt5.QtWidgets import (
        QMainWindow, QApplication, QMenu,
        QLabel, QToolBar, QAction, QStatusBar,
        QVBoxLayout, QFrame, QSplitter, QStyleFactory,
        QGridLayout, QLineEdit, QWidget, QPushButton,
        QScrollArea, QFormLayout, QGroupBox
    )
    from PyQt5.QtGui import QIcon, QPixmap
    from PyQt5.QtCore import Qt, QSize, pyqtSlot
    from PyQt5.QtGui import QKeySequence, QFont
    import sympy as sp
    import re
    # from widgets.py import *
    #from parcer.py import *