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

    checkbox = QtWidgets.QCheckBox()
    checkbox.setObjectName("NEW NEW NEW")
    checkbox.setParent(toolbar)
        
    toolbar.setParent(None)
    
    for x in toolbar.children():
        print(x)
        
    #for x in toolbar.findChildren(QtWidgets.QWidget):
       #print(x)
       
    #for x in QtWidgets.QApplication.allWidgets():
       # print(x.__class__.__name__)
        #if x.__class__.__name__ == "QImage":
            #print(x.objectName())
            #print("found one")
            #print(" ")

def printTest():
    print("Test")
    
def extendRenderWindowMenuBar():
    renderWindow = getPyQtWindowByName("renderViewWindow")
    menubar = renderWindow.findChild(QtWidgets.QMenuBar,"renderView")
    
    #Create MenuBar Item
    styleTransferOptionsAction = QtWidgets.QAction("Style Transfer Options",renderWindow) #QAction(QIcon('exit.png'), 'Exit', renderWindow)
    styleTransferOptionsAction.setShortcut('Ctrl+M')
    styleTransferOptionsAction.setStatusTip('Open Style Transfer Options')
    styleTransferOptionsAction.triggered.connect(printTest)
    
    #Create MenuBar
    newMenu = menubar.addMenu("Test")
    newMenu.addAction(styleTransferOptionsAction)      
   

if __name__ == "__main__":
    extendRenderWindowToolbar()

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