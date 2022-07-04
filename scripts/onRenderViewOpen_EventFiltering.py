from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as mui

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)

class RenderViewFilter(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(RenderViewFilter, self).__init__(parent)

        self.setWindowTitle("Test OnRenderViewOpen")
        self.setMinimumSize(200, 100)
    
        self.maya_main_window = parent
        self.maya_main_window.installEventFilter(self)  
        
    def closeEvent(self, event):
        self.maya_main_window.removeEventFilter(self)
    
    def eventFilter(self, obj, event):

        if obj == self.maya_main_window:
            
            if event.type() == QtCore.QEvent.Type.ChildPolished:
                child = event.child()
                print(child)
                print("ChildPolished")
                print(child.objectName())
                if 'renderViewWindow' in child.objectName():
                    print("OPEN Render View")
                 
            if event.type() == QtCore.QEvent.Type.ChildRemoved:
                child = event.child()
                print(child)
                print("ChildRemoved")
                print(child.objectName())
                if 'renderViewWindow' in child.objectName():
                    print("CLOSED Render View")
              
        return False
        
     
if __name__ == "__main__":
    x = RenderViewFilter()
    x.show()