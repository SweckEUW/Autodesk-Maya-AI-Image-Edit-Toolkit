from PySide2 import QtGui, QtWidgets, QtTest, QtCore
import unittest

from Plugin.scripts.optionWindow import OptionWindow
from Plugin.scripts.optionWindow_utils import getOptions
from Plugin.scripts.unload_packages import unload_packages


_instance = None
class UsesQApplication(unittest.TestCase):

    qapplication = True

    def setUp(self):
        super(UsesQApplication, self).setUp()
        global _instance
        if _instance is None:
            _instance = QtGui.QApplication([])

        self.app = _instance

    def tearDown(self):
        del self.app
        super(UsesQApplication, self).tearDown()



optionWindow = OptionWindow()

class Testing(unittest.TestCase):

    def test_Option_Changed_Checkbox(self):                
        checkBox = optionWindow.findChild(QtWidgets.QCheckBox,"keepcolor_checkbox")
        checkBox.click()
        self.assertEqual(checkBox.isChecked(), (getOptions()["style_transfer"]["original_colors"] == 'True'))
 
    def test_Option_Changed_Slider(self):
        slider = optionWindow.findChild(QtWidgets.QSlider,"itterations_slider")
        slider.setValue(100)
        self.assertEqual(slider.value(), (getOptions()["style_transfer"]["itterations"]))

       
if __name__ == "__main__":
    unload_packages()

    # option_window = Testing()
    # option_window.test_Option_Changed_Slider()
    unittest.main(argv=["ignored","-v"], defaultTest="Testing", verbosity=2, exit=False)
