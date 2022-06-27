from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as mui

def getPyQtWindowByName(windowName):
    ptr = mui.MQtUtil.findWindow(windowName)
    if not ptr:
        ptr = mui.MQtUtil.findControl(windowName)
    return wrapInstance(int(ptr), QtWidgets.QDialog)

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)

def getRenderImage():
    renderWindow = getPyQtWindowByName("renderViewWindow")
    renderImageContainer = renderWindow.findChild(QtWidgets.QStackedWidget,"renderView")
    renderImage = renderImageContainer.findChild(QtWidgets.QWidget)
    #renderImageContainer.setStyleSheet("border: 2px solid red;")
    return renderImage
    
def extendRenderWindowToolbar():
    renderWindow = getPyQtWindowByName("renderViewWindow")
    toolbar = renderWindow.findChild(QtWidgets.QLayout,"renderViewToolbar")
    
    for x in renderWindow.findChildren(QtWidgets.QWidget):
        print(x)
        
    #Development code
    oldMenuBar = renderWindow.findChild(QtWidgets.QWidget,"StyleTransferButton")
    if oldMenuBar:
        oldMenuBar.setParent(None)
        
    styleTransferButton = QtWidgets.QPushButton()
    styleTransferButton.setIcon(QtGui.QIcon(QtGui.QPixmap("./media/icDocuments.svg")))
    styleTransferButton.clicked.connect(printTest)
    styleTransferButton.setObjectName("StyleTransferButton")
    styleTransferButton.setToolTip('Transfer the style of a selected image to the rendering')
    
    toolbar.addWidget(styleTransferButton)
    
def printTest():
    print("Test")
    
def extendRenderWindowMenuBar():
    renderWindow = getPyQtWindowByName("renderViewWindow")
    menubar = renderWindow.findChild(QtWidgets.QMenuBar,"renderView")
    
    #Development code
    oldMenuBar = renderWindow.findChild(QtWidgets.QWidget,"ImageEditMenuBar")
    if oldMenuBar:
        oldMenuBar.setParent(None)
        
    #Create MenuBar Item
    styleTransferOptionsAction = QtWidgets.QAction("Style Transfer Options",renderWindow) #QAction(QIcon('exit.png'), 'Exit', renderWindow)
    styleTransferOptionsAction.setShortcut('Ctrl+M')
    styleTransferOptionsAction.setStatusTip('Open Style Transfer Options')
    styleTransferOptionsAction.triggered.connect(printTest)
    
    #Create MenuBar
    newMenu = menubar.addMenu("AI Image Edit")
    newMenu.setObjectName("ImageEditMenuBar")
    newMenu.addAction(styleTransferOptionsAction)      
   

if __name__ == "__main__":
    extendRenderWindowToolbar()
    extendRenderWindowMenuBar()

def deconstructRenderView():
    renderWindow = getPyQtWindowByName("renderViewWindow")
    renderWindow.findChild(QtWidgets.QMenuBar,"renderView").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewToolbar").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewrenderInfoItem").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupDisplayMenu").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupresolutionItem").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopuprenderUsingItem").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupOptionsMenu").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupiprUpdateOptionsItem").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupiprRenderItem").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupIprMenu").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopuprenderSnapshotItem").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopuprenderRenderItem").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupRenderMenu").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupViewMenu").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopuploadPassFileItem").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupFileMenu").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"renderViewpopupMenu").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"iprMemEstText").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"pauseIprButton").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"closeIprButton").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget,"scrollBar").setParent(None)
    renderWindow.findChild(QtWidgets.QWidget).setParent(None)
    renderWindow.findChild(QtWidgets.QMenu).setParent(None)
    renderWindow.findChild(QtWidgets.QRubberBand).setParent(None)
    renderWindow.findChild(QtWidgets.QRubberBand).setParent(None)
    #renderWindow.findChild(QtWidgets.QTabBar).setParent(None) #Causes Crashes
    #renderWindow.findChild(QtWidgets.QWidget,"qt_splithandle_mayaLayoutInternalWidget").setParent(None) #Causes Error

    for x in renderWindow.findChildren(QtWidgets.QWidget):
        print(x)

    # Render Image hirarchy
    #--> Widget: <Object name not set>
    #--> Parent: renderView
    #--> Parent: editorForm
    #--> Parent: renderViewForm
    #--> Parent: renderView
    #--> Parent: renderViewWindow
    #--> Parent: qt_tabwidget_stackedwidget
    #--> Parent: mayaLayoutInternalWidget
    #--> Parent: mayaLayoutInternalWidget
    #--> Parent: mayaLayoutInternalWidget
    #--> Parent: mayaLayoutInternalWidget
    #--> Parent: workspacePanel1
    #--> Parent: MayaWindow 