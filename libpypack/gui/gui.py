import pandas as pd
import pyqtgraph as pg
import libpypack

from libpypack.locations.start_docker import run_docker
from libpypack.locations import map_locations
from libpypack.locations import webpage_locations
from libpypack.visualization import generate_maps
from libpypack.visualization import choropleth
from libpypack.visualization import heatmap

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction,
                             QLineEdit, QLabel, QPushButton, QComboBox,
                             QFileDialog, QGridLayout, QWidget)
from PyQt5.QtWidgets import *



def openShapeFileNameDialog(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.csv)", options=options)
    if fileName:
        self.shapeLine.setText(fileName)
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

def get_headers(csv_file, seperator):
    try:
        p2.columnBox.clear()
        p2.columnBox.addItems(list(pd.read_csv(csv_file, nrows=0, sep=seperator).columns))
    except:
        p2.columnBox.addItem("No File Selected")

def openInputFileNameDialog(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.csv)", options=options)
    if fileName:
        p1.inputLine.setText(fileName)
        if(str(p1.outFileType.currentText()) == 'CSV'):
            seperator = ","
        else:
            seperator = "\t"
        get_headers(fileName, seperator)
        return fileName
    else:
        return None

def clickMethod(csv_file, output_dir, filename=None):
    loc_df = map_locations.locations_df(csv_file, sep=seperator, output_dir=str(p1.outputLine.text()), \
                                        df_column=str(p1.columnBox.currentText()))
    return loc_df

def scrape_websites(csv_file):
    if(str(p1.outFileType.currentText()) == 'CSV'):
        seperator = ","
    else:
        seperator = "\t"
    web_df = webpage_locations.extract_webpage_locations(csv_file, sep=seperator, output_dir=str(p1.outputLine.text()), \
                                        column_name=str(p2.columnBox.currentText()))
    mapped_df = webpage_locations.map_web_locations(web_df, sep=seperator, output_dir=str(p1.outputLine.text()))

    return web_df

# Generate the Map
def generate_map(csv_file):
    if(str(p1.outFileType.currentText()) == 'CSV'):
        seperator = ","
    else:
        seperator = "\t"
    loc_df = pd.read_csv(csv_file, sep=seperator)
    loc_gdf = generate_maps.get_loc_gdf(loc_df, column_name=str(p2.columnBox.currentText()))
    text = str(p2.typeBox.currentText())
    if(text == "Heatmap"):
        hmap = heatmap.heatmap(loc_gdf, output_dir=str(p1.outputLine.text()))
    elif(text == "Choropleth"):
        gdf = choropleth.choropleth_map(loc_gdf, shp_path=str(p2.shapeLine.text()))
        plot = choropleth.plot_map(gdf, output_dir=str(p1.outputLine.text()))
    elif(text == "Map of Locations Overlay onto Shapefile"):
        gdf, loc_gdf = generate_maps.generate_overlay_gdf(loc_df, shp_path=str(p2.shapeLine.text()))
        plot = generate_maps.plot_gdf(gdf, loc_gdf, output_dir=str(p1.outputLine.text()))

# Generate the Map
def overlay(csv_file):
    if(str(p1.outFileType.currentText()) == 'CSV'):
        seperator = ","
    else:
        seperator = "\t"
    loc_df = map_locations.locations_df(csv_file, sep=seperator, output_dir=str(p1.outputLine.text()), \
                                        df_column=str(p2.columnBox.currentText()))
    loc_gdf = generate_maps.get_loc_gdf(loc_df)
    text = str(p2.typeBox.currentText())
    if(text == "Heatmap"):
        hmap = heatmap.heatmap(loc_gdf, output_dir=str(p1.outputLine.text()))
    elif(text == "Choropleth"):
        gdf = choropleth.choropleth_map(loc_gdf, shp_path=str(p2.shapeLine.text()))
        plot = choropleth.plot_map(gdf, output_dir=str(p1.outputLine.text()))
    elif(text == "Map of Locations Overlay onto Shapefile"):
        gdf, loc_gdf = generate_maps.generate_overlay_gdf(loc_df, shp_path=str(p2.shapeLine.text()))
        plot = generate_maps.plot_gdf(gdf, loc_gdf, output_dir=str(p1.outputLine.text()))

app = QApplication([])

# page 1
p1 = QWizardPage()
layout = QtWidgets.QVBoxLayout()
p1.setTitle('PyPACK File Configuration')
# Input Label/Line
file_types = [
        p1.tr('CSV'),
        p1.tr('TSV'),
        ]

p1.fileLabel= QLabel("Please Choose Type of File")
p1.outFileType = QComboBox(p1)
p1.outFileType.addItems(file_types)

p1.inputLabel = QLabel("Please Enter or Browse for an Input File")
p1.open_file = QPushButton('Browse for Input File', p1)
p1.open_file.clicked.connect(lambda: openInputFileNameDialog(p1))
p1.inputLine = QLineEdit(p1)
p1.outputLine = QLineEdit(p1)

# Browse for Output File Path
p1.outputLabel = QLabel("Please Enter or Browse for an Output Directory")
p1.output_file = QPushButton('Browse for Output Directory', p1)
p1.output_file.clicked.connect(lambda: openOutputFileNameDialog(p1))

layout.addWidget(p1.fileLabel)
layout.addWidget(p1.outFileType)
layout.addWidget(p1.inputLabel)
layout.addWidget(p1.inputLine)
layout.addWidget(p1.open_file)
layout.addWidget(p1.outputLabel)
layout.addWidget(p1.outputLine)
layout.addWidget(p1.output_file)

p1.setLayout(layout)

# page 2
p2 = QWizardPage()
layout = QtWidgets.QVBoxLayout()
p2.setTitle('PyPACK Column Selection')
p2.columnLabel = QLabel("Please Choose a Column to Analyze")
p2.columnBox = QComboBox(p2)

# Browse for ShapeFile Path
p2.shapeLabel = QLabel("***OPTIONAL*** (Browse Only if Generating an Overlay/Choropleth Map)")
p2.shapeLine = QLineEdit(p2)
p2.shape_file = QPushButton('Browse for Shape File', p2)
p2.shape_file.clicked.connect(lambda: openShapeFileNameDialog(p2))

# List of Map Types PyPACK Supports
map_types = [
        p2.tr('Heatmap'),
        p2.tr('Choropleth'),
        p2.tr('Map of Locations Overlay onto Shapefile'),
        ]
# Map Drop-Down Box
p2.mapTypeLabel = QLabel("If Generating a Map, Please Select Type of Map")
p2.typeBox = QComboBox(p2)
p2.typeBox.addItems(map_types)

# Column information
layout.addWidget(p2.columnLabel)
layout.addWidget(p2.columnBox)

# Type of Maps
layout.addWidget(p2.mapTypeLabel)
layout.addWidget(p2.typeBox)

# Shapefile information
layout.addWidget(p2.shapeLabel)
layout.addWidget(p2.shapeLine)
layout.addWidget(p2.shape_file)


p2.setLayout(layout)

# page 3
p3 = QWizardPage()
p3.setTitle('PyPACK Action Selection')
layout = QtWidgets.QVBoxLayout()
p3.fileLabel= QLabel("What you would like to do?")
p3.gen_maps = QPushButton("Extract Locations and Generate Map", p3)
p3.scrape_web = QPushButton("Scrape Websites", p3)
p3.gen_map_only = QPushButton("Generate a Map Only", p3)
p3.extract_locs = QPushButton("Extract Locations Only", p3)

# Parse Locations button
p3.extract_locs.clicked.connect(lambda: clickMethod(p1.inputLine.text(), p1.outputLine.text()))

# Gen-Map Button
p3.gen_maps.clicked.connect(lambda: overlay(p1.inputLine.text()))

# Websites Location
p3.scrape_web.clicked.connect(lambda: scrape_websites(p1.inputLine.text()))

# Websites Location
p3.gen_map_only.clicked.connect(lambda: generate_map(p1.inputLine.text()))

layout.addWidget(p3.fileLabel)
layout.addWidget(p3.gen_maps)
layout.addWidget(p3.scrape_web)
layout.addWidget(p3.gen_map_only)
layout.addWidget(p3.extract_locs)
p3.setLayout(layout)




# wizard

def main():
    import sys
    wizard = QWizard()
    # Run docker
    run_docker()
    wizard.addPage(p1)
    wizard.addPage(p2)
    wizard.addPage(p3)
    wizard.show()
    sys.exit(app.exec_())
