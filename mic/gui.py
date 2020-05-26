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
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, SLOT, SIGNAL)
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
    changed = -1 #0: handle, #1: type, #2: resolution, #3: rate
    handleUpdated = -1
    sliders = []
    comboBoxResol = 0
    comboBoxRate = 0
    resolIndex = -1
    rateIndex = -1
    filterIndex = -1

    def __init__(self, numberOfHandles = 10):
        super(micGui, self).__init__()
        self.setupGui(numberOfHandles)

    # True if some option has changed
    def hasUpdates(self):
        return self.changesAvailable

    def updateIndex(self):
        return self.changed

    def getRate(self):
        return self.comboBoxRate.currentIndex()

    def getResolution(self):
        return self.comboBoxResol.currentIndex()

    def getFilterType(self):
        return self.filterIndex

    def getHandleNumber(self):
        return self.handleUpdated

    def getHandleValue(self):
        return self.handlers.value[self.handleUpdated]
     
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
        self.changed = 0

    def setHandlers(self, newVal, handlerID):
        val = [handlerID, newVal]
        print(self.handlers.value)
        self.handlers.value = val

    def resolutionOptions(self):
        resolutions = ["Ultra High", "High", "Normal", "Low", "Ultra Low"]
        self.comboBoxResol = self.setComboBox(2, 550, 155, "comboBoxResol", resolutions)
        l = lambda optionSelected, optionIndex = 2: self.updateComboBoxStatus(optionSelected, optionIndex)
        self.comboBoxResol.currentIndexChanged[int].connect(l)

    def samplingRateOptions(self):
        rates = ["48000", "44100", "32000", "22050", "11025", "8000"]
        self.comboBoxRate = self.setComboBox(3, 550, 204, "comboBoxRate", rates)
        l = lambda optionSelected, optionIndex = 3: self.updateComboBoxStatus(optionSelected, optionIndex)
        self.comboBoxRate.currentIndexChanged[int].connect(l)

    @QtCore.Slot(int)
    def updateComboBoxStatus(self, newVal, changeCode):
        self.changesAvailable = True
        self.changed = changeCode
        if (changeCode == 3):
            self.rateIndex = newVal
            self.getRate()
        elif (changeCode == 2):
            self.resolIndex = newVal
            self.getResolution()

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
        combo = QComboBox(self)
        for item in items:
            combo.addItem(item)
        combo.setObjectName(objName)
        combo.setGeometry(QRect(xPos, yPos, 125, 22))
        combo.setCurrentIndex(startingIndex)
        return combo

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
        button = QRadioButton(self)
        button.setObjectName(name)
        button.setEnabled(True)
        button.setGeometry(QRect(xPos, yPos, 82, 17))
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setChecked(checked)
        lam = lambda id = idButton : self.buttonChecked(id)
        self.connect(button, SIGNAL("clicked()"), lam)
        self.filterTypeButtons.addButton(button, idButton)
        
    def buttonChecked(self, idButton):
        self.filterIndex = idButton

    def sys_exit(self, exitProgram):
        self.app.exec_()
        exitProgram.value = True
        sys.exit()

def runUserGUI(exitProgram):
    widget = micGui()
    widget.show()
    widget.sys_exit(exitProgram)
