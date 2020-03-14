import sys
import libpypack
import pandas as pd
import pyqtgraph as pg

from libpypack.locations import map_locations
from libpypack.visualization import generate_maps
from libpypack.visualization import choropleth
from libpypack.visualization import heatmap

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction,
                             QLineEdit, QLabel, QPushButton, QComboBox,
                             QFileDialog, QGridLayout, QWidget)

class GraphWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyPACK GUI")
        self.resize( 800, 600 )

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class PYPACK_GUI(QMainWindow):

    def __init__(self):
        print('In GUI')
        super().__init__()
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
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

    def openShapeFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.shapeLine.setText(fileName)
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
        loc_df = map_locations.locations_df(csv_file)
        loc_gdf = generate_maps.get_loc_gdf(loc_df)
        text = str(self.typeBox.currentText())
        if(text == "Heatmap"):
            heatmap.heatmap(loc_gdf)
        elif(text == "Choropleth"):
            gdf = choropleth.choropleth_map(loc_gdf, shp_path=str(self.shapeLine.currentText()))
        elif(text == "Overlay Locations"):
            gdf = generate_maps.generate_overlay_gdf(loc_df, filename=str(self.shapeLine.currentText()))
        self.mapWindow = GraphWindow()
        sc = MplCanvas(self.mapWindow, width=5, height=4, dpi=100)
        gdf.plot(ax=sc.axes)
        self.mapWindow.setCentralWidget(sc)
        self.mapWindow.show()
        # self.show()

    def initUI(self):
        self.grid = QGridLayout(self.centralwidget)
        self.grid.setSpacing(15)

        # Input Label/Line
        self.inputLabel = QLabel(self)
        self.inputLabel.setText('Input File Path:')
        self.inputLine = QLineEdit(self)
        # Header Dropdown Menu
        self.comboBox = QComboBox(self)

        # Output Label/Line
        self.outputLabel = QLabel(self)
        self.outputLabel.setText('Output File Path:')
        self.outputLine = QLineEdit(self)

        # Output Label/Line
        self.shapeLabel = QLabel(self)
        self.shapeLabel.setText('Shape File Path:')
        self.shapeLine = QLineEdit(self)

        # Map Types
        self.graphWidget = pg.PlotWidget()

        # Browse for Input File Path
        open_file = QPushButton('Browse for Input File', self)
        open_file.clicked.connect(lambda: self.openInputFileNameDialog())

        # Browse for ShapeFile Path
        shape_file = QPushButton('Browse for Shape File', self)
        shape_file.clicked.connect(lambda: self.openShapeFileNameDialog())

        # Browse for Output File Path
        output_file = QPushButton('Browse for Output File', self)
        output_file.clicked.connect(lambda: self.openOutputFileNameDialog())

        # Parse Locations button
        parse_locs = QPushButton('Parse Locations', self)
        parse_locs.clicked.connect(lambda: self.clickMethod(self.inputLine.text(), self.outputLine.text()))
        # Gen-Map Button
        gen_maps = QPushButton('Generate Map', self)
        gen_maps.clicked.connect(lambda: self.overlay(self.inputLine.text()))

        # List of Map Types PyPACK Supports
        map_types = [
                self.tr('Heatmap'),
                self.tr('Choropleth'),
                self.tr('Overlay Locations'),
                ]
        # Map Drop-Down Box
        self.typeBox = QComboBox(self)
        self.typeBox.addItems(map_types)

        # Line Edits
        self.grid.addWidget(self.inputLabel, 1, 0)
        self.grid.addWidget(self.inputLine, 1, 1)
        self.grid.addWidget(self.comboBox, 1, 2)
        self.grid.addWidget(self.outputLabel, 3, 0)
        self.grid.addWidget(self.outputLine, 3, 1)
        self.grid.addWidget(self.shapeLabel, 5, 0)
        self.grid.addWidget(self.shapeLine, 5, 1)

        # Browsers
        self.grid.addWidget(open_file, 2, 1)
        self.grid.addWidget(output_file, 4, 1)
        self.grid.addWidget(shape_file, 6, 1)

        # Buttons
        self.grid.addWidget(parse_locs, 7, 0)
        self.grid.addWidget(self.typeBox, 7, 1)
        self.grid.addWidget(gen_maps, 7, 2)

        # # Quit Button
        # quit_app = QPushButton('Quit Application', self)
        # quit_app.clicked.connect(QApplication.quit)

        self.comboBox.activated[str].connect(self.onActivated)
        self.typeBox.activated[str].connect(self.onActivated)

        menubar = self.menuBar()
        locMenu = menubar.addMenu('Locations')
        visMenu = menubar.addMenu('Visualization')

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

        # self.setGeometry(500, 500, 500, 400)
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = PYPACK_GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
