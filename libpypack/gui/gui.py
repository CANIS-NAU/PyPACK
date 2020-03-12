import sys
import libpypack
import pandas as pd
import pyqtgraph as pg

from libpypack.locations import map_locations
from libpypack.visualization import generate_maps
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction,
                             QLineEdit, QLabel, QPushButton, QComboBox, QFileDialog)

class GraphWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plot")

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class PYPACK_GUI(QMainWindow):

    def __init__(self):
        print('In GUI')
        super().__init__()
        self.initUI()

    def create_directory(self):
        textEdit = QTextEdit()
        textEdit.setPlainText("Enter the file or directory you want to parse")

    def get_headers(self, csv_file):
        try:
            self.comboBox.addItems(list(pd.read_csv(csv_file, nrows=1, sep='\t').columns.values))
        except:
            self.comboBox.addItem("No File Selected")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.inputLine.setText(fileName)
            return fileName
        else:
            return None

    def openInputFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.inputLine.setText(fileName)
            try:
                self.comboBox.addItems(list(pd.read_csv(fileName, nrows=1, sep='\t').columns.values))
            except:
                self.comboBox.addItem("No File Selected")
            return fileName
        else:
            return None

    def openOutputFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.outputLine.setText(fileName)
            return fileName
        else:
            return None

    def clickMethod(self, csv_file, output_dir):
        loc_df = map_locations.locations_df(csv_file)
        map_locations.write_csv(output_dir, 'example.csv', loc_df)

    def onActivated(self):
        print('Item Selected')

    # Generate the Map
    def overlay(self, csv_file):
        df = pd.read_csv(csv_file, sep='\t')
        loc_df = map_locations.locations_df(csv_file)
        self.mapWindow = GraphWindow()
        sc = MplCanvas(self.mapWindow, width=5, height=4, dpi=100)
        gdf = generate_maps.generate_overlay_gdf(loc_df)
        gdf.plot(ax=sc.axes)
        self.mapWindow.setCentralWidget(sc)
        self.mapWindow.show()
        # self.show()

    def initUI(self):

        # Input Label/Line
        self.inputLabel = QLabel(self)
        self.inputLabel.setText('Input File Path:')
        self.inputLine = QLineEdit(self)

        # Header Dropdown Menu
        self.comboBox = QComboBox(self)
        self.comboBox.move(350, 20)

        # Output Label/Line
        self.outputLabel = QLabel(self)
        self.outputLabel.setText('Output File Path:')
        self.outputLine = QLineEdit(self)

        # Input Label/Line Adjustments
        self.inputLine.move(125, 20)
        self.inputLine.resize(200, 32)
        self.inputLabel.move(20, 20)

        # Output Label/Line Adjustments
        self.outputLine.move(125, 100)
        self.outputLine.resize(200, 32)
        self.outputLabel.move(20, 100)

        # Map Types
        self.graphWidget = pg.PlotWidget()

        # Browse for Input File Path
        open_file = QPushButton('Browse for Input File', self)
        open_file.clicked.connect(lambda: self.openInputFileNameDialog())
        open_file.resize(150, 30)
        open_file.move(120, 60)

        # Browse for Output File Path
        output_file = QPushButton('Browse for Output File', self)
        output_file.clicked.connect(lambda: self.openOutputFileNameDialog())
        output_file.resize(165, 30)
        output_file.move(120, 140)

        # Parse Locations button
        parse_locs = QPushButton('Parse Locations', self)
        parse_locs.clicked.connect(lambda: self.clickMethod(self.inputLine.text(), self.outputLine.text()))
        parse_locs.resize(125,30)
        parse_locs.move(20, 180)

        # load_headers = QPushButton('Load Headers', self)
        # load_headers.clicked.connect(lambda: self.get_headers(self.inputLine.text()))
        # load_headers.resize(125,30)
        # load_headers.move(150, 180)

        # List of Map Types PyPACK Supports
        map_types = [
                self.tr('Heatmap'),
                self.tr('Choropleth'),
                self.tr('Overlay Locations'),
                ]
        # Map Drop-Down Box
        self.typeBox = QComboBox(self)
        self.typeBox.move(150, 210)
        self.typeBox.resize(100,30)
        self.typeBox.addItems(map_types)

        # Gen-Map Button
        gen_maps = QPushButton('Generate Map', self)
        gen_maps.clicked.connect(lambda: self.overlay(self.inputLine.text()))
        gen_maps.resize(125,30)
        gen_maps.move(150, 180)

        # Quit Button
        quit_app = QPushButton('Quit Application', self)
        quit_app.clicked.connect(QApplication.quit)
        quit_app.resize(250,50)
        quit_app.move(120, 300)

        self.comboBox.activated[str].connect(self.onActivated)
        self.typeBox.activated[str].connect(self.onActivated)

        menubar = self.menuBar()
        locMenu = menubar.addMenu('Locations')
        visMenu = menubar.addMenu('Visualization')

        # self.centralwidget = QtWidgets.QWidget(self)
        # self.centralwidget.setObjectName("centralwidget")
        # self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit.setObjectName("lineEdit")
        # self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setObjectName("pushButton")
        # self.verticalLayout = QtWidgets.QVBoxLayout()
        # self.verticalLayout.setObjectName("verticalLayout")
        # self.tableView = QtWidgets.QTableView(self.centralwidget)
        # self.tableView.setObjectName("tableView")
        # self.verticalLayout.addWidget(self.tableView)

        # layout = QGridLayout()
        # lineEdit = QLineEdit()
        # self.addWidget(lineEdit)

        self.impMenu = QMenu('Parse Locations')
        self.impAct = QAction('Run Mordecai')
        self.impMenu.addAction(self.impAct)
        self.impAct.triggered.connect(lambda: self.clickMethod(self.inputLine.text(), self.outputLine.text()))

        self.genMenu = QMenu('Generate Visuals')
        self.heatAct = QAction('Heatmap')
        self.choroAct = QAction('Choropleth')

        self.genMenu.addAction(self.choroAct)
        self.genMenu.addAction(self.heatAct)

        # self.choroAct.triggered.connect(self.print_something)
        # self.heatAct.triggered.connect(self.print_something)

        # Add the Menus
        locMenu.addMenu(self.impMenu)
        visMenu.addMenu(self.genMenu)

        self.setGeometry(500, 500, 500, 400)
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = PYPACK_GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
