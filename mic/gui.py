# This Python file uses the following encoding: utf-8
import time
import sys
import os
import ctypes

from filters.settings import guiSettings
from mic import handlers as han
from multiprocessing import Queue

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, QTime, QUrl, Qt,
                            SLOT, SIGNAL, QFile)
from PySide2.QtGui import  (QBrush, QColor, QConicalGradient, QCursor, QFont,
                            QFontDatabase, QIcon, QKeySequence, QLinearGradient, 
                            QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import (QApplication, QWidget, QSlider, QPlainTextEdit, 
                               QDialog, QGridLayout, QRadioButton, QButtonGroup, 
                               QComboBox, QLabel, QPushButton)
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader

myappid = 'bokus-filter' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# gives life to main window for mic filtering
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
    modeIndex = -1
    filterIndex = -1
    guiSettings = guiSettings(initValues = [0, 2, 3, 0, 50])
    queue = Queue()
    
    # Initializes graphical setup and updates queue
    def __init__(self, queue, numberOfHandles = 10):
        super(micGui, self).__init__()
        self.setupGui(numberOfHandles)
        self.queue = queue
    
    # Configs graphical elements and their initializations
    def setupGui(self, numberOfHandles):
        self.configWindow()
        self.configureBackground()
        self.resolutionOptions()
        self.samplingRateOptions()
        self.modeOptions()
        self.showSettingsButton()
        for i in range(numberOfHandles):
            self.sliders.append(self.createImgSlider("./mic/gui/filter-gui/slider.png", i))
            self.sliders[i].valueChanged[int].connect(lambda val, index = i: self.setHandlers(val, index))
            self.handlers.register_callback(self.updateHandlersStatus)

    # Updates handle value when signal is received and sends
    # a signal for filter updater
    def updateHandlersStatus(self, handleNumber):
        self.changesAvailable = True
        self.handleUpdated = handleNumber
        self.changed = 0

    # Sends gui settings
    def setHandlers(self, newVal, handlerID):
        self.guiSettings.updatesAvailable = True
        self.guiSettings.handleSelected = handlerID
        self.guiSettings.handleValue = newVal
        self.queue.put(self.guiSettings)

    # Initializes resolution options and it's changes callback
    def resolutionOptions(self):
        resolutions = ["Ultra High", "High", "Normal", "Low", "Ultra Low"]
        self.comboBoxResol = self.setComboBox(2, 542, 187, "comboBoxResol", resolutions)
        l = lambda optionSelected, optionIndex = 2: self.updateComboBoxStatus(optionSelected, optionIndex)
        self.comboBoxResol.currentIndexChanged[int].connect(l)

    # Initializes sampling rate options and it's changes callback
    def samplingRateOptions(self):
        rates = ["48000", "44100", "32000", "22050", "11025", "8000"]
        self.comboBoxRate = self.setComboBox(3, 542, 125, "comboBoxRate", rates)
        l = lambda optionSelected, optionIndex = 3: self.updateComboBoxStatus(optionSelected, optionIndex)
        self.comboBoxRate.currentIndexChanged[int].connect(l)

    # Initializes mode options and it's changes callback
    def modeOptions(self):
        modes = ["FIR (slow)", "Butterworth (fast)", "Devil", "Goblin"]
        self.comboBoxMode = self.setComboBox(0, 542, 63, "comboBoxMode", modes)
        l = lambda optionSelected, optionIndex = 1: self.updateComboBoxStatus(optionSelected, optionIndex)
        self.comboBoxMode.currentIndexChanged[int].connect(l)

    # If any combo box option is changed, this callback is called.
    # Sends update to updates queue.
    @QtCore.Slot(int)
    def updateComboBoxStatus(self, newVal, changeCode):
        self.changesAvailable = True
        self.changed = changeCode
        if (changeCode == 3):
            self.rateIndex = newVal
            self.guiSettings.rateSelected = newVal
        elif (changeCode == 2):
            self.resolIndex = newVal
            self.guiSettings.resolutionSelected = newVal
        elif (changeCode == 1):
            self.filterIndex = newVal
            self.guiSettings.filterSelected = newVal
        self.queue.put(self.guiSettings)

    # Sets background image
    def configureBackground(self):
        image = "mic/gui/filter-gui/UI.png"

        self.text_field = QPlainTextEdit(self)
        self.text_field.setDisabled(True)
        self.text_field.setMinimumSize(720, 301)
        self.text_field.setStyleSheet(  "background-image: url(" + 
                                        image + 
                                        "); background-attachment: fixed"
                                    )

    # Initializes combo box
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
        combo.setStyleSheet("background-color: rgb(47, 47, 47) ; color: rgb(255, 96, 96);")
        return combo

    # Initializes Windows and title bar icons
    def configIcons(self):
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon16.png', QSize(16,16))
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon24.png', QSize(24,24))
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon32.png', QSize(32,32))
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon48.png', QSize(48,48))
        self.app_icon.addFile('mic/gui/filter-gui/icon/icon256.png', QSize(256,256))
        self.app.setWindowIcon(self.app_icon)

    # Initializes general window's elements like 
    # title Bar and window size
    def configWindow(self):
        self.configIcons()
        self.setWindowTitle('Bokus Multiband Filter')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setFixedSize(720, 301)

    # Creates an slider, with an image as a handle
    def createImgSlider(self, imgPath, index):
        xPosition = 36 + 47 * index
        slider = QSlider(self)
        slider.setObjectName(u"slider" + str(index))
        slider.setGeometry(QRect(xPosition, -1, 51, 300))
        slider.setCursor(QCursor(Qt.OpenHandCursor))
        slider.setMouseTracking(False)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setAcceptDrops(False)
        slider.setAutoFillBackground(False)
        slider.setStyleSheet(    u"QSlider::handle:vertical {\n"
                                                "	image: url(" + imgPath + ");\n"
                                                "	width: 90px;\n"
                                                "	height: 90px\n"
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

    # [DEPRECATED] loads GUI from from.ui (PyQt)
    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "./gui/filter-gui/form2.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    # [DEPRECATED. Replaced with combo boxes] loads buttons for mode selecting.
    def filterModeButtons(self):
        self.filterTypeButtons = QButtonGroup(self)
        self.configFilterTypeButtons("firButton", True, 560, 49, 0)
        self.configFilterTypeButtons("iirButton", False, 560, 68, 1)
        self.configFilterTypeButtons("devilButton", False, 560, 86, 2)
        self.configFilterTypeButtons("goblinButton", False, 560, 104, 3)

    # [DEPRECATED. Used in filterModeButtons]
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

    # [DEPRECATED. Used in filterModeButtons]
    def buttonChecked(self, idButton):
        self.filterIndex = idButton
        self.guiSettings.filterSelected = idButton
        self.queue.put(self.guiSettings)

    # Properly closes GUI if flag is received
    def sys_exit(self, exitProgram):
        self.app.exec_()
        exitProgram.value = True
        self.queue.put(None)
        sys.exit()

    # Properly closes settings window
    def closeEvent(self, event):
        self.closeSettings()

    # Properly closes settings window
    def closeSettings(self):
        if hasattr(self, 'sets'):
            self.sets.close()

    # Initializes button for opening settings
    def showSettingsButton(self):
        image = "./mic/gui/filter-gui/settings-button.png"
        imageHover = "./mic/gui/filter-gui/settings-button-hover.png"
        button = QPushButton("", self) 
        button.setGeometry(685, 10, 24, 27)
        button.setStyleSheet("border-radius : 50") 
        button.setStyleSheet("QPushButton {border-image: url("+image+"); } QPushButton:hover { border-image: url("+imageHover+")}")
        button.clicked.connect(self.openSettings)
        self.settingsButton = button

    # Shows settings
    def openSettings(self):
        self.sets = settingsWindow()
        self.sets.show()

# gives life to settings window for mic filtering
# Includes License related info.
class settingsWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Settings')
        self.setFixedSize(320, 500)
        layout = QGridLayout()
        self.label = QLabel()
        self.label.setOpenExternalLinks(True)
        text = ("<strong>Software developed using:</strong><br>"
                "Qt for Python under LGPL v3 and GPL v3 licenses.<br>"
                "Qt sources will be provided on demand, contact me if needed.<br>"
                "<a href=\"https://wiki.qt.io/Building_Qt_5_from_Git#Getting_the_source_code\">Official download</a>.<br>"
                "<br>"
                "NumPy under the BSD 3-Clause License. <br>"
                "<br>"
                "PyAudio under the MIT License. <br>"
                "<br>"
                "Check binaries to see licenses.")
        
        self.label.setText(text)
        self.label.setTextFormat(Qt.RichText)
        self.label.openExternalLinks()
        layout.addWidget(self.label)
        self.button = QPushButton('Close')
        self.button.clicked.connect(self.close)
        layout.addWidget(self.button)
        self.setLayout(layout)

# runs main window
def runUserGUI(exitProgram, queue):
    mainWindow = micGui(queue)
    mainWindow.show()
    mainWindow.sys_exit(exitProgram)
