"""
This is a Python script for plotting in real time data of the MPU9250 which are collected on a com port
@author : Mohamed SANA
@contact : Follow me on github.com/Sanahm/
@licence : Under GNU licence
@date : 30/04/2017
"""

import serial
import time
import numpy as np
import matplotlib
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

matplotlib.use('Qt5Agg')
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# initialization of Qt
app = QtGui.QApplication([])

# Define a top-level widget to hold everything
main_window = QtGui.QWidget()
main_window.setWindowTitle('MPU9250 features acquisition')
# w.resize(1366,768)
child_window = QtGui.QWidget(main_window)
graphic_window = pg.GraphicsWindow()

# Globals
pause = False
k = 1


def click_handle():
    global pause
    pause = not pause
    if pause:
        QtGui.QLineEdit.setText(text, 'Pause')
    else:
        QtGui.QLineEdit.setText(text, 'running...')


def quit_handle():
    main_window.close()


def save_handle():
    """
    Data between cursors can be save automatically by clicking on this button
    Here is how to save data of screen 12 by using "lr12"
    """
    global k
    QtGui.QLineEdit.setText(text, "datas have been saved!")
    edge = lr11.getRegion()
    edge = (int(edge[0]), int(edge[1]))
    data = np.zeros((10, edge[1] - edge[0]))
    data[0:3, :] = data1[:, edge[0]:edge[1]]
    data[3:6, :] = data2[:, edge[0]:edge[1]]
    data[6:9, :] = data3[:, edge[0]:edge[1]]
    data[9] = tps[edge[0]:edge[1]] - tps[0]
    np.savetxt("./SavedData/data" + str(k) + ".csv", data, delimiter=',')
    k += 1

# Create some widgets to be placed inside
pause_btn = QtGui.QPushButton('Pause/Resume')
quit_btn = QtGui.QPushButton('Quit')
save_btn = QtGui.QPushButton('Save')
pause_btn.clicked.connect(click_handle)
quit_btn.clicked.connect(quit_handle)
save_btn.clicked.connect(save_handle)
text = QtGui.QLineEdit('Enter text')

namespace = {'pg': pg, 'np': np}
texts = """
This is an interactive python console. The numpy and pyqtgraph modules have already been imported 
as 'np' and 'pg'. 

Go, play.
"""


def configure_layout():
    global layout_child_window, layout_main_window
    # Create a grid layout to manage the widgets size and position
    layout_child_window = QtGui.QGridLayout()
    child_window.setLayout(layout_child_window)
    # child_window.setFixedW(main_window.width() / 10)
    layout_main_window = QtGui.QGridLayout()
    main_window.setLayout(layout_main_window)


configure_layout()

# Add widgets to the layout in their proper positions
layout_child_window.addWidget(pause_btn, 0, 0)  # button goes in upper-left
layout_child_window.addWidget(quit_btn, 0, 1)
layout_child_window.addWidget(save_btn, 0, 2)

layout_main_window.addWidget(child_window, 0, 0)  # plot goes on right side, spanning 3 rows
layout_main_window.addWidget(graphic_window, 1, 0)

# Display the widget as a new window
main_window.show()
graphic_window.setFrameStyle(2)

# screens are numerated like this: lr11 means first ligne and first column
lr11 = pg.LinearRegionItem(values=[30, 80])
lr21 = pg.LinearRegionItem(values=[30, 80])
lr31 = pg.LinearRegionItem(values=[30, 80])

# the idea of scrolling plot is to define a matrix of data with fix length and to
# update it each time you receive data

# here the length is set to 300. 3 means the 3-dimension.
data1 = np.zeros((3, 300));  # contains acc_x, acc_y and acc_z

p11 = graphic_window.addPlot()
p11.addLegend(offset=(10, 10))
p11.addItem(lr11, name='region11')
label = pg.InfLineLabel(lr11.lines[0], "x2={value:0.2f}", position=0.9, rotateAxis=(1, 0), anchor=(1, 1))
label = pg.InfLineLabel(lr11.lines[1], "x1={value:0.2f}", position=0.9, rotateAxis=(1, 0), anchor=(1, 1))
graphic_window.nextRow()

p21 = graphic_window.addPlot()
p21.addLegend(offset=(10, 10))
p21.addItem(lr21, name='region21')
graphic_window.nextRow()

p31 = graphic_window.addPlot()
p31.addLegend(offset=(10, 10))
p31.addItem(lr31, name='region31')

curve11 = p11.plot(data1[0], pen=(0, 3), name='acc[x]')
curve21 = p21.plot(data1[1], pen=(1, 3), name='acc[y]')
curve31 = p31.plot(data1[2], pen=(2, 3), name='acc[z]')

com = '/dev/cu.usbmodem14101'
speed = 9600
start = time.time()
try:
    serie = serial.Serial(com, speed)
except:
    print("An error occured: unable to open the specified port " + com)
    exit(0)

tps = np.zeros(300)  # you need time to, the same lenght as data
if not (serie.readable()):
    print("unable to read available value on port\n" + com)


def update():
    global data1, curve11, data2, curve21, data3, curve31
    line = str(serie.readline()[:-3], 'ascii')
    if not pause:
        acc = []
        line = line.split("\t")

        # for each line I collect data like this "acc_x acc_y acc_z gyr_x ... mag_z"
        tab = [float(i) for i in line]

        acc = tab[0:3]  # read and store the 3 values of acc according to how you send your data from arduino
        tps[:-1] = tps[1:]
        tps[-1] = time.time() - start
        data1[:, :-1] = data1[:, 1:]  # shift data in the array one sample left
        data1[:, -1] = acc
        curve11.setData(data1[0])
        curve21.setData(data1[1])
        curve31.setData(data1[2])

# timer = pg.QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start(20)

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

#    acc = np.array(acc)
#    gyr = np.array(gyr)
#    mag = np.array(mag)
# plt.plot(tps,acc[:,0])
# plt.show()
# serie.close()
