# from girafe.gui.cicada_main_window import GirafeMainWindow
from girafe.gui.girafe_initial_config_window import InitialConfigWindow
from girafe.gui.girafe_config_handler import ConfigHandler
import sys
import platform
from qtpy.QtWidgets import *
import os
import matplotlib
matplotlib.use('Agg')  # For general use cannot use plt.show() to debug but no pb with plot out of the main thread
# matplotlib.use('Qt5Agg')

app = QApplication(sys.argv)

# set the environment variable to use a specific wrapper
# it can be set to PyQt, PyQt5, PySide or PySide2 (not implemented yet)
# os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'

# dark_style_style_sheet = qdarkstyle.load_stylesheet_from_environment(is_pyqtgraph=True)
# from package qdarkstyle, modified css
my_path = os.path.abspath(os.path.dirname(__file__))
if platform.system() == "Windows":
	to_insert = os.path.join(my_path, "gui/icons/")
	to_insert = to_insert.replace("\\", "/")
else:
	to_insert = os.path.join(my_path, "gui/icons/")
	
file_name = os.path.join(my_path, "gui/girafe_qdarkstyle.css")
# with open(file_name, "w", encoding='UTF-8') as file:
#     file.write(dark_style_style_sheet)
with open(file_name, "r", encoding='UTF-8') as file:
	dark_style_cicada_style_sheet = file.read()

dark_style_cicada_style_sheet = dark_style_cicada_style_sheet.replace("icons/", to_insert)
app.setStyleSheet(dark_style_cicada_style_sheet)

config_handler = ConfigHandler()

# girafe_first_window = GirafeMainWindow(config_handler=config_handler)
girafe_first_window = InitialConfigWindow(config_handler=config_handler)

# putting the window at the center of the screen
# screenGeometry is an instance of Qrect
screenGeometry = QApplication.desktop().screenGeometry()
x = int((screenGeometry.width() - girafe_first_window.width()) / 2)
y = int((screenGeometry.height() - girafe_first_window.height()) / 2)


girafe_first_window.move(x, y)
girafe_first_window.show()

sys.exit(app.exec_())
