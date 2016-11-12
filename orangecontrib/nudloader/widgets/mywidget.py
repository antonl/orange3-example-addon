from qtpy import QtGui, QtCore, QtWidgets
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui, settings

from qtpy.QtWidgets import QSizePolicy as Policy
from qtpy.QtWidgets import QStyle

import pathlib
import os.path
import sys

def parse_datafolder_name(path):
    path = pathlib.Path(path)
    
    assert path.is_dir(), "path must be a directory"
    
    print(path.name)        
    

class DataLoader(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "Load Data"
    icon = "icons/mywidget.svg"
    want_main_area = False
    
    mycheckbox = settings.Setting(True)
    autoload = settings.Setting(False)
    

    def __init__(self):
        super().__init__()
        
        self.data = None
        self.loaded_path = pathlib.Path()        
        
        box = gui.hBox(self.controlArea, 'Folder')
        self.path_lb = gui.widgetLabel(box, "No folder selected")
        
        file_button = gui.button(
            box, self, '...', callback=self.browse_file, autoDefault=False)
        file_button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        file_button.setSizePolicy(Policy.Maximum, Policy.Fixed)
        
        box = gui.vBox(self.controlArea, "Info")
        self.info = gui.widgetLabel(box, 'No data loaded.')
        self.warnings = gui.widgetLabel(box, '')
        
        box = gui.vBox(self.controlArea, "Settings") 
        gui.checkBox(box, self, "mycheckbox", "My checkbox?")
    
        autoloadbox = gui.hBox(box)
        self.autoload_cb = gui.checkBox(autoloadbox, self, "autoload", "Automatically load data",\
            callback=self._set_autoload)
        self.load_btn = gui.button(autoloadbox, self, "Load", callback=self.load_data)
        self.load_btn.setSizePolicy(Policy.Minimum, Policy.Fixed)
        self._set_autoload()        
    
    def _set_autoload(self):
        self.autoload = self.autoload_cb.isChecked()
        
        if self.autoload:
            self.load_btn.setEnabled(False)
        else:
            self.load_btn.setEnabled(True)   

    def _update_info(self):
        paths = sorted(self.loaded_path.glob('*.spe'))
        
        if len(paths) < 1:
            self.error('This is probably not a data folder.')
            return
        
        print(paths[-1])
    
    def load_data(self):
        pass
    
    def browse_file(self):
        start_file = os.path.expanduser("~/")
        
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Ogilvie lab data folders', start_file)
        if not path:
            return
        self.loaded_path = pathlib.Path(path)
        self.path_lb.setText(str(self.loaded_path))
        
        self._update_info()                
        
        if self.autoload:
            self.load_data()

def main(argv=sys.argv):
    app = QtCore.QApplication(list(argv))
    
    ow = DataLoader()
    ow.show()
    ow.raise_()

    '''    
    dataset = Orange.data.Table(filename)
    ow.set_data(dataset)
    ow.handleNewSignals()
    app.exec_()
    ow.set_data(None)
    ow.handleNewSignals()
    '''
    app.exec_()
    return 0

if __name__=="__main__":
    sys.exit(main())
