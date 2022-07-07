from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as mui
import maya.cmds as cmds
from PIL.ImageQt import ImageQt
import os
import maya.app.general.createImageFormats as createImageFormats

from neural_style import neural_style
from optionWindow import OptionWindow
from image_super_resolution import image_super_resolution
from unload_packages import unload_packages


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

def openOptionsWindow():
    global option_window
    try:
        option_window.close() #pyling: disable=E0601
        option_window.deleteLater()
    except:
        pass 

    option_window = OptionWindow()
    option_window.show()

def run_service(name):
    # TODO: Display Loadingscreen 

    # Save rendered Image
    formatManager = createImageFormats.ImageFormats()
    formatManager.pushRenderGlobalsForDesc("JPEG")
    path = os.path.join(os.path.split(cmds.file(q=True, loc=True))[0], "Plugin/media/tmp/rendering.jpg")
    cmds.renderWindowEditor("renderView", e=True, writeImage=path)
    
    # Run Service
    image = None
    if name == "super_resolution":
        image = image_super_resolution.main(path)
    if name == "style_transfer":
        image = neural_style.main(path)
    
    # Display Image
    extendRenderWindowImage()
    extended_renderview_image.create_image(image)

def saveImage():
    extended_renderview_image.saveImage()

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
        self.styleTransferButton.setIcon(QtGui.QIcon(QtGui.QPixmap("./Plugin/media/icons/style_transfer.svg")))
        self.styleTransferButton.setToolTip('Run Neural Style Transfer on Rendering')
        self.styleTransferButton.clicked.connect(lambda: run_service("style_transfer"))
        
        # Image Super-Resolution
        self.superResolutionButton = QtWidgets.QPushButton()
        self.superResolutionButton.setIcon(QtGui.QIcon(QtGui.QPixmap("./Plugin/media/icons/image_super_resolution.svg")))
        self.superResolutionButton.setToolTip('Run Image Super-Resolution on Rendering')
        self.superResolutionButton.clicked.connect(lambda: run_service("super_resolution"))

        # Options
        self.openOptionsWindowButton = QtWidgets.QPushButton()
        self.openOptionsWindowButton.setIcon(QtGui.QIcon(QtGui.QPixmap("./Plugin/media/icons/settings.svg")))
        self.openOptionsWindowButton.setToolTip('Open AI-Image-Edit-Toolkit Options')
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
        super(ExtendedRenderViewMenuBar, self).__init__("AI Image Edit",self)

        self.setObjectName("ExtendedRenderViewMenuBar")

        # Add this QMenu to Render View MenuBar
        menubar = renderWindow.findChild(QtWidgets.QMenuBar,"renderView")
        menubar.addMenu(self)

        self.addActions()

    def addActions(self):
        # Options
        openOptionsAction = QtWidgets.QAction("Options",self) #QAction(QIcon('exit.png'), 'Exit', renderWindow)
        # openOptionsAction.setShortcut('Ctrl+M')
        openOptionsAction.setStatusTip('Options')
        openOptionsAction.triggered.connect(openOptionsWindow)
        self.addAction(openOptionsAction)   

        # Style Transfer
        styleTransferAction = QtWidgets.QAction("Run Neural Style Transfer",self)
        styleTransferAction.triggered.connect(lambda: run_service("style_transfer"))
        self.addAction(styleTransferAction)   

        # Image Super-Resolution
        superResolutionAction = QtWidgets.QAction("Run Image Super-Resolution",self) 
        superResolutionAction.triggered.connect(lambda: run_service("super_resolution"))
        self.addAction(superResolutionAction)   

        # Save Image
        saveImageAction = QtWidgets.QAction("Save Image",self)
        saveImageAction.triggered.connect(saveImage)
        self.addAction(saveImageAction)  

class ExtendedRenderViewImage(QtWidgets.QWidget):
    def __init__(self):
        self.renderWindow = getPyQtWindowByName("renderViewWindow")
        self.renderViewImageContainer = self.renderWindow.findChild(QtWidgets.QStackedWidget,"renderView")
        super(ExtendedRenderViewImage, self).__init__(self.renderViewImageContainer)

        self.setObjectName("ExtendedRenderViewImage")

        self.create_widgets()
        self.cerate_layout()
        
        self.renderWindow.installEventFilter(self)
    
    def create_widgets(self):
        # TODO: Loadinscreen

        self.image_widget = QtWidgets.QLabel("")
        self.image_widget.setAlignment(QtCore.Qt.AlignCenter)

    def cerate_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.image_widget)
        
    def create_image(self, pilImage):
        self.image = ImageQt(pilImage)
        
        self.pixmap = QtGui.QPixmap()
        self.pixmap.convertFromImage(self.image)
        self.pixmap_copy = QtGui.QPixmap()
        self.pixmap_copy.convertFromImage(self.image)

        self.image_widget.setPixmap(self.pixmap)
        
        self.resizeImage()
         
    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.Type.Resize:
            self.resizeImage()
        if event.type() == QtCore.QEvent.Type.Wheel:
            new_height = self.pixmap.size().height() + event.angleDelta().y()
            new_width = self.pixmap.size().width() + event.angleDelta().y()
            self.pixmap = self.pixmap_copy.scaled(new_width, new_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            self.image_widget.setPixmap(self.pixmap)

    def resizeImage(self):
        image_width = self.pixmap.size().width()
        image_height = self.pixmap.size().height()
        self_width = self.renderWindow.size().width()
        self_height = self.renderWindow.size().height() - 70

        if self_width < image_width or self_height < image_height:
            self.pixmap = self.pixmap_copy.scaled(self_width, self_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            self.image_widget.setPixmap(self.pixmap)

        if self_width < self.pixmap_copy.size().width() or self_height < self.pixmap_copy.size().height():
            self.pixmap = self.pixmap_copy.scaled(self_width, self_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            self.image_widget.setPixmap(self.pixmap)

    def saveImage(self):
        fileName, selected_filter = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image File","","Images (*.jpg *.jpeg *png *)")
        if fileName:
            self.image.save(fileName)

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

if __name__ == "__main__":
    unload_packages() 
    extendRenderWindow()