# IR Data - Lepton 3.5, PureThermal 2, Raspbery Pi, Linux, Ubuntu, Windows, Python, OpenCV, Matplotlib, VNC, Wireless Control

# Raw Data Recording and Viewing

I wanted an infared camera that could be easily controlled remotely from a PC and could record raw IR data. The Lepton 3.5 along with the purethermal 2 (PT2) board provided a lot of options integrated with a raspberry pi. Looking through Groupgets software GetThermal and purethermal1-uvc-capture, I was able to piece together two user interfaces, IR Data and IR Data Viewer, combining opencv and matplotlib with pyqt4.

### IR Data Abilities

The folder IR Data has the python script irdatavXX.X.py and a .ui file.

- View IR Camera Stream
- Display Max and Min Temperatures
- Record Raw Data as HDF5 without overloading raspberry pi CPU
- Save Specific Filenames to Directories

Screenshot of IR Data Software

![Alt text](/images/irDataStreaming.png?raw=true)

You can notice in the above Screenshot the pixelation of the IR images; this is because it is being resized from 120X160 to 480x640 using Qt's resize function only, the cv2 resize function is commented out. IR Data is configured to run on a raspberry pi 3b+ at a 45% CPU usage (cv2.resize takes up too much resources on the pi). If you are running on a stronger computer, simply uncomment the cv2.resize function from irDatav16.5.py script.

In order to control the IR Camera wirelessly, I was able to use a VNC Session between a PC computer and the raspberry pi connected to the same network (WIFI). Follow the below link to learn how to control your raspberry pi wirelessly. 

https://www.realvnc.com/en/raspberrypi/

Unfortunately, Perform FFC and changing Gain Modes features are still unavailable. If anyone wants to help me develop these features, please reach out to me or take it on yourself.

### IR Data Viewer Abilities

The folder IR Data Viewer has the python script irDataViewervXX.py and another .ui file. IR Data Viewer is a post processing script designed to take in the binary .HDF5 files and process them into a matplotlib figure for analysis.

- View .HDF5 Recorded Raw Data in matplotlib format
- Save .AVI Files of specific length
- Save PNG Images
- Generate TIFF Files for further processing in MATLAB or GNU Octave
- View Temperatures at any pixel on the frame
- Zoom in and analyze your data in depth
- Executable files are included for Linux and Windows Machines!

Screenshot of IR Data Viewer Software

![Alt text](/images/irDataViewerSelected.png?raw=true)

Special thanks to the developers of GetThermal and the Flir Community Forum who helped me achieve my goals in this project.

I purchased the Lepton 3.5 and PT2 from the below link:

https://groupgets.com/manufacturers/getlab/products/purethermal-2-flir-lepton-smart-i-o-module

## REVISION CHANGES

### IR Data

- v12 = Works, but crashes on pi
- v14 = Uses new .ui and doesn't crash on pi
- v15 = New save format
- v16 = Improvments all around

### IR Data Viewer

- v10 = Open and review .hdf5 files

## SYSTEM UPDATE/INSTALL PACKAGE COMMANDS FOR IR DATA

If you have not already, please connect your pi or linux computer to the internet and open up the terminal.

Terminal Commands:

	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get dist-upgrade
	sudo apt-get install python-qt4
	sudo apt-get install python-opencv
	sudo apt-get install python-tifffile
	sudo apt-get install python-h5py
	sudo apt-get install python-psutil
	sudo apt-get install git
	sudo apt-get install libusb-1.0-0-dev
	sudo apt-get install libusb-1.0
	sudo apt-get install build-essential

## GITHUB

Terminal Commands:

	cd Documents
	git clone https://github.com/Kheirlb/purethermal1-uvc-capture.git
	cd purethermal1-uvc-capture
	cd python
	git clone https://github.com/groupgets/libuvc
	sudo apt-get install cmake
	cd libuvc
	mkdir build
	cd build
	cmake ..
	make && sudo make install
	sudo ldconfig -v
	cd ../..

## RUNNING IR Data .PY SCRIPT

Make sure the PT2 is plugged into computer.

Terminal Commands:

	cd IR_Data
	sudo python irdatavXX.X.py

## RUNNNING IR Data Viewer .PY SCRIPT - Post Processing Script

Terminal Commands:

	cd IR_Data_Viewer
	sudo python irDataViewervXX.py

Or As An Executable:

	irDataViewervXX

There is also a windows executable for IR Data Viewer.

## FYI

Might have to run .py files as sudo (admin)

## Old FYI for Previous Versions

- v12:
	- All Raw Data is Save to Same Directory as .PY
	- Use .m script and Octave GNU to process .tiff raw data files.

## UI Development

If you would like to change the user interface and do more development of your own, I used Qt Designer.

Install Qt Designer:

	sudo apt-get install qt4-designer

Or Qt Creator:

	sudo apt-get install qtcreator

## Helpful Links

- https://pythonspot.com/qt4-file-dialog/
- https://stackoverflow.com/questions/4286036/how-to-have-a-directory-dialog-in-pyqt
