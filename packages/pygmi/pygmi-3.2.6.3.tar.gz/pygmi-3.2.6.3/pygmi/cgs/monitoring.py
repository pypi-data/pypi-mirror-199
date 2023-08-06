# -----------------------------------------------------------------------------
# Name:        monitoring.py (part of PyGMI)
#
# Author:      Patrick Cole, Emmanuel Sakala, Gabrielle Janse van Rensburg
# E-Mail:      pcole@geoscience.org.za
#
# Copyright:   (c) 2021 Council for Geoscience
# Licence:     Confidential, only for CGS.
# -----------------------------------------------------------------------------
"""AI Dolomite Routines."""


import os

from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import rasterio
import rasterio.mask
import rasterio.shutil
from rasterio.io import MemoryFile
from rasterio.windows import Window
from rasterio.plot import plotting_extent
from shapely.geometry import box
from shapely.geometry import Polygon
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
import geopandas as gpd

from pygmi.misc import frm
from pygmi.misc import ProgressBarText
from pygmi.raster import datatypes


class MyMplCanvas(FigureCanvasQTAgg):
    """Canvas for the actual plot."""

    def __init__(self, parent=None):
        fig = Figure()
        super().__init__(fig)

        if parent is None:
            self.showprocesslog = print
        else:
            self.showprocesslog = parent.showprocesslog

        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def t3_raster(self, ifile, ifile1):
        """
        Routine to plot raster data on tab 3.

        Parameters
        ----------
        ifile : str
            input INSAR filename.
        ifile1 : str
            input area shapefile filename.

        Returns
        -------
        None.
        """
        sar_img = rasterio.open(ifile)
        img = sar_img.read(1)
        img[img == 0] = sar_img.nodata
        img[img == sar_img.nodata] = np.nan

        extents = plotting_extent(sar_img)

        self.figure.clf()
        axes = self.figure.add_subplot(111, label='map')
        axes.ticklabel_format(style='plain')
        axes.tick_params(axis='x', rotation=90)
        axes.tick_params(axis='y', rotation=0)

        test = axes.imshow(img, cmap='viridis', extent=extents)

        self.figure.colorbar(test)

        gdf1 = gpd.read_file(ifile1)
        gdf1.boundary.plot(ax=axes)

        bounds = gdf1.total_bounds

        pad = (bounds[2]-bounds[0])*0.1

        axes.set_xlim(bounds[0]-pad, bounds[2]+pad)
        axes.set_ylim(bounds[1]-pad, bounds[3]+pad)

        axes.xaxis.set_major_formatter(frm)
        axes.yaxis.set_major_formatter(frm)

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def t3_vector(self, ifile1, ifile2):
        """
        Plot vector data.

        Parameters
        ----------
        ifile1 : str
            Area shapefile filename.
        ifile2 : str
            Stability point shapefile filename.

        Returns
        -------
        None.

        """
        gdf1 = gpd.read_file(ifile1)
        gdf2 = gpd.read_file(ifile2)

        self.figure.clf()
        axes = self.figure.add_subplot(111, label='map')
        axes.ticklabel_format(style='plain')
        axes.tick_params(axis='x', rotation=90)
        axes.tick_params(axis='y', rotation=0)

        gdf1.boundary.plot(ax=axes, label='Boundary')
        gdf2.plot(ax=axes, color='k', label='Stability Points')

        axes.xaxis.set_major_formatter(frm)
        axes.yaxis.set_major_formatter(frm)

        axes.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                    ncol=2, fancybox=True, shadow=True)

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def t4_bhole_class(self, class_img, extent):
        """
        Plot borehole classification.

        Parameters
        ----------
        class_img : numpy array
            Array of output classes.

        Returns
        -------
        None.

        """
        self.figure.clf()

        ax1 = self.figure.add_subplot(111, label='map')

        vals = np.unique(class_img)
        vals = vals.compressed()
        vals = vals.astype(int)
        vals2 = []

        class_img = class_img.copy()

        for i, val in enumerate(vals):
            class_img[class_img == val] = i
            vals2.append(i)

        vals2 = np.array(vals2)
        test = ax1.imshow(class_img, extent=extent)

        bnds = (vals2 - 0.5).tolist() + [vals2.max() + .5]

        if len(vals) > 1:
            cbar = ax1.figure.colorbar(test, boundaries=bnds,
                                       label='Class Name')
            cbar.set_ticks(vals2, labels=vals)

        ax1.ticklabel_format(style='plain')
        ax1.tick_params(axis='x', rotation=90)
        ax1.xaxis.set_major_formatter(frm)
        ax1.yaxis.set_major_formatter(frm)

        self.figure.tight_layout()
        self.figure.canvas.draw()


class Monitoring(QtWidgets.QDialog):
    """
    Early Warning System Monitoring Module.

    Attributes
    ----------
    parent : parent
        reference to the parent routine
    indata : dictionary
        dictionary of input datasets
    outdata : dictionary
        dictionary of output datasets
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is None:
            self.showprocesslog = print
        else:
            self.showprocesslog = parent.showprocesslog

        self.indata = {}
        self.outdata = {}
        self.parent = parent

        if parent is not None:
            self.piter = parent.pbar.iter
        else:
            self.piter = ProgressBarText().iter

        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        self.tab4 = QtWidgets.QWidget()

        # Tab 1
        self.qfile = {}

        # Tab 2
        self.tablewidget = QtWidgets.QTableWidget()
        # self.param_ratio = {}
        self.param_threshold = {}
        delegate = NumericDelegate(self.tablewidget)
        self.tablewidget.setItemDelegate(delegate)

        # Tab 3
        self.mt3 = MyMplCanvas(self)
        self.t3_combobox1 = QtWidgets.QComboBox()
        self.t3_run = True
        self.t3_calculate = QtWidgets.QPushButton('Calculate')
        self.myarray_bh = None
        self.trans_bh = None
        self.out_meta = {}
        self.data = datatypes.Data()
        self.t3_firstrun = True

        # Tab 4
        self.t4_combobox1 = QtWidgets.QComboBox()
        self.mt4 = MyMplCanvas(self)
        self.bhole_rank = []
        self.final_result = []
        self.insar_rank = []
        self.insar_extent = None
        self.bh_extent = None
        self.ofile = ''
        self.t4_export = QtWidgets.QPushButton('Export')

        self.setupui()

    def setupui(self):
        """
        Set up UI.

        Returns
        -------
        None.

        """
        # Initialize tab screen

        layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle(r'Monitoring Window')
        self.resize(640, 480)

        # Initialize tab screen

# Add tabs
        self.tabs.addTab(self.tab1, 'Import Data')
        self.tabs.addTab(self.tab2, 'Parameters')
        self.tabs.addTab(self.tab3, 'Early Warning Calculation')
        self.tabs.addTab(self.tab4, 'Results')

        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)

        # Create first tab
        area_shp = QtWidgets.QPushButton('Area Vector Data (.shp)')
        stab_shp = QtWidgets.QPushButton('Stability Points Vector Data (.shp,'
                                         ' .pix)')
        insar = QtWidgets.QPushButton('InSAR Raster Data (.tif)')
        bhole = QtWidgets.QPushButton('Borehole Data (.csv)')

        self.qfile['area_shp'] = QtWidgets.QLineEdit('')
        self.qfile['stab_shp'] = QtWidgets.QLineEdit('')
        self.qfile['insar'] = QtWidgets.QLineEdit('')
        self.qfile['bhole'] = QtWidgets.QLineEdit('')

        tab1_layout = QtWidgets.QGridLayout()

        tab1_layout.addWidget(area_shp, 0, 0, 1, 1)
        tab1_layout.addWidget(self.qfile['area_shp'], 0, 1, 1, 1)
        tab1_layout.addWidget(stab_shp, 1, 0, 1, 1)
        tab1_layout.addWidget(self.qfile['stab_shp'], 1, 1, 1, 1)
        tab1_layout.addWidget(insar, 2, 0, 1, 1)
        tab1_layout.addWidget(self.qfile['insar'], 2, 1, 1, 1)
        tab1_layout.addWidget(bhole, 3, 0, 1, 1)
        tab1_layout.addWidget(self.qfile['bhole'], 3, 1, 1, 1)

        self.tab1.setLayout(tab1_layout)

        area_shp.clicked.connect(lambda: self.load_data('area_shp', 'shp'))
        stab_shp.clicked.connect(lambda: self.load_data('stab_shp', 'shp'))
        insar.clicked.connect(lambda: self.load_data('insar', 'tif'))
        bhole.clicked.connect(lambda: self.load_data('bhole', 'csv'))

        # Create Second Tab
        tab2_layout = QtWidgets.QGridLayout()
        lbl_set_params = QtWidgets.QLabel('Please set the parameters:')

        table_group = self.tablewidget
        table_group.setRowCount(26)
        table_group.setColumnCount(5)
        table_group.setHorizontalHeaderLabels(['Ratio', 'Threshold',
                                               'Dry', 'Moist', 'Wet'])
        table_group.resizeColumnsToContents()
        self.t2_set_threshold()

        tab2_layout.addWidget(lbl_set_params, 0, 0, 1, 1)
        tab2_layout.addWidget(table_group, 2, 0, 1, 1)

        self.tab2.setLayout(tab2_layout)

        # Create Third Tab
        mpl_toolbar_t3 = NavigationToolbar2QT(self.mt3, self.parent)
        t3_label1 = QtWidgets.QLabel('Early Warning System Monitoring Module'
                                     ' Calculation')
        t3_label2 = QtWidgets.QLabel('The InSAR data is combined with the '
                                     'borehole sinkhole hazard classification '
                                     'results')
        t3_label3 = QtWidgets.QLabel('View Data:')
        t3_label4 = QtWidgets.QLabel('Proceed with the calculation:')

        self.t3_combobox1.addItems(['Location Data',
                                    'InSAR Data'])

        self.t3_combobox1.setCurrentText('Location Data')

        tab3_layout = QtWidgets.QGridLayout()
        tab3_layout.addWidget(t3_label1, 0, 0, 1, 2)
        tab3_layout.addWidget(t3_label2, 1, 0, 1, 2)
        tab3_layout.addWidget(t3_label3, 4, 0, 1, 2)
        tab3_layout.addWidget(self.t3_combobox1, 4, 1, 1, 1)
        tab3_layout.addWidget(self.mt3, 5, 0, 2, 2)
        tab3_layout.addWidget(mpl_toolbar_t3, 7, 1, 1, 1)
        tab3_layout.addWidget(t3_label4, 8, 0, 1, 1)
        tab3_layout.addWidget(self.t3_calculate, 8, 1, 1, 1)

        self.t3_combobox1.currentIndexChanged.connect(self.t3_change_graph)

        self.tab3.setLayout(tab3_layout)

        self.t3_calculate.clicked.connect(self.eng_proc)

        # Create Fourth Tab
        mpl_toolbar_t4 = NavigationToolbar2QT(self.mt4, self.parent)

        t4_label1 = QtWidgets.QLabel('Classified image:')
        self.t4_combobox1.addItems(['Final classification',
                                    'InSAR classification',
                                    'Borehole rank classification'])

        self.t4_combobox1.setCurrentText('Final classification')

        tab4_layout = QtWidgets.QGridLayout()
        tab4_layout.addWidget(t4_label1, 4, 0, 1, 1)
        tab4_layout.addWidget(self.t4_combobox1, 4, 1, 1, 1)
        tab4_layout.addWidget(self.mt4, 5, 0, 2, 2)
        tab3_layout.addWidget(mpl_toolbar_t4, 7, 1, 1, 1)
        tab4_layout.addWidget(self.t4_export, 8, 1, 1, 1)

        self.t4_export.clicked.connect(self.export_raster)

        self.tab4.setLayout(tab4_layout)

        self.t4_combobox1.currentIndexChanged.connect(self.t4_change_graph)


# Add tabs to widget
        layout.addWidget(self.tabs)

        self.tabs.currentChanged.connect(self.change_tab)

    def load_data(self, datatype, ext):
        """
        Load data.

        Parameters
        ----------
        datatype : str
            string describing the file.
        ext : str
            filename extension.

        Returns
        -------
        None.

        """
        if ext == 'csv':
            ext = 'CSV file (*.csv)'
        elif ext == 'tif':
            ext = 'GeoTiff file (*.tif)'
        elif ext == 'pix':
            ext = 'Geomatica file (*.pix)'
        else:
            ext = 'Shape file (*.shp)'

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.parent, 'Open File', '.', ext)
        if filename == '':
            return

        os.chdir(os.path.dirname(filename))

        self.qfile[datatype].setText(filename)

        test = [self.qfile[i].text() for i in self.qfile]

        if '' not in test:
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(2, True)

    def change_tab(self, index):
        """
        Change tab.

        Parameters
        ----------
        index : int
            Tab index.

        Returns
        -------
        None.

        """
        if index == 2 and self.t3_firstrun is True:
            self.t3_firstrun = False
            self.t3_change_graph()

    def t2_set_threshold(self):
        """
        Set threshold for different materials.

        Returns
        -------
        None.

        """
        param_ratio = {'Fill': [1, 47, 37, 30],
                       'Tr - gvl': [1, 47, 37, 30],
                       'Tr - sa': [1, 47, 37, 30],
                       'Tr - si': [.3, 85, 55, 45],
                       'Tr - cl': [.2, 85, 50, 35],
                       'Pedo': [.1, 90, 90, 90],
                       'Res dol - gvl': [.8, 47, 37, 30],
                       'Res dol - wad': [1, 85, 55, 45],
                       'Res dol - sa': [.7, 70, 60, 50],
                       'Res dol - si': [.7, 85, 55, 45],
                       'Res dol - cl': [.6, 85, 50, 35],
                       'Res chert - gvl': [.8, 70, 60, 50],
                       'Res chert - sa': [.8, 47, 37, 30],
                       'Res chert - si': [.7, 85, 55, 45],
                       'Res chert - cl': [.7, 85, 50, 35],
                       'Res intru - gvl': [.5, 47, 37, 30],
                       'Res intru - sa': [.5, 47, 37, 30],
                       'Res intru - si': [.3, 85, 55, 45],
                       'Res intru - cl': [.3, 85, 50, 35],
                       'Res Karoo - gvl': [.5, 70, 60, 50],
                       'Res Karoo - sa': [.5, 46, 35, 30],
                       'Res Karoo - si': [.3, 46, 35, 30],
                       'Res Karoo - cl': [.3, 46, 35, 30],
                       'Weathered - dol': [.01, 46, 35, 30],
                       'Weathered - intru': [.01, 46, 35, 30],
                       'Cavity': [1, .01, .01, .01]}

        for name in param_ratio:
            item = QtWidgets.QTableWidgetItem(name)
            key_list = list(param_ratio)
            row = key_list.index(name)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.tablewidget.setItem(row, 0, item)

            for i, val in enumerate(param_ratio[name]):
                item2 = QtWidgets.QTableWidgetItem(str(val))
                self.tablewidget.setItem(row, i+1, item2)

        self.tablewidget.resizeColumnsToContents()

    def t3_change_graph(self):
        """
        Change the graph type on tab 3.

        Returns
        -------
        None.

        """
        option = self.t3_combobox1.currentText()

        if option == 'Location Data':
            self.mt3.figure.clf()
            ifile1 = self.qfile['area_shp'].text()
            ifile2 = self.qfile['stab_shp'].text()

            self.mt3.t3_vector(ifile1, ifile2)

        elif option == 'InSAR Data':
            ifile = self.qfile['insar'].text()
            ifile1 = self.qfile['area_shp'].text()

            self.mt3.t3_raster(ifile, ifile1)

    def t4_change_graph(self):
        """
        Change the graph type on tab 3.

        Returns
        -------
        None.

        """
        option = self.t4_combobox1.currentText()

        if option == 'Final classification':
            self.mt4.figure.clf()

            self.mt4.t4_bhole_class(self.final_result, self.bh_extent)

        elif option == 'InSAR classification':

            self.mt4.t4_bhole_class(self.insar_rank, self.bh_extent)

        elif option == 'Borehole rank classification':

            self.mt4.t4_bhole_class(self.bhole_rank, self.bh_extent)

    def export_raster(self):
        """
        Export raster.

        Returns
        -------
        None.

        """
        file_location = self.qfile['insar'].text()
        file_string = file_location[:-4]

        ofile = file_string + '_final_class.tif'
        with rasterio.open(ofile, 'w', **self.out_meta) as dest:
            dest.write(self.final_result, 1)

        self.showprocesslog(r'Export Complete to ' + ofile)

        ofile = file_string + '_bhole_rank.tif'
        with rasterio.open(ofile, 'w', **self.out_meta) as dest:
            dest.write(self.bhole_rank, 1)

        self.showprocesslog(r'Export Complete to ' + ofile)

        ofile = file_string + '_insar_rank.tif'
        with rasterio.open(ofile, 'w', **self.out_meta) as dest:
            dest.write(self.insar_rank, 1)

        self.showprocesslog(r'Export Complete to ' + ofile)

    def mask_raster_with_geometry(self, raster, transform, shapes, **kwargs):
        """
        Use rasterio.mask.mask to allow for in-memory processing.

        by https://gis.stackexchange.com/users/177672/luna

        Docs: https://rasterio.readthedocs.io/en/latest/api/rasterio.mask.html

        Parameters
        ----------
        raster : numpy array
            Input.
        transform : affine.Affine
            the transform of the raster.
        shapes : list
            List of shapely Polygons.
        **kwargs : **kwargs
            passed to rasterio.mask.mask.

        Returns
        -------
        output : numpy array
            Output.
        outtrans : affine.Affine
            output transform.

        """
        with rasterio.io.MemoryFile() as memfile:
            with memfile.open(
                driver='GTiff',
                height=raster.shape[0],
                width=raster.shape[1],
                count=1,
                dtype=raster.dtype,
                transform=transform,
            ) as dataset:
                dataset.write(raster, 1)
            with memfile.open() as dataset:
                output, outtrans = rasterio.mask.mask(dataset, shapes,
                                                      **kwargs)
        return output.squeeze(0), outtrans

    def repose(self, layer_number, df, ly1):
        """
        Calculate the radius of repose for a material.

        This is based on a layer thickness and angle of repose.

        Parameters
        ----------
        layer_number : int
            Layer number.
        df : pandas DataaFrame
            Main dataframe with data.
        ly1 : float
            Layer thickness.

        Returns
        -------
        radius1 :
            Radius of repose.

        """
        layer_material = 'Layer'+str(layer_number)+'_material'
        layer_condition = 'Layer'+str(layer_number)+'_condition'

        numrows = self.tablewidget.rowCount()

        newval = {}
        newval['Ratio'] = []
        newval['thres'] = []

        tmp = []
        for i in range(numrows):
            key = self.tablewidget.item(i, 0).text()
            dry = float(self.tablewidget.item(i, 2).text())
            moist = float(self.tablewidget.item(i, 3).text())
            wet = float(self.tablewidget.item(i, 4).text())

            tmp.append([key, 'Dry', dry])
            tmp.append([key, 'Moist', moist])
            tmp.append([key, 'Wet', wet])


        tmp2 = [['Fill', 'Dry', 47],
                ['Fill', 'Moist', 37],
                ['Fill', 'Wet', 30],
                ['Tr - gvl', 'Dry', 47],
                ['Tr - gvl', 'Moist', 37],
                ['Tr - gvl', 'Wet', 30],
                ['Tr - sa', 'Dry', 47],
                ['Tr - sa', 'Moist', 37],
                ['Tr - sa', 'Wet', 30],
                ['Tr - si', 'Dry', 85],
                ['Tr - si', 'Moist', 55],
                ['Tr - si', 'Wet', 45],
                ['Tr - cl', 'Dry', 85],
                ['Tr - cl', 'Moist', 50],
                ['Tr - cl', 'Wet', 35],
                ['Pedo', 'Dry', 90],
                ['Pedo', 'Moist', 90],
                ['Pedo', 'Wet', 90],
                ['Res dol - wad', 'Dry', 85],
                ['Res dol - wad', 'Moist', 55],
                ['Res dol - wad', 'Wet', 45],
                ['Res dol - gvl', 'Dry', 47],
                ['Res dol - gvl', 'Moist', 37],
                ['Res dol - gvl', 'Wet', 30],
                ['Res dol - sa', 'Dry', 70],
                ['Res dol - sa', 'Moist', 60],
                ['Res dol - sa', 'Wet', 50],
                ['Res dol - si', 'Dry', 85],
                ['Res dol - si', 'Moist', 55],
                ['Res dol - si', 'Wet', 45],
                ['Res dol - cl', 'Dry', 85],
                ['Res dol - cl', 'Moist', 50],
                ['Res dol - cl', 'Wet', 35],
                ['Res chert - gvl', 'Dry', 70],
                ['Res chert - gvl', 'Moist', 60],
                ['Res chert - gvl', 'Wet', 50],
                ['Res chert - sa', 'Dry', 47],
                ['Res chert - sa', 'Moist', 37],
                ['Res chert - sa', 'Wet', 30],
                ['Res chert - si', 'Dry', 85],
                ['Res chert - si', 'Moist', 55],
                ['Res chert - si', 'Wet', 45],
                ['Res chert - cl', 'Dry', 85],
                ['Res chert - cl', 'Moist', 50],
                ['Res chert - cl', 'Wet', 35],
                ['Res intru - gvl', 'Dry', 47],
                ['Res intru - gvl', 'Moist', 37],
                ['Res intru - gvl', 'Wet', 30],
                ['Res intru - sa', 'Dry', 47],
                ['Res intru - sa', 'Moist', 37],
                ['Res intru - sa', 'Wet', 30],
                ['Res intru - si', 'Dry', 85],
                ['Res intru - si', 'Moist', 55],
                ['Res intru - si', 'Wet', 45],
                ['Res intru - cl', 'Dry', 85],
                ['Res intru - cl', 'Moist', 50],
                ['Res intru - cl', 'Wet', 35],
                ['Res Karoo - gvl', 'Dry', 70],
                ['Res Karoo - gvl', 'Moist', 60],
                ['Res Karoo - gvl', 'Wet', 50],
                ['Res Karoo - sa', 'Dry', 46],
                ['Res Karoo - sa', 'Moist', 35],
                ['Res Karoo - sa', 'Wet', 30],
                ['Res Karoo - si', 'Dry', 46],
                ['Res Karoo - si', 'Moist', 35],
                ['Res Karoo - si', 'Wet', 30],
                ['Res Karoo - cl', 'Dry', 46],
                ['Res Karoo - cl', 'Moist', 35],
                ['Res Karoo - cl', 'Wet', 30],
                ['Weathered - dol', 'Dry', 46],
                ['Weathered - dol', 'Moist', 35],
                ['Weathered - dol', 'Wet', 30],
                ['Weathered - intru', 'Dry', 46],
                ['Weathered - intru', 'Moist', 35],
                ['Weathered - intru', 'Wet', 30],
                ['Cavity', 'Dry', 0.01],
                ['Cavity', 'Moist', 0.01],
                ['Cavity', 'Wet', 0.01]]


        dfr = pd.DataFrame(tmp,
                           columns=[layer_material, layer_condition, 'repose'])

        df2 = pd.merge(df, dfr, how='left',
                       on=[layer_material, layer_condition])

        angle1 = np.deg2rad(df2['repose'])
        radius1 = ly1/np.tan(angle1)

        return radius1

    def sink_cal(self, x):
        """
        Sinkhole calculation.

        This assigns the sinkhole diameters to four values, from 0 to 1.

        Parameters
        ----------
        x : float
            sinkhole diameter.

        Returns
        -------
        z : int
            Output class.

        """
        z = np.zeros_like(x)
        z[x < 2] = 0
        z[(x >= 2) & (x < 5)] = 0.33
        z[(x >= 5) & (x <= 15)] = 0.66
        z[x > 15] = 1.

        return z

    def eng_proc(self):
        """
        Engineering Process calculation and quality check.

        (Calculating the borehole classification)

        Returns
        -------
        None.

        """
        csv_file = self.qfile['bhole'].text()

        df = pd.read_csv(csv_file, skip_blank_lines=True).dropna()
        df.reset_index(inplace=True, drop=True)

        ly1 = df['Layer1_thickness_m']
        ly2 = df['Layer2_thickness_m']
        ly3 = df['Layer3_thickness_m']
        ly4 = df['Layer4_thickness_m']

        mat1 = df['Layer1_material']
        mat2 = df['Layer2_material']
        mat3 = df['Layer3_material']
        mat4 = df['Layer4_material']

        # fix: total radius only used to use ly1.
        totalradius = (self.repose(1, df, ly1) +
                       self.repose(2, df, ly2) +
                       self.repose(3, df, ly3) +
                       self.repose(4, df, ly4))
        sinkholediameter = 2*totalradius
        df['Sinkhole_diameter'] = sinkholediameter

        wl = df['Depth to water level (m)']
        dbr = df['DDBR_m']
        ingress = (wl > dbr)
        ingress_n = ingress.astype(int)

        # Group 1 parameters
        df_voids = df['Presence of voids'].map({'YES': 1, 'NO': 0})
        df_air = df['Air loss'].map({'YES': 1, 'NO': 0})
        df_mat = df['Material loss'].map({'YES': 1, 'NO': 0})

        df['Fzy_Sink_size'] = self.sink_cal(sinkholediameter)
        df['Sinkhole_Size'] = df['Fzy_Sink_size'].replace([0, 0.33, 0.66, 1.0],
                                                          ['Small', 'Medium',
                                                           'Large',
                                                           'Very Large'])
        df['Ratio_L1'] = ly1 / dbr
        df['Ratio_L2'] = ly2 / dbr
        df['Ratio_L3'] = ly3 / dbr
        df['Ratio_L4'] = ly4 / dbr

        if ((df['Ratio_L1'] + df['Ratio_L2'] + df['Ratio_L3'] +
             df['Ratio_L4'] == 1).all()):
            self.showprocesslog('Borehole Quality Control - PASS')
        else:
            self.showprocesslog('Quality Control Fail: Please check if the sum'
                                ' of layer thickness is equal to the depth to'
                                ' bedrock')

        # Should this only be three ratios?
        df1 = df[['Ratio_L1', 'Ratio_L2', 'Ratio_L3', 'Ratio_L4']]
        df['Ratio'] = df1.idxmax(1)

        self.showprocesslog('Calculating Ratios...')

        filt = (df['Ratio'] == 'Ratio_L1')
        df.loc[filt, 'Ratio'] = df.loc[filt, 'Layer1_material']
        filt = (df['Ratio'] == 'Ratio_L2')
        df.loc[filt, 'Ratio'] = df.loc[filt, 'Layer2_material']
        filt = (df['Ratio'] == 'Ratio_L3')
        df.loc[filt, 'Ratio'] = df.loc[filt, 'Layer3_material']
        filt = (df['Ratio'] == 'Ratio_L4')
        df.loc[filt, 'Ratio'] = df.loc[filt, 'Layer4_material']

        # Parameters to be edited
        # Get the threshold info from the table
        numrows = self.tablewidget.rowCount()

        newval = {}
        newval['Ratio'] = []
        newval['thres'] = []
        for i in range(numrows):
            key = self.tablewidget.item(i, 0)
            newval['Ratio'].append(key.text())
            val = self.tablewidget.item(i, 1)
            newval['thres'].append(float(val.text()))

        dfnv = pd.DataFrame(newval)
        df2 = pd.merge(df, dfnv, how='left', on='Ratio')

        ratio1 = np.array(df2['thres'])

        void_A_loss_max = np.maximum(df_voids, df_air)
        void_A_Mat_loss_max = np.maximum(void_A_loss_max, df_mat)
        void_ingress_max = np.maximum(void_A_Mat_loss_max, ingress_n)

        df['Rank_class'] = void_ingress_max / ratio1
        df['Rank_class'] = df['Rank_class'].round(4)
        df['Final_class'] = df['Rank_class']
        df['Final_class'].astype(str)

        df['Test_Out_Drill'] = np.where((mat1 == 'Cavity') |
                                        (mat2 == 'Cavity') |
                                        (mat3 == 'Cavity') |
                                        (mat4 == 'Cavity'), '7',
                                        df['Final_class'])
        df['Test_Out_Mat'] = np.where((df['Presence of voids'] == 'YES') &
                                      (df['Air loss'] == 'YES') &
                                      (df['Material loss'] == 'YES'), '7',
                                      df['Final_class'])
        df['BH_Rank'] = np.where((df['Test_Out_Drill'] == '7') |
                                 (df['Test_Out_Mat'] == '7'),
                                 '5_6_7_8', df['Final_class'])

        df['Cavity'] = '0'
        df.loc[mat1 == 'Cavity', 'Cavity'] = '1'
        df.loc[mat2 == 'Cavity', 'Cavity'] = '2'
        df.loc[mat3 == 'Cavity', 'Cavity'] = '3'
        df.loc[mat4 == 'Cavity', 'Cavity'] = '4'

        L1 = 0
        L2 = ly1
        L3 = ly1+ly2
        L4 = ly3+ly2+ly1
        # breakpoint()

        df['Cavity_1'] = np.where((df['Cavity'] == '1'), L1, '0')
        df['Cavity_1'] = np.where((df['Cavity'] == '2'), L2, df['Cavity_1'])
        df['Cavity_1'] = np.where((df['Cavity'] == '3'), L3, df['Cavity_1'])
        df['Cavity_1'] = np.where((df['Cavity'] == '4'), L4, df['Cavity_1'])
        df['Cavity_2'] = np.where((mat1 == 'Cavity') & (mat2 == 'Cavity') &
                                  (mat3 == 'Cavity') & (mat4 == 'Cavity'),
                                  '0', df['Cavity_1'])
        df['Cavity_3'] = np.where((mat2 == 'Cavity') & (mat3 == 'Cavity') &
                                  (mat4 == 'Cavity') & (mat1 != 'Cavity'),
                                  L2, df['Cavity_2'])
        df['Cavity_4'] = np.where((mat3 == 'Cavity') & (mat4 == 'Cavity') &
                                  (mat1 != 'Cavity') & (mat2 != 'Cavity'),
                                  L3, df['Cavity_3'])
        df['Cavity_4'] = np.where((mat1 == 'Cavity'), L1, df['Cavity_4'])
        df['Cavity_4'] = np.where((mat1 != 'Cavity') & (mat2 == 'Cavity'),
                                  L2, df['Cavity_4'])
        df['Cavity_4'] = np.where((mat1 != 'Cavity') & (mat2 != 'Cavity') &
                                  (mat3 == 'Cavity'),
                                  L3, df['Cavity_4'])

        df['Result_Class'] = np.where((df['Cavity_4'].astype(int) > 55),
                                      df['Final_class'], df['BH_Rank'])

        df['Result_Class_1'] = np.where((df['Result_Class'] == str(1.4286)) &
                                        (df['Presence of voids'] == 'YES'),
                                        '5_6_7_8', df['Result_Class'])

        df['Result_Class_1'].replace(['0.0', '3.3333', 'inf', '8'],
                                     '1', inplace=True)

        df['Result_Class_1'].replace(['1.0', '1.25', '1.4286', '1.6667',
                                      '2.0', '5.0', '10.0', '100.0'],
                                     '2_3_4', inplace=True)

        df['Hazard_Class'] = np.where((df['Result_Class'] == str(0.0)) &
                                      (df['Ratio'] == 'Res dol - wad'),
                                      '2_3_4', df['Result_Class_1'])

        filt = (df['Cavity_4'].astype(int) > 55)
        df.loc[filt, 'Hazard_Class'].replace(['3.3333', '0.0', '8.0'],
                                             '1', inplace=True)

        df.loc[filt, 'Hazard_Class'].replace(['1.0', '1.25', '1.4286',
                                              '1.6667'], '2_3_4',
                                             inplace=True)

        # df2 = df.drop(['Ratio_L1', 'Ratio_L2', 'Ratio_L3',
        #                'Ratio', 'Rank_class', 'Ratio_L4', 'BH_Rank',
        #                'Test_Out_Drill', 'Test_Out_Mat',
        #                'Cavity', 'Cavity_1', 'Cavity_2', 'Cavity_3',
        #                'Cavity_4', 'Result_Class', 'Result_Class_1',
        #                'Final_class', 'Fzy_Sink_size'], axis=1)

        self.showprocesslog('Borehole Classification Done.')

        # self.qfile['bhole_class'] = df2

        # the sar image is fetched here to get the cell size
        sar_file = self.qfile['insar'].text()

        with rasterio.open(sar_file) as tmp:
            cell_size = tmp.transform[0]

        df['Hazard_Class_no'] = df['Hazard_Class'].replace('1', 1)
        df['Hazard_Class_no'] = df['Hazard_Class_no'].replace('2_3_4', 4)
        df['Hazard_Class_no'] = df['Hazard_Class_no'].replace('5_6_7_8', 7)

        values = df['Hazard_Class_no'].astype(float)
        xv = df['X']
        yv = df['Y']

        n_column = (np.max(xv) - np.min(xv))/cell_size
        n_rows = (np.max(yv) - np.min(yv))/cell_size

        xti = np.linspace(np.min(xv), np.max(xv), int(n_column))
        yti = np.linspace(np.min(yv), np.max(yv), int(n_rows))
        xi, yi = np.meshgrid(xti, yti)

        # interpolate and mask results
        zi = griddata((xv, yv), values, (xi, yi), method='linear')

        transform = rasterio.transform.from_origin(xv.min(), yv.max(),
                                                   cell_size, cell_size)
        inshape = self.qfile['area_shp'].text()

        gdf = gpd.read_file(inshape)

        coords = gdf['geometry'].loc[0].exterior.coords
        shapes = [Polygon([[p[0], p[1]] for p in coords])]

        # Output classification is in self.myarray_bh
        self.myarray_bh, self.trans_bh = self.mask_raster_with_geometry(
            np.flipud(zi), transform, shapes, nodata=np.nan, crop=True)

        self.showprocesslog('Automatic borehole classification - DONE')

        self.insar_incorp()

        self.mt4.t4_bhole_class(self.final_result, self.bh_extent)

        self.tabs.setTabEnabled(3, True)
        self.tabs.setCurrentIndex(3)

    def insar_incorp(self):
        """Incorporating the InSAR data."""
        sar_file = self.qfile['insar'].text()

        sar_img = rasterio.open(sar_file)
        myarray_sar = sar_img.read(1)

        self.showprocesslog('InSAR data import - DONE')
        self.showprocesslog('Creating the SAR class image...')

        myarray_sar[myarray_sar == 0] = sar_img.nodata
        myarray_sar = np.ma.masked_equal(myarray_sar, sar_img.nodata)

        x1 = (myarray_sar < -1)
        x2 = (myarray_sar >= -1) & (myarray_sar < 0)
        x3 = (myarray_sar >= 0)

        myarray_sar[x1] = 3
        myarray_sar[x2] = 2
        myarray_sar[x3] = 1

        self.insar_rank = myarray_sar
        self.insar_extent = plotting_extent(sar_img)

        self.showprocesslog('INSAR Class Image Done')

        self.showprocesslog('Fetching the borehole image...')
        myarray_bh = self.myarray_bh
        myarray_bh[np.isnan(myarray_bh)] = 1e+20
        myarray_bh = np.ma.masked_equal(myarray_bh, 1e+20)

        x1 = myarray_bh < 1
        x2 = (myarray_bh >= 1) & (myarray_bh <= 3)
        x3 = (myarray_bh >= 4) & (myarray_bh <= 5)
        x4 = (myarray_bh >= 6) & (myarray_bh <= 8)
        x5 = myarray_bh > 8

        myarray_bh[x1] = 1e+20
        myarray_bh[x2] = 1
        myarray_bh[x3] = 2
        myarray_bh[x4] = 3
        myarray_bh[x5] = 1e+20

        myarray_bh = np.ma.masked_equal(myarray_bh, 1e+20)

        # Not sure why this was done in two stages
        x1 = (myarray_bh == 1)
        x2 = (myarray_bh > 1) & (myarray_bh <= 3)
        x3 = (myarray_bh > 3)

        myarray_bh[x1] = 1
        myarray_bh[x2] = 2
        myarray_bh[x3] = 3

        self.out_meta.update({'driver': 'GTiff',
                              'height': myarray_bh.shape[0],
                              'width': myarray_bh.shape[1],
                              'transform': self.trans_bh,
                              'count': 1,
                              'dtype': myarray_bh.dtype,
                              'nodata': np.nan,
                              'crs': rasterio.crs.CRS.from_epsg(4326)})

        self.bhole_rank = myarray_bh

        self.showprocesslog('Creating the borehole class image...')
        # Write results to memory file, to take advantage of rasterio.

        bh_class_img = MemoryFile().open(driver='GTiff',
                                         height=myarray_bh.shape[0],
                                         width=myarray_bh.shape[1], count=1,
                                         dtype=myarray_bh.dtype,
                                         transform=self.trans_bh)
        bh_class_img.write(myarray_bh, 1)
        self.bh_extent = plotting_extent(bh_class_img)

        sar_class_img = MemoryFile().open(driver='GTiff',
                                          height=myarray_sar.shape[0],
                                          width=myarray_sar.shape[1], count=1,
                                          dtype=myarray_sar.dtype,
                                          transform=sar_img.transform)
        sar_class_img.write(myarray_sar, 1)

        # Get intersection of both datasets
        bb_raster1 = box(bh_class_img.bounds[0], bh_class_img.bounds[1],
                         bh_class_img.bounds[2], bh_class_img.bounds[3])
        bb_raster2 = box(sar_class_img.bounds[0], sar_class_img.bounds[1],
                         sar_class_img.bounds[2], sar_class_img.bounds[3])

        xminR1, _, _, ymaxR1 = bh_class_img.bounds
        xminR2, _, _, ymaxR2 = sar_class_img.bounds

        intersection = bb_raster1.intersection(bb_raster2)

        p1Y = intersection.bounds[3] - bh_class_img.res[1]/2
        p1X = intersection.bounds[0] + bh_class_img.res[0]/2
        p2Y = intersection.bounds[1] + bh_class_img.res[1]/2
        p2X = intersection.bounds[2] - bh_class_img.res[0]/2
        row1R1 = int((ymaxR1 - p1Y)/bh_class_img.res[1])
        row1R2 = int((ymaxR2 - p1Y)/sar_class_img.res[1])
        col1R1 = int((p1X - xminR1)/bh_class_img.res[0])
        col1R2 = int((p1X - xminR2)/bh_class_img.res[0])

        row2R1 = int((ymaxR1 - p2Y)/bh_class_img.res[1])
        row2R2 = int((ymaxR2 - p2Y)/sar_class_img.res[1])
        col2R1 = int((p2X - xminR1)/bh_class_img.res[0])
        col2R2 = int((p2X - xminR2)/bh_class_img.res[0])

        width1 = col2R1 - col1R1 + 1
        width2 = col2R2 - col1R2 + 1
        height1 = row2R1 - row1R1 + 1
        height2 = row2R2 - row1R2 + 1

        array_c_bh = bh_class_img.read(1, window=Window(col1R1, row1R1,
                                                        width1, height1))
        array_c_sar = sar_class_img.read(1, window=Window(col1R2, row1R2,
                                                          width2, height2))

        x1 = (array_c_sar == 3) & (array_c_bh == 3)
        x2 = (array_c_sar == 3) & (array_c_bh == 2)
        x3 = (array_c_sar == 3) & (array_c_bh == 1)
        x4 = (array_c_sar == 2) & (array_c_bh == 3)
        x5 = (array_c_sar == 2) & (array_c_bh == 2)
        x6 = (array_c_sar == 2) & (array_c_bh == 1)
        x7 = (array_c_sar == 1) & (array_c_bh == 3)
        x8 = (array_c_sar == 1) & (array_c_bh == 2)
        x9 = (array_c_sar == 1) & (array_c_bh == 1)
        x10 = (array_c_sar == 0) & (array_c_bh == 0)

        array_c_bh[x1] = 13
        array_c_bh[x2] = 12
        array_c_bh[x3] = 11
        array_c_bh[x4] = 10
        array_c_bh[x5] = 9
        array_c_bh[x6] = 4
        array_c_bh[x7] = 3
        array_c_bh[x8] = 2
        array_c_bh[x9] = 1
        array_c_bh[x10] = 1e+20

        array_c_bh = np.ma.masked_equal(array_c_bh, 1e+20)

        self.out_meta.update({'driver': 'GTiff',
                              'height': array_c_bh.shape[0],
                              'width': array_c_bh.shape[1],
                              'transform': self.trans_bh,
                              'count': 1,
                              'dtype': array_c_bh.dtype,
                              'nodata': 1e+20,
                              'crs': rasterio.crs.CRS.from_epsg(4326)})

        self.final_result = array_c_bh
        self.insar_rank = np.ma.array(array_c_sar, mask=array_c_bh.mask)

        self.showprocesslog("Automatic Classsification Done")

    def settings(self, nodialog=False):
        """
        Entry point into item.

        Parameters
        ----------
        nodialog : bool, optional
            Run settings without a dialog. The default is False.

        Returns
        -------
        bool
            True if successful, False otherwise.

        """
        # tst = self.indata['csv']

        # to check if the data is linked to this process
        if not nodialog:
            temp = self.exec_()
            if temp == 0:
                return False

        self.parent.process_is_active()

        flag = self.run()  # flag gets the database

        if not nodialog:
            self.parent.process_is_active(False)
            self.parent.pbar.to_max()
        return flag


class NumericDelegate(QtWidgets.QStyledItemDelegate):
    """
    Numeric delegate class, used to accept numbers only in the table.

    From https://stackoverflow.com/questions/63149168/how-to-accept-only-numeric-values-as-input-for-the-qtablewidget-disable-the-al
    """

    def createEditor(self, parent, option, index):
        """
        Create editor.

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.
        option : TYPE
            DESCRIPTION.
        index : TYPE
            DESCRIPTION.

        Returns
        -------
        editor : TYPE
            DESCRIPTION.

        """
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QtWidgets.QLineEdit):
            reg_ex = QtCore.QRegExp("[0-9]+.?[0-9]{,2}")
            validator = QtGui.QRegExpValidator(reg_ex, editor)
            editor.setValidator(validator)
        return editor


def _testfn():
    """Test routine."""
    import sys

    app = QtWidgets.QApplication(sys.argv)

    tmp = Monitoring(None)

    tmp.qfile['area_shp'].setText(r'C:/Workdata/AI_DOL/Carletonville_Area3.shp')
    tmp.qfile['stab_shp'].setText(r'C:/Workdata/AI_DOL/Four_Stability_points_SRTM_elevation.shp')
    tmp.qfile['insar'].setText(r'C:/Workdata/AI_DOL/sardd.tif')
    tmp.qfile['bhole'].setText(r'C:/Workdata/AI_DOL/FX_Carletonville_3_Boreholes.csv')

    tmp.tabs.setTabEnabled(1, True)
    tmp.tabs.setTabEnabled(2, True)

    tmp.settings()


if __name__ == "__main__":
    _testfn()
