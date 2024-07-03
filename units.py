import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def getTempFileName(templateName):
    fileName = ""
    tempFile = QTemporaryFile(QFileInfo(QDir.temp(), QFileInfo(templateName).baseName()).filePath())
    if tempFile.open():
        fileName = tempFile.fileName() + "." + QFileInfo(templateName).completeSuffix()
        tempFile.close()
    return fileName