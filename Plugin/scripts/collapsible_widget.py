from PySide2 import QtCore, QtGui, QtWidgets

class CollapsibleHeader(QtWidgets.QWidget):
    
    COLLAPSED_PIXMAP = QtGui.QPixmap(":teRightArrow.png")
    EXPANDED_PIXMAP = QtGui.QPixmap(":teDownArrow.png")
    
    clicked = QtCore.Signal()
    
    def __init__(self, text, parent=None):
        super(CollapsibleHeader, self).__init__(parent)
        
        self.setAutoFillBackground(True)
        self.set_background_color(None)
        
        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedWidth(self.COLLAPSED_PIXMAP.width())
        self.text_label = QtWidgets.QLabel()
        self.text_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(15)
        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addWidget(self.text_label)
        
        self.set_text(text)
        self.set_expanded(True)
        
    def set_text(self, text):
        self.text_label.setText("<b>{0}</b>".format(text))
        
    def set_background_color(self, color):
        if not color:
            color = QtWidgets.QPushButton().palette().color(QtGui.QPalette.Button)
        
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)
        
    def is_expanded(self):
        return self._expanded
        
    def set_expanded(self, expanded):
        self._expanded = expanded
        
        if(self._expanded):
            self.icon_label.setPixmap(self.EXPANDED_PIXMAP)
        else:
            self.icon_label.setPixmap(self.COLLAPSED_PIXMAP)
            
    def mouseReleaseEvent(self, event):
        self.clicked.emit()  # pylint: disable=E1101
            
    
class CollapsibleWidget(QtWidgets.QWidget):
    
    def __init__(self, text, parent=None):
        super(CollapsibleWidget, self).__init__(parent)
        
        self.header_wdg = CollapsibleHeader(text)
        self.header_wdg.clicked.connect(self.on_header_clicked)  # pylint: disable=E1101
        
        self.body_wdg = QtWidgets.QWidget()
        self.body_layout = QtWidgets.QVBoxLayout(self.body_wdg)

        self.body_wdg.setStyleSheet("background-color: rgb(74,74,74);")
        self.body_wdg.setContentsMargins(50, 0, 0, 0)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.header_wdg)
        self.main_layout.addWidget(self.body_wdg)
        
        self.set_expanded(True) 
        
    def add_widget(self, widget):
        self.body_layout.addWidget(widget)
        
    def add_layout(self, layout):
        self.body_layout.addLayout(layout)
        
    def set_expanded(self, expanded):
        self.header_wdg.set_expanded(expanded)
        self.body_wdg.setVisible(expanded)
        
    def set_header_background_color(self, color):
        self.header_wdg.set_background_color(color)
        
    def on_header_clicked(self):
        self.set_expanded(not self.header_wdg.is_expanded())
        