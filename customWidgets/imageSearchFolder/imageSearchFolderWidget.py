
from PyQt5.QtWidgets import (
    QWidget, QApplication,QDialogButtonBox, QDialog, QHeaderView,
    QAction, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QScrollBar, QTabWidget, QSizePolicy, QDockWidget
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QCursor
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize,pyqtSlot
from os import listdir
from os.path import isfile, join

from customWidgets.imageSearchFolder.imageSearchFolderWidget_ui import Ui_Form


class ImageSearchFolderWidget(QWidget):
    returned = pyqtSignal(str)
    changed = pyqtSignal()
    sendImageNameandPath = pyqtSignal(object, object)


    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.make_signal_slot_connections()
        #self.setWindowState(Qt.WindowMaximized)
    
    def initialize_table_configurations(self):
        self.ui.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.tableWidget.setHorizontalScrollBar(QScrollBar(self))
        self.ui.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.tableWidget.setVerticalScrollBar(QScrollBar(self))
        
        
        self.ui.tableWidget.setMouseTracking(True)
    
    def make_signal_slot_connections(self):
        self.ui.pushButton_open_folder.clicked.connect(self.open_test_folder_slot)
        #self.ui.tableWidget.cellClicked[int, int].connect(self.table_widget_cell_activated)
        self.ui.tableWidget.cellClicked.connect(self.table_widget_cell_activated)
    
    @pyqtSlot()
    def open_test_folder_slot(self):
        self.data_folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.ui.lineEdit_folder_path.setText(self.data_folder_path)

        if not self.data_folder_path:
            QMessageBox.about(self, "Warning", "file path is empty")
            return

        image_files = self.get_image_files(self.data_folder_path)
        self.create_table_widget(image_files)
        

    def get_image_files(self, file_path):
        if file_path is not None:
            onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]
            return onlyfiles
        return None

    def create_table_widget(self, image_files):

        self.ui.tableWidget.setRowCount(len(image_files))
        self.ui.tableWidget.setColumnCount(1)
        

        for i in range(len(image_files)):
            item = QTableWidgetItem(image_files[i])
            item.setToolTip(image_files[i])
            self.ui.tableWidget.setItem(i, 0, item)

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.initialize_table_configurations()

    @pyqtSlot(int,int)
    def table_widget_cell_activated(self, row, column):

        data_item = self.ui.tableWidget.item(row, column).text()

        #test_path =  os.path.join(self.data_folder_path, data_item)

        data_path = self.data_folder_path + "/" + data_item
        self.sendImageNameandPath.emit(data_path, data_item)
