# This Python file uses the following encoding: utf-8
import sys
import os
from mic import handlers as han

from PySide2.QtWidgets import QApplication, QWidget, QSlider, QPlainTextEdit
from PySide2.QtWidgets import QRadioButton, QButtonGroup, QComboBox, QLabel
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize
from PySide2 import QtCore
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

import ctypes

myappid = 'bokus-filter' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class micGui(QWidget):
    app_icon = QIcon()
    app = QApplication([])
    handlers = han.Handlers(50)
    changesAvailable = True
    handleUpdated = -1
    sliders = []

    # True if some handler has changed
    def checkHandlersStatus(self):
        if (self.changesAvailable):
            self.changesAvailable = False
            return True
        return False

    def __init__(self, numberOfHandles = 10):
        super(micGui, self).__init__()
        self.setupGui(numberOfHandles)
        
    def setupGui(self, numberOfHandles):
        self.configWindow()
        self.configureBackground()
        self.filterModeButtons()
        self.resolutionOptions()
        self.samplingRateOptions()
        for i in range(numberOfHandles):
            self.sliders.append(self.createImgSlider("./mic/gui/filter-gui/slider.png", i))
            self.sliders[i].valueChanged[int].connect(lambda val, index = i: self.setHandlers(val, index))
            self.handlers.register_callback(self.updateHandlersStatus)

    def updateHandlersStatus(self, handleNumber):
        self.changesAvailable = True
        self.handleUpdated = handleNumber

    def setHandlers(self, newVal, handlerID):
        val = [handlerID, newVal]
        print(self.handlers.value)
        self.handlers.value = val

    def resolutionOptions(self):
        resolutions = ["Ultra High", "High", "Normal", "Low", "Ultra Low"]
        self.setComboBox(2, 550, 155, "comboBox", resolutions)

    def samplingRateOptions(self):
        rates = ["48000", "44100", "32000", "22050", "11025", "8000"]
        self.setComboBox(3, 550, 204, "comboBox_2", rates)

    def configureBackground(self):
        image = "mic/gui/filter-gui/UI.jpg"

        self.text_field = QPlainTextEdit(self)
        self.text_field.setDisabled(True)
        self.text_field.setMinimumSize(720, 301)
        self.text_field.setStyleSheet(  "background-image: url(" + 
                                        image + 
                                        "); background-attachment: fixed"
                                    )

    def setComboBox(self, 
                    startingIndex = 0, 
                    xPos = 0, yPos = 0, 
                    objName = "default",
                    items = []):
        self.comboBox = QComboBox(self)
        for item in items:
            self.comboBox.addItem(item)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(xPos, yPos, 125, 22))
        self.comboBox.setCurrentIndex(startingIndex)

    def configIcons(self):
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon16.png', QSize(16,16))
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon24.png', QSize(24,24))
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon32.png', QSize(32,32))
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon48.png', QSize(48,48))
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon256.png', QSize(256,256))
        self.app.setWindowIcon(self.app_icon)

    def configWindow(self):
        self.configIcons()
        self.setWindowTitle('Bokus Multiband Filter')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setFixedSize(720, 301)

    def createImgSlider(self, imgPath, index):
        xPosition = 35 + 47 * index
        slider = QSlider(self)
        slider.setObjectName(u"slider" + str(index))
        slider.setGeometry(QRect(xPosition, 49, 41, 191))
        slider.setCursor(QCursor(Qt.OpenHandCursor))
        slider.setMouseTracking(False)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setAcceptDrops(False)
        slider.setAutoFillBackground(False)
        slider.setStyleSheet(    u"QSlider::handle:vertical {\n"
                                                "	image: url(" + imgPath + ");\n"
                                                "	width: 50px;\n"
                                                "	height: 13px\n"
                                                "}\n"
                                                "\n"
                                                "QSlider::groove:vertical{\n"
                                                "	background: rgba(0, 0, 0, 0);\n"
                                                "}"  )
        slider.setValue(50)
        slider.setSliderPosition(50)
        slider.setOrientation(Qt.Vertical)
        slider.setInvertedAppearance(False)
        return slider


    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "./gui/filter-gui/form2.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def filterModeButtons(self):
        self.filterTypeButtons = QButtonGroup(self)
        self.configFilterTypeButtons("firButton", True, 560, 49, 0)
        self.configFilterTypeButtons("iirButton", False, 560, 68, 1)
        self.configFilterTypeButtons("devilButton", False, 560, 86, 2)
        self.configFilterTypeButtons("goblinButton", False, 560, 104, 3)

    def configFilterTypeButtons(self, 
                                name = u"default", 
                                checked = False, 
                                xPos = 0, yPos = 0, 
                                idButton = 0):
        self.button = QRadioButton(self)
        self.button.setObjectName(name)
        self.button.setEnabled(True)
        self.button.setGeometry(QRect(xPos, yPos, 82, 17))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setChecked(checked)
        self.filterTypeButtons.addButton(self.button, idButton)

    def sys_exit(self, exitProgram):
        self.app.exec_()
        exitProgram.value = True
        sys.exit()

def runUserGUI(exitProgram):
    widget = micGui()
    widget.show()
    widget.sys_exit(exitProgram)
