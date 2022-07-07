from PySide2 import QtGui, QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import webbrowser
import maya.cmds as cmds
import os

from collapsible_widget import CollapsibleWidget
from optionWindow_utils import updateOptions, getOptions
from unload_packages import unload_packages


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


option_window = None
class OptionWindow(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(OptionWindow, self).__init__(parent)

        self.setWindowTitle("Option Window")
        self.resize(600,600)

        self.optionsJson = getOptions()

        self.create_widgets()
        self.create_layouts()
        self.createMenuBar()

    def create_widgets(self):
        self.collapsible_a = CollapsibleWidget("Neural Style Transfer")
        self.addWidgetsCollapsibleA()

        self.collapsible_b = CollapsibleWidget("Image Super-Resolution")
        self.addWidgetsCollapsibleB()

        self.collapsible_c = CollapsibleWidget("Neural Dream")
        self.addWidgetsCollapsibleC()
            

    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(4)
        form_layout.addRow(self.collapsible_a)
        form_layout.addRow(self.collapsible_b)
        form_layout.addRow(self.collapsible_c)

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
    
    def addWidgetsCollapsibleC(self):
        main_layout = QtWidgets.QGridLayout()
        main_layout.setHorizontalSpacing(20)
        main_layout.setVerticalSpacing(20)
        self.collapsible_c.add_layout(main_layout)

        def createHBoxWidget(text,widgets,tooltip_text):
            label = QtWidgets.QLabel(text)
            label.setToolTip(tooltip_text)
            hbox = QtWidgets.QHBoxLayout()
            main_layout.addWidget(label,main_layout.rowCount(),0)
            main_layout.addLayout(hbox,main_layout.rowCount()-1,1)
            for widget in widgets:
                hbox.addWidget(widget)
            return hbox

        # Itterations
        itterations_label = QtWidgets.QLabel(str(self.optionsJson["neural_dream"]["itterations"]))
        itterations_label.setMinimumWidth(25)
        itterations_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        itterations_slider.setMinimum(1)
        itterations_slider.setMaximum(50)
        itterations_slider.setValue(int(self.optionsJson["neural_dream"]["itterations"]))
        itterations_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        itterations_slider.valueChanged.connect(lambda: (
            updateOptions("neural_dream","itterations",itterations_slider.value()),
            itterations_label.setText(str(itterations_slider.value()))
        ))
        createHBoxWidget("Itterations",[itterations_label,itterations_slider],"")

        # Learning rate
        learning_rate_label = QtWidgets.QLabel(str(self.optionsJson["neural_dream"]["learning_rate"]))
        learning_rate_label.setMinimumWidth(25)
        learning_rate_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        learning_rate_slider.setMinimum(0)
        learning_rate_slider.setMaximum(50)
        learning_rate_slider.setValue(int(self.optionsJson["neural_dream"]["learning_rate"]*10))
        learning_rate_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        learning_rate_slider.valueChanged.connect(lambda: (
            updateOptions("neural_dream","learning_rate",learning_rate_slider.value()/10),
            learning_rate_label.setText(str(learning_rate_slider.value()/10)) 
        ))
        createHBoxWidget("Learning rate",[learning_rate_label,learning_rate_slider],'Learning rate to use with the ADAM and L-BFGS optimizers. Default is 1.5. On other DeepDream projects this parameter is commonly called step size') 

        # Keep original colors
        keepcolor_checkbox = QtWidgets.QCheckBox()
        keepcolor_checkbox.setChecked(self.optionsJson["neural_dream"]["original_colors"] == "True")
        keepcolor_checkbox.toggled.connect(lambda: ( 
            updateOptions("neural_dream","original_colors",str(keepcolor_checkbox.isChecked()))
        ))
        createHBoxWidget("Keep original colors",[keepcolor_checkbox],"The output image will retain the colors of the original image")

    def addWidgetsCollapsibleB(self):
        main_layout = QtWidgets.QGridLayout()
        main_layout.setHorizontalSpacing(20)
        self.collapsible_b.add_layout(main_layout)

        label = QtWidgets.QLabel("Model")
        label.setToolTip("Selected Neural Network for Image Super-Resolution")

        r0 = QtWidgets.QRadioButton("SRGAN")
        r0.setChecked(self.optionsJson["image_super_resolution"]["model"] == "SRGAN")
        r0.setToolTip("Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network (SRGAN)")

        r1 = QtWidgets.QRadioButton("EDSR")
        r1.setChecked(self.optionsJson["image_super_resolution"]["model"] == "EDSR")
        r0.setToolTip("Enhanced Deep Residual Networks for Single Image Super-Resolution (EDSR), winner of the NTIRE 2017 super-resolution challenge")

        r2 = QtWidgets.QRadioButton("WDSR")
        r2.setChecked(self.optionsJson["image_super_resolution"]["model"] == "WDSR")
        r0.setToolTip("Wide Activation for Efficient and Accurate Image Super-Resolution (WDSR), winner of the NTIRE 2018 super-resolution challenge (realistic tracks).")

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(r0) 
        hbox.addWidget(r1)
        hbox.addWidget(r2)

        number_group = QtWidgets.QButtonGroup()
        number_group.addButton(r0)
        number_group.addButton(r1)
        number_group.addButton(r2)
        number_group.buttonClicked.connect(lambda: updateOptions("image_super_resolution","model",number_group.checkedButton().text()))

        main_layout.addWidget(label,0,0)
        main_layout.addLayout(hbox,0,1)
    
    def addWidgetsCollapsibleA(self):
        main_layout = QtWidgets.QGridLayout()
        main_layout.setHorizontalSpacing(20)
        main_layout.setVerticalSpacing(20)
        self.collapsible_a.add_layout(main_layout)

        def createHBoxWidget(text,widgets,tooltip_text):
            label = QtWidgets.QLabel(text)
            label.setToolTip(tooltip_text)
            hbox = QtWidgets.QHBoxLayout()
            main_layout.addWidget(label,main_layout.rowCount(),0)
            main_layout.addLayout(hbox,main_layout.rowCount()-1,1)
            for widget in widgets:
                hbox.addWidget(widget)
            return hbox
        
        style_images = OptionWindowStyleImageSelection()
        createHBoxWidget("Style Images",[style_images],"When using multiple style images, you can control the degree to which they are blended")

        QSS = """
            QSlider::groove:horizontal {
                border-radius: 1px;
                height: 5px;
                margin: 0px;
                background-color: rgb(43,43,43);
            }
            QSlider::groove:horizontal:hover {
                background-color: rgb(63,63,63);
            }
            QSlider::handle:horizontal {
                background-color: rgb(189,189,189);
                border: none;
                height: 20px;
                width: 8px;
                margin: -20px 0;
                border-radius: 50px;
            }
            QSlider::handle:horizontal:hover {
                background-color: rgb(200,200,200);
            }
            QSlider::handle:horizontal:pressed {
                background-color: rgb(170, 170, 170);
            }
            QLineEdit{
                background-color: rgb(43,43,43);
            }
            QToolTip { 
                color: #ffffff; 
            }
        """
        self.setStyleSheet(QSS)

        # Itterations
        itterations_label = QtWidgets.QLabel(str(self.optionsJson["style_transfer"]["itterations"]))
        itterations_label.setMinimumWidth(25)
        itterations_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        itterations_slider.setMinimum(1)
        itterations_slider.setMaximum(1500)
        itterations_slider.setValue(int(self.optionsJson["style_transfer"]["itterations"]))
        itterations_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        itterations_slider.valueChanged.connect(lambda: (
            updateOptions("style_transfer","itterations",itterations_slider.value()),
            itterations_label.setText(str(itterations_slider.value()))
        ))
        createHBoxWidget("Itterations",[itterations_label,itterations_slider],"")
            
        # Keep original colors
        keepcolor_checkbox = QtWidgets.QCheckBox()
        keepcolor_checkbox.setChecked(self.optionsJson["style_transfer"]["original_colors"] == "True")
        keepcolor_checkbox.toggled.connect(lambda: ( 
            updateOptions("style_transfer","original_colors",str(keepcolor_checkbox.isChecked()))
        ))
        createHBoxWidget("Keep original colors",[keepcolor_checkbox],"The output image will retain the colors of the original image")

        # Style weight
        styleweight_label = QtWidgets.QLabel(str(self.optionsJson["style_transfer"]["style_weight"]))
        styleweight_label.setMinimumWidth(25)
        styleweight_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        styleweight_slider.setMinimum(1)
        styleweight_slider.setMaximum(400)
        styleweight_slider.setValue(int(self.optionsJson["style_transfer"]["style_weight"]))
        styleweight_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        styleweight_slider.valueChanged.connect(lambda: (
            updateOptions("style_transfer","style_weight",styleweight_slider.value()),
            styleweight_label.setText(str(styleweight_slider.value()))
        ))
        createHBoxWidget("Style weight",[styleweight_label,styleweight_slider],'How much to weight the style reconstruction term. Default is 100')
        
        # Content weight
        contentweight_label = QtWidgets.QLabel(str(self.optionsJson["style_transfer"]["content_weight"]))
        contentweight_label.setMinimumWidth(25)
        contentweight_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        contentweight_slider.setMinimum(1)
        contentweight_slider.setMaximum(200)
        contentweight_slider.setValue(int(self.optionsJson["style_transfer"]["content_weight"]))
        contentweight_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        contentweight_slider.valueChanged.connect(lambda: (
            updateOptions("style_transfer","content_weight",contentweight_slider.value()),
            contentweight_label.setText(str(contentweight_slider.value()))
        ))
        createHBoxWidget("Content weight",[contentweight_label,contentweight_slider],'How much to weight the content reconstruction term. Default is 5')
        
        # Style scale
        stylescale_label = QtWidgets.QLabel(str(self.optionsJson["style_transfer"]["style_scale"]))
        stylescale_label.setMinimumWidth(25)
        stylescale_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        stylescale_slider.setMinimum(0)
        stylescale_slider.setMaximum(50)
        stylescale_slider.setValue(int(self.optionsJson["style_transfer"]["style_scale"]*10))
        stylescale_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        stylescale_slider.valueChanged.connect(lambda: (
            updateOptions("style_transfer","style_scale",stylescale_slider.value()/10),
            stylescale_label.setText(str(stylescale_slider.value()/10)) 
        ))
        createHBoxWidget("Style scale",[stylescale_label,stylescale_slider],'By resizing the style image before extracting style features, we can control the types of artistic features that are transfered from the style image') 
                       
    def createMenuBar(self):
        mainMenu = QtWidgets.QMenuBar(self)
        
        exportSettingsAction = QtWidgets.QAction("Export Settings",self)
        exportSettingsAction.triggered.connect(lambda: print("Test"))

        importSettingsAction = QtWidgets.QAction("Import Settings",self)
        importSettingsAction.triggered.connect(lambda: print("Test"))
        
        editMenu = mainMenu.addMenu("Presets")
        editMenu.addAction(exportSettingsAction)     
        editMenu.addAction(importSettingsAction)     

        helpAction = QtWidgets.QAction("Help",self)
        helpAction.triggered.connect(lambda: webbrowser.open('https://github.com/SweckEUW/Autodesk-Maya-AI-Image-Edit-Toolkit'))

        helpAction_styleTransfer = QtWidgets.QAction("Help Style Transfer",self)
        helpAction_styleTransfer.triggered.connect(lambda: webbrowser.open('https://github.com/ProGamerGov/neural-style-pt'))

        helpAction_superResolution = QtWidgets.QAction("Help Image Super-Resolution",self)
        helpAction_superResolution.triggered.connect(lambda: webbrowser.open('https://github.com/krasserm/super-resolution'))

        helpAction_neuralDream = QtWidgets.QAction("Help Neural Dream",self)
        helpAction_neuralDream.triggered.connect(lambda: webbrowser.open('https://github.com/ProGamerGov/neural-dream'))

        presetsMenu = mainMenu.addMenu("Help")
        presetsMenu.addAction(helpAction)   
        presetsMenu.addAction(helpAction_styleTransfer)   
        presetsMenu.addAction(helpAction_superResolution)   
        presetsMenu.addAction(helpAction_neuralDream)  

class OptionWindowStyleImageSelection(QtWidgets.QWidget):
    def __init__(self):
        super(OptionWindowStyleImageSelection, self).__init__()

        self.sliders = []
        self.lineedits = []
        self.optionsJson = getOptions()

        self.create_layouts()
        self.create_widgets()

    def create_layouts(self):
        self.style_widgets_layout = QtWidgets.QVBoxLayout()

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.style_widgets_layout)

    def create_widgets(self):
        style_images = self.optionsJson["style_transfer"]["style_images"].split(",")
        style_blend_weights = self.optionsJson["style_transfer"]["style_blend_weights"].split(",")
        
        for i in range(len(style_images)):
            style_image_widget = self.create_style_image_widget(style_images[i],style_blend_weights[i])
            self.style_widgets_layout.addLayout(style_image_widget)

        # Add and Remove Buttons
        self.button_container = QtWidgets.QHBoxLayout()

        # Add
        add_style_image_button = QtWidgets.QPushButton()
        add_style_image_button.setIcon(QtGui.QIcon(QtGui.QPixmap("./Plugin/media/icons/add.svg")))
        add_style_image_button.setToolTip('Add Style Image')
        add_style_image_button.clicked.connect(self.add_style_image_widget)
        self.button_container.addWidget(add_style_image_button)

        # Remove
        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setIcon(QtGui.QIcon(QtGui.QPixmap("./Plugin/media/icons/delete.svg")))
        self.delete_button.setToolTip('Delete First Style Image')
        self.delete_button.clicked.connect(lambda: self.remove_style_image_widget())
        if len(style_images) != 1:
            self.button_container.addWidget(self.delete_button)

        self.main_layout.addLayout(self.button_container)

    def create_style_image_widget(self,path,weight):
        if weight == "None":
            weight = "2"

        # Path
        path_label = QtWidgets.QLabel("Path")
        path_label.setToolTip('Path to Style Image')
        path_label.setMinimumWidth(45)

        output_path_lineedit = QtWidgets.QLineEdit(path)
        output_path_lineedit.editingFinished.connect(self.update_style_images)
        self.lineedits.append(output_path_lineedit)
        select_file_button = QtWidgets.QPushButton()
        select_file_button.setToolTip('Select path to Style Image')
        select_file_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        select_file_button.clicked.connect(lambda: self.select_style_image(output_path_lineedit))

        hbox_path = QtWidgets.QHBoxLayout()
        hbox_path.addWidget(path_label)
        hbox_path.addWidget(output_path_lineedit)
        hbox_path.addWidget(select_file_button)

        # Weight
        weight_label = QtWidgets.QLabel("Weight")
        weight_label.setMinimumWidth(45) 
        weight_label.setToolTip('The weight for blending the style of multiple style images')

        weight_slider_label = QtWidgets.QLabel(weight)
        weight_slider_label.setToolTip('The weight for blending the style of multiple style images')
        weight_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        weight_slider.setMinimum(1)
        weight_slider.setMaximum(10)
        weight_slider.setValue(int(weight))
        weight_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        weight_slider.setToolTip('The weight for blending the style of multiple style images')
        weight_slider.valueChanged.connect(lambda: (
            self.update_style_images(),
            weight_slider_label.setText(str(weight_slider.value()))
        ))
        self.sliders.append(weight_slider)

        hbox_weight = QtWidgets.QHBoxLayout()
        hbox_weight.addWidget(weight_label)
        hbox_weight.addWidget(weight_slider_label)
        hbox_weight.addWidget(weight_slider)
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(hbox_path)
        main_layout.addLayout(hbox_weight)
        return main_layout

    def add_style_image_widget(self):
        # Add Widget
        path = os.path.join(os.path.split(cmds.file(q=True, loc=True))[0], "Plugin/media/styles/style7.jpg")
        new_style_image = self.create_style_image_widget(path,"5")
        self.style_widgets_layout.addLayout(new_style_image)

        # Update options.json
        self.update_style_images()

        # Add delete button 
        if len(self.lineedits) == 2:
            self.button_container.addWidget(self.delete_button)

    def remove_style_image_widget(self):
        # Remove widget
        self.style_widgets_layout.takeAt(0)

        # Update options.json
        self.lineedits.pop(0)
        self.sliders.pop(0)
        self.update_style_images()

        # Remove delete button 
        if len(self.lineedits) == 1:
            self.button_container.removeWidget(self.delete_button)

    def update_style_images(self):
        style_images = ""
        style_blend_weights = ""

        for i in range(len(self.lineedits)):
            if i == 0:
                style_images += self.lineedits[i].text()
            else:
                style_images += "," + self.lineedits[i].text()
        
        if len(self.lineedits) == 1:
            style_blend_weights = "None"
        else:
            for i in range(len(self.lineedits)):
                if i == 0:
                    style_blend_weights += str(self.sliders[i].value())
                else:
                    style_blend_weights += "," + str(self.sliders[i].value())

        updateOptions("style_transfer","style_blend_weights",style_blend_weights)
        updateOptions("style_transfer","style_images",style_images)

    def select_style_image(self,widget):
        starting_path = os.path.join(os.path.split(cmds.file(q=True, loc=True))[0], "Plugin/media/styles/")
        output_path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", starting_path, "Images (*.jpg *.jpeg *png *)")
        if output_path:
            widget.setText(output_path)
            self.update_style_images()

if __name__ == "__main__":
    unload_packages() 

    if(option_window):
        option_window.close()
        option_window.deleteLater()
    
    option_window = OptionWindow()
    option_window.show()
