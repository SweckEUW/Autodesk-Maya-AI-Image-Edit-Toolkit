from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as mui
from neural_style import neural_style
from optionWindow import OptionWindow
import maya.cmds as cmds


option_window = None
extended_renderview_menubar = None
extended_renderview_image = None
extended_renderview_toolbar = None

def getPyQtWindowByName(windowName):
    ptr = mui.MQtUtil.findWindow(windowName)
    if not ptr:
        ptr = mui.MQtUtil.findControl(windowName)
    return wrapInstance(int(ptr), QtWidgets.QDialog)

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)

def style_transfer():
    neural_style.main()
    extendRenderWindowImage()
    extended_renderview_image.update_image("C:/Users/Simon/Desktop/Output/output.jpg")

def openOptionsWindow():
    global option_window
    try:
        option_window.close() #pyling: disable=E0601
        option_window.deleteLater()
    except:
        pass 

    option_window = OptionWindow()
    option_window.show()

def super_resolution():
    print("Test")

class ExtendedRenderViewToolbar(QtWidgets.QWidget):
    def __init__(self):
        renderWindow = getPyQtWindowByName("renderViewWindow")
        super(ExtendedRenderViewToolbar, self).__init__(renderWindow)
        
        self.setObjectName("ExtendedRenderViewToolbar")

        toolbar = renderWindow.findChild(QtWidgets.QLayout,"renderViewToolbar")
        toolbar.addWidget(self)

        self.create_widgets()
        self.cerate_layout()

    def create_widgets(self):
        # Neural style transfer
        self.styleTransferButton = QtWidgets.QPushButton()
        self.styleTransferButton.setIcon(QtGui.QIcon(QtGui.QPixmap("./media/icons/style_transfer.svg")))
        self.styleTransferButton.setToolTip('Run Neural style transfer')
        self.styleTransferButton.clicked.connect(style_transfer)
        
        # Image Super-Resolution
        self.superResolutionButton = QtWidgets.QPushButton()
        self.superResolutionButton.setIcon(QtGui.QIcon(QtGui.QPixmap("./media/icons/image_super_resolution.svg")))
        self.superResolutionButton.setToolTip('Run Image Super-Resolution')
        self.superResolutionButton.clicked.connect(super_resolution)

        # Options
        self.openOptionsWindowButton = QtWidgets.QPushButton()
        self.openOptionsWindowButton.setIcon(QtGui.QIcon(QtGui.QPixmap("./media/icons/settings.svg")))
        self.openOptionsWindowButton.setToolTip('Open AI Image Edit Options')
        self.openOptionsWindowButton.clicked.connect(openOptionsWindow)

    def cerate_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(4)
        main_layout.addWidget(self.openOptionsWindowButton)
        main_layout.addWidget(self.styleTransferButton)
        main_layout.addWidget(self.superResolutionButton)

class ExtendedRenderViewMenuBar(QtWidgets.QMenu):
    def __init__(self):
        renderWindow = getPyQtWindowByName("renderViewWindow")
        super(ExtendedRenderViewMenuBar, self).__init__("AI Image Edit",renderWindow)

        self.setObjectName("ExtendedRenderViewMenuBar")

        self.addActions()

        # Add this QMenu to Render View MenuBar
        menubar = renderWindow.findChild(QtWidgets.QMenuBar,"renderView")
        menubar.addMenu(self)

    def addActions(self):
        # Options
        openOptionsAction = QtWidgets.QAction("Options",self) #QAction(QIcon('exit.png'), 'Exit', renderWindow)
        openOptionsAction.setShortcut('Ctrl+M')
        openOptionsAction.setStatusTip('Options')
        openOptionsAction.triggered.connect(openOptionsWindow)
        self.addAction(openOptionsAction)   

        # Style Transfer
        styleTransferAction = QtWidgets.QAction("Run Style Transfer",self)
        styleTransferAction.triggered.connect(style_transfer)
        self.addAction(styleTransferAction)   

        # Image Super-Resolution
        superResolutionAction = QtWidgets.QAction("Run Image Super-Resolution",self) 
        superResolutionAction.triggered.connect(super_resolution)
        self.addAction(superResolutionAction)   

class ExtendedRenderViewImage(QtWidgets.QWidget):
    def __init__(self):
        renderWindow = getPyQtWindowByName("renderViewWindow")
        renderViewImageContainer = renderWindow.findChild(QtWidgets.QStackedWidget,"renderView")
        super(ExtendedRenderViewImage, self).__init__(renderViewImageContainer)

        self.setObjectName("ExtendedRenderViewImage")

        self.create_widgets()
        self.cerate_layout()
    
    def create_image(self):
        image = QtGui.QImage("C:/Users/Simon/Desktop/Output/Output.jpg")
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image)

        self.image_widget = QtWidgets.QLabel("")
        self.image_widget.setAlignment(QtCore.Qt.AlignCenter)
        self.image_widget.setPixmap(pixmap)
        self.image_widget.setScaledContents(False)

    def create_widgets(self):
        self.create_image()

    def cerate_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.image_widget)
        
    def update_image(self, url):
        image = QtGui.QImage(url)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image)
        self.image_widget.setPixmap(pixmap)
         
    def eventFilter(self, widget, event):
        # TODO: overwrite resize event to scale image down
        pass

    def paintEvent(self, paint_event):
        parent = self.parentWidget()
        self.setGeometry(parent.geometry())
        painter = QtGui.QPainter(self)
        fill_color = QtGui.QColor(44,44,44)
        painter.fillRect(0, 0, self.width(), self.height(), fill_color)

def extendRenderWindowMenuBar():
    oldMenu = getPyQtWindowByName("renderViewWindow").findChild(QtWidgets.QMenu,"ExtendedRenderViewMenuBar")
    if(oldMenu):
        oldMenu.setParent(None)

    global extended_renderview_menubar
    extended_renderview_menubar = ExtendedRenderViewMenuBar()
    extended_renderview_menubar.show()

def extendRenderWindowImage():
    oldImage = getPyQtWindowByName("renderViewWindow").findChild(QtWidgets.QWidget,"ExtendedRenderViewImage")
    if(oldImage):
        oldImage.setParent(None)

    global extended_renderview_image
    extended_renderview_image = ExtendedRenderViewImage()
    extended_renderview_image.show()

def extendRenderWindowToolbar():
    oldToolbar = getPyQtWindowByName("renderViewWindow").findChild(QtWidgets.QWidget,"ExtendedRenderViewToolbar")
    if(oldToolbar):
        oldToolbar.setParent(None)

    global extended_renderview_toolbar
    extended_renderview_toolbar = ExtendedRenderViewToolbar()
    extended_renderview_toolbar.show()

def extendRenderWindow():
    print("AI_TOOLKIT : Extending Render Window")
    extendRenderWindowToolbar()
    extendRenderWindowMenuBar()
    #extendRenderWindowImage()

if __name__ == "__main__":
    extendRenderWindow()