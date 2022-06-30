from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from neural_style import neural_style
from collapsible_widget import CollapsibleWidget

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

    def create_widgets(self):
        self.collapsible_a = CollapsibleWidget("Style Transfer")
        for i in range(6):
            self.collapsible_a.add_widget(QtWidgets.QPushButton("Button {0}".format(i)))
            
        self.collapsible_b = CollapsibleWidget("Upscale")
        for i in range(6):
            self.collapsible_b.add_widget(QtWidgets.QPushButton("Button {0}".format(i)))
            
        self.style_transfer_button = QtWidgets.QPushButton("Style Transfer")
        self.style_transfer_button.clicked.connect(self.style_transfer)
        
        self.upscale_button = QtWidgets.QPushButton("Upscale")
        self.upscale_button.clicked.connect(self.upscale)

        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")


    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(4)
        form_layout.addRow(self.style_transfer_button)
        form_layout.addRow(self.upscale_button)
        form_layout.addRow(self.collapsible_a)
        form_layout.addRow(self.collapsible_b)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        # main_layout.addLayout(button_layout)
        
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_layout)
        
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
       
        scrollArea.setObjectName("ai_scrollArea");
        scrollArea.setStyleSheet('#ai_scrollArea { border: none; }')
       
        scrollArea.setWidget(main_widget)
        
        main_layout2 = QtWidgets.QVBoxLayout(self)
        main_layout2.setContentsMargins(0,0,0,0)
        main_layout2.addWidget(scrollArea)

    def style_transfer(self):
        neural_style.main()
       
    def upscale(self):
        pass
    # def upscale_image(self):
    
    #     def load_image(image_path):
    #         hr_image = tf.image.decode_image(tf.io.read_file(image_path))
    #         if hr_image.shape[-1] == 4:
    #             hr_image = hr_image[...,:-1]
    #         hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
    #         hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
    #         hr_image = tf.cast(hr_image, tf.float32)
    #         return tf.expand_dims(hr_image, 0)
        
    #     #Save current rendering to disk
    #     editor = 'renderView'
    #     cmds.renderWindowEditor(editor, e=True, writeImage=self.media_path+"rendering.jpg")
        
    #     #load neural net
    #     model = hub.load("https://tfhub.dev/captain-pool/esrgan-tf2/1")
        
    #     if os.path.exists(self.media_path+"output.jpg"):
    #         low_resolution_image = load_image(self.media_path+"output.jpg")
    #     else:
    #         low_resolution_image = load_image(self.media_path+"rendering.jpg")

    #     super_resolution_image = model(low_resolution_image)

    #     image = tf.squeeze(tf.cast(tf.clip_by_value(super_resolution_image, 0, 255), tf.uint8))
    #     image = Image.fromarray(image.numpy())
    #     image.save(self.media_path+"output.jpg")    

    #     cmds.image("test123",image=self.media_path+"output.jpg", edit=True)

if __name__ == "__main__":
    d = OptionWindow()
    d.show()
