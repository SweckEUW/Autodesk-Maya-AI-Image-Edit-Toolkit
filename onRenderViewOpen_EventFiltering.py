from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as mui

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)

def getPyQtWindowByName(windowName):
    ptr = mui.MQtUtil.findWindow(windowName)
    if not ptr:
        ptr = mui.MQtUtil.findControl(windowName)
    return wrapInstance(int(ptr), QtWidgets.QDialog)

    
class RenderViewFilter(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(RenderViewFilter, self).__init__(parent)

        self.setWindowTitle("Test OnRenderViewOpen")
        self.setMinimumSize(200, 100)
    
        self.maya_main_window = maya_main_window()
        self.maya_main_window.installEventFilter(self)  
        
    def closeEvent(self, event):
        self.maya_main_window.removeEventFilter(self)
    
    def eventFilter(self, obj, event):

        if obj == self.maya_main_window:

            print(event.type())

            # if event.type() == QtCore.QEvent.Type.ChildPolished:
                # child = event.child()
                # print("@@@@@@@@@@@@@@@@@@")
                
                # print(child)
                # print(child.children())
                # print(child.findChildren(QtWidgets.QWidget))
                # print(child.parent())
                # print(child.parentWidget())
                # print(child.winId())
                # print(child.accessibleName())
                # print(child.objectName())
                
                # print("@@@@@@@@@@@@@@@@@@@@@")
                
                # for x in child.findChildren(QtWidgets.QWidget):
                #     print(x.objectName())
                #     if x.objectName() == "mayaLayoutInternalWidget":
                #         print("OPEN")
                        
            # if event.type() == QtCore.QEvent.Type.ChildRemoved:
                # child = event.child()

                # print(child)
                # print(child.children())
                # print(child.findChildren(QtWidgets.QWidget))
                # print(child.parent())
                #print(child.parentWidget())
                #print(child.winId())
                #print(child.accessibleName())
                # print(child.objectName())

                # if 'renderViewWindow' in child.objectName():
                #     doStuff()
                          
        return False
               

     
if __name__ == "__main__":
    x = RenderViewFilter()
    x.show()