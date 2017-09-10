import sys
import os

from PySide.QtGui import *
from PySide.QtCore import *

#custom module for formatting filenames
from collapse_padding import formatFilenames

#https://srinikom.github.io/pyside-docs/index.html

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        #create widgets
        self.openButton = QPushButton("Open Files")
        self.displayButton = QPushButton("Display Selected Files")
        self.itemlist = QListWidget(self)
        
        self.window().setWindowTitle("File Listing")
        self.window().setWindowIcon(QIcon("d20_plain_icon_ready.png"))
        
        #create layout/add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.openButton)
        layout.addWidget(self.itemlist)
        layout.addWidget(self.displayButton)
        
        self.setLayout(layout)
        self.openButton.clicked.connect(self.fileOpen)
        self.displayButton.clicked.connect(self.msgboxFiles)
    
        #create attribute to hold currently selected directory files
        self.currentfiles = []
        
        #enable user to select multiple files in the list widget
        self.itemlist.setSelectionMode(QAbstractItemView.MultiSelection)

    
    def fileOpen(self):
        #open the explorer dialog to allow user to browse computer
        #specify starting directory
        basedir = "C:"
        dialog = QFileDialog(self)
        dialog.setDirectory(basedir)

        dialog.setOption(QFileDialog.ShowDirsOnly,True)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.open()
        
        #run when the user presses OK
        if dialog.exec_():
            foldername = dialog.selectedFiles()

            # now look through the directory and get the filenames, save as list
            filenames = os.listdir(str(foldername[0]))
            self.currentfiles = filenames
            
            #collapse sequential files
            format_f = formatFilenames(filenames)
            self.itemlist.clear()
            
            #populate the list widget with files in the folder
            self.itemlist.addItems(format_f)
            
        #for f in self.currentfiles:
        #    print f
        
    def msgboxFiles(self):
        #message box to display the actual files the user selected
        #self.currentfiles has the full list of files, so iterate to get actual filenames
        msgbox = QMessageBox()
        msgbox.setText("    Selected Files     ")
        
        report = ""
        for item in self.itemlist.selectedItems():
            if "%" not in item.text():
                report+=item.text() + "\n"
            else:
                pattern = item.text().split("%")
                for file in self.currentfiles:
                    if pattern[0] in file:
                        report+=file + "\n"
        msgbox.setInformativeText(report)
        msgbox.exec_()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = Form()
    frame.show()
app.exec_()
