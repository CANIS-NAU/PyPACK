import sys
import libpypack
import pandas as pd
import pyqtgraph as pg

from libpypack.locations import map_locations
from libpypack.locations import webpage_locations
from libpypack.visualization import generate_maps
from libpypack.visualization import choropleth
from libpypack.visualization import heatmap
from libpypack.locations.start_docker import run_docker
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
        super().__init__()
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        # Run docker
        run_docker()
        self.initUI()

    def create_directory(self):
        textEdit = QTextEdit()
        textEdit.setPlainText("Enter the file or directory you want to parse")

    def get_headers(self, csv_file, seperator):
        try:
            self.comboBox.addItems(list(pd.read_csv(csv_file, nrows=0, sep=seperator).columns))
        except:
            self.comboBox.addItem("No File Selected")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.inputLine.setText(fileName)
            return fileName
        else:
            return None

    def openInputFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.csv)", options=options)
        if fileName:
            self.inputLine.setText(fileName)
            if(str(self.outFileType.currentText()) == 'CSV'):
                seperator = ","
            else:
                seperator = "\t"
            self.get_headers(fileName, seperator)
            return fileName
        else:
            return None

    def openOutputFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        output_dir = QFileDialog.getExistingDirectory(self, 'Browse for Output Directory', options=options)
        if output_dir:
            self.outputLine.setText(output_dir)
            return output_dir
        else:
            return None

    def openShapeFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.csv)", options=options)
        if fileName:
            self.shapeLine.setText(fileName)
            return fileName
        else:
            return None

    def clickMethod(self, csv_file, output_dir, filename=None):
        loc_df = map_locations.locations_df(csv_file, sep=seperator, output_dir=str(self.outputLine.text()), \
                                            df_column=str(self.comboBox.currentText()))
        return loc_df

    def scrape_websites(self, csv_file):
        if(str(self.outFileType.currentText()) == 'CSV'):
            seperator = ","
        else:
            seperator = "\t"
        web_df = webpage_locations.extract_webpage_locations(csv_file, sep=seperator, output_dir=str(self.outputLine.text()), \
                                            column_name=str(self.comboBox.currentText()))
        mapped_df = webpage_locations.map_web_locations(web_df, sep=seperator, output_dir=str(self.outputLine.text()))

        return web_df

    # Generate the Map
    def generate_map(self, csv_file):
        if(str(self.outFileType.currentText()) == 'CSV'):
            seperator = ","
        else:
            seperator = "\t"
        loc_df = pd.read_csv(csv_file, sep=seperator)
        loc_gdf = generate_maps.get_loc_gdf(loc_df, column_name=str(self.comboBox.currentText()))
        text = str(self.typeBox.currentText())
        if(text == "Heatmap"):
            hmap = heatmap.heatmap(loc_gdf, output_dir=str(self.outputLine.text()))
        elif(text == "Choropleth"):
            gdf = choropleth.choropleth_map(loc_gdf, shp_path=str(self.shapeLine.text()))
            plot = choropleth.plot_map(gdf, output_dir=str(self.outputLine.text()))
        elif(text == "Overlay Locations Map"):
            gdf, loc_gdf = generate_maps.generate_overlay_gdf(loc_df, filename=str(self.shapeLine.text()))
            plot = generate_maps.plot_gdf(gdf, loc_gdf, filepath=str(self.outputLine.text()))

    # Generate the Map
    def overlay(self, csv_file):
        if(str(self.outFileType.currentText()) == 'CSV'):
            seperator = ","
        else:
            seperator = "\t"
        loc_df = map_locations.locations_df(csv_file, sep=seperator, output_dir=str(self.outputLine.text()), \
                                            df_column=str(self.comboBox.currentText()))
        loc_gdf = generate_maps.get_loc_gdf(loc_df)
        text = str(self.typeBox.currentText())
        if(text == "Heatmap"):
            hmap = heatmap.heatmap(loc_gdf, output_dir=str(self.outputLine.text()))
        elif(text == "Choropleth"):
            gdf = choropleth.choropleth_map(loc_gdf, shp_path=str(self.shapeLine.text()))
            plot = choropleth.plot_map(gdf, output_dir=str(self.outputLine.text()))
        elif(text == "Overlay Locations Map"):
            gdf, loc_gdf = generate_maps.generate_overlay_gdf(loc_df, filename=str(self.shapeLine.text()))
            plot = generate_maps.plot_gdf(gdf, loc_gdf, filepath=str(self.outputLine.text()))

    def initUI(self):
        self.grid = QGridLayout(self.centralwidget)
        self.grid.setSpacing(15)

        # Input Label/Line
        self.inputLabel = QLabel(self)
        self.inputLabel.setText('Input File Path:')
        self.inputLine = QLineEdit(self)
        # Header Dropdown Menu
        file_types = [
                self.tr('None Selected'),
                self.tr('CSV'),
                self.tr('TSV'),
                ]

        self.outFileLabel = QLabel(self)
        self.outFileLabel.setText('Output File Type:')
        self.outFileType = QComboBox(self)
        self.outFileType.addItems(file_types)

        self.comboBoxLabel = QLabel(self)
        self.comboBoxLabel.setText('Column to Analyze:')
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
        output_file = QPushButton('Browse for Output Directory', self)
        output_file.clicked.connect(lambda: self.openOutputFileNameDialog())

        # Parse Locations button
        parse_locs = QPushButton('Parse Locations Only', self)
        parse_locs.clicked.connect(lambda: self.clickMethod(self.inputLine.text(), self.outputLine.text()))
        # Gen-Map Button
        gen_maps = QPushButton('Generate Map and Parse Locations', self)
        gen_maps.clicked.connect(lambda: self.overlay(self.inputLine.text()))

        # Websites Location
        websites = QPushButton('Scrape Websites', self)
        websites.clicked.connect(lambda: self.scrape_websites(self.inputLine.text()))

        # Websites Location
        gen_map = QPushButton('Generate Map Only', self)
        gen_map.clicked.connect(lambda: self.generate_map(self.inputLine.text()))

        # List of Map Types PyPACK Supports
        map_types = [
                self.tr('Heatmap'),
                self.tr('Choropleth'),
                self.tr('Overlay Locations Map'),
                ]
        # Map Drop-Down Box
        self.mapTypeLabel = QLabel(self)
        self.mapTypeLabel.setText('Map Type:')
        self.typeBox = QComboBox(self)
        self.typeBox.addItems(map_types)

        # Line Edits
        self.grid.addWidget(self.inputLabel, 1, 0)
        self.grid.addWidget(self.inputLine, 1, 1)
        self.grid.addWidget(self.outFileLabel, 1, 2)
        self.grid.addWidget(self.outFileType, 1, 3)
        self.grid.addWidget(self.comboBoxLabel, 2, 2)
        self.grid.addWidget(self.comboBox, 2, 3)
        self.grid.addWidget(self.outputLabel, 3, 0)
        self.grid.addWidget(self.outputLine, 3, 1)
        self.grid.addWidget(self.shapeLabel, 5, 0)
        self.grid.addWidget(self.shapeLine, 5, 1)

        # Browsers
        self.grid.addWidget(open_file, 2, 1)
        self.grid.addWidget(output_file, 4, 1)
        self.grid.addWidget(shape_file, 6, 1)

        # Buttons
        self.grid.addWidget(parse_locs, 8, 2)
        self.grid.addWidget(self.mapTypeLabel, 7, 0)
        self.grid.addWidget(self.typeBox, 7, 1)
        self.grid.addWidget(gen_maps, 7, 2)
        self.grid.addWidget(websites, 7, 3)
        self.grid.addWidget(gen_map, 8, 3)

        # self.setGeometry(500, 500, 500, 400)
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = PYPACK_GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
