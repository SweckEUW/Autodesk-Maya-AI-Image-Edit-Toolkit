from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from neural_style import neural_style
from collapsible_widget import CollapsibleWidget
import os

from unload_packages import unload_packages
unload_packages(True,["collapsible_widget"])

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class OptionWindow(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(OptionWindow, self).__init__(parent)

        self.media_path = "C:/Users/Simon/Desktop/Projektarbeit/Autodesk-Maya-AI-Toolkit/media/"
        self.style_img_path = [self.media_path+"style7.jpg"]

        self.setWindowTitle("Option Window")
        self.resize(400,600)

        self.create_widgets()
        self.create_layouts()
        self.createMenuBar()

    def create_widgets(self):
        self.collapsible_a = CollapsibleWidget("Style Transfer")
        self.addWidgetsCollapsibleA()
            
        self.collapsible_b = CollapsibleWidget("Upscale")
        for i in range(6):
            self.collapsible_b.add_widget(QtWidgets.QPushButton("Button {0}".format(i)))
            

    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(4)
        form_layout.addRow(self.collapsible_a)
        form_layout.addRow(self.collapsible_b)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(form_layout)
        
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName("ai_scrollArea")
        scrollArea.setStyleSheet('#ai_scrollArea { border: none; }')
        scrollArea.setWidget(main_widget)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0,15,0,0)
        main_layout.addWidget(scrollArea)
        
    def addWidgetsCollapsibleA(self):
        main_layout = QtWidgets.QGridLayout()
        main_layout.setHorizontalSpacing(20)
        self.collapsible_a.add_layout(main_layout)
        
        def createHBoxWidget(text):
            label = QtWidgets.QLabel(text)
            hbox = QtWidgets.QHBoxLayout()
            main_layout.addWidget(label,main_layout.rowCount(),0)
            main_layout.addLayout(hbox,main_layout.rowCount()-1,1)
            return hbox
            
        # Itterations
        hbox1 = createHBoxWidget("Itterations")
        self.itterations_lineedit = QtWidgets.QLineEdit("1000")
        self.itterations_lineedit.setStyleSheet('background-color: rgb(43,43,43);')
        self.itterations_lineedit.setValidator(QtGui.QIntValidator())
        hbox1.addWidget(self.itterations_lineedit)
            
        # Keep original colors
        hbox2 = createHBoxWidget("Keep original colors")
        self.keepcolor_checkbox = QtWidgets.QCheckBox()
        #self.keepcolor_checkbox.setStyleSheet('QCheckBox::indicator {background-color: rgb(43,43,43); }"')
        hbox2.addWidget(self.keepcolor_checkbox)

        # Style weight
        hbox3 = createHBoxWidget("Style weight")
        self.styleweight_lineedit = QtWidgets.QLineEdit("100")
        self.styleweight_lineedit.setStyleSheet('background-color: rgb(43,43,43);')
        hbox3.addWidget(self.styleweight_lineedit)
        
        # Content weight
        hbox4 = createHBoxWidget("Content weight")
        self.contentweight_lineedit = QtWidgets.QLineEdit("4")
        self.contentweight_lineedit.setStyleSheet('background-color: rgb(43,43,43);')
        hbox4.addWidget(self.contentweight_lineedit)
        
        # Style scale
        hbox5 = createHBoxWidget("Style scale")
        self.stylescale_lineedit = QtWidgets.QLineEdit("1")
        self.stylescale_lineedit.setValidator(QtGui.QIntValidator())
        self.stylescale_lineedit.setStyleSheet('background-color: rgb(43,43,43);')
        hbox5.addWidget(self.stylescale_lineedit)
                
        # Output Path
        # hbox2 = createHBoxWidget("Select File")
        # self.output_path_lineedit = QtWidgets.QLineEdit("C:/Users/Simon/Desktop/Output")
        # hbox2.addWidget(self.output_path_lineedit)
        # select_file_button = QtWidgets.QPushButton()
        # select_file_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        # select_file_button.clicked.connect(self.select_directory)
        # hbox2.addWidget(select_file_button)
        # self.collapsible_a.add_layout(hbox2)
        
        
    def select_directory(self):
        output_path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(self,"Select File", os.getcwd(), 'All Files(*.*)')
        
        #output_path = cmds.fileDialog2(fileFilter="All Files (*.*)", dialogStyle=2, fileMode=1, cap='Open Image')
        if output_path:
            self.output_path_lineedit.setText(output_path)
        
    def createMenuBar(self):
        mainMenu = QtWidgets.QMenuBar(self)
        
        test = QtWidgets.QAction("Test",self) #QAction(QIcon('exit.png'), 'Exit', renderWindow)
        test.setShortcut('Ctrl+M')
        test.setStatusTip('Options')
        test.triggered.connect(lambda x: print("Test"))
        
        editMenu = mainMenu.addMenu("Edit")
        editMenu.addAction(test)     
        
        presetsMenu = mainMenu.addMenu("Presets")
        

if __name__ == "__main__":
    try:
        option_window.close() #pyling: disable=E0601
        option_window.deleteLater()
    except:
        pass
    
    option_window = OptionWindow()
    option_window.show()
