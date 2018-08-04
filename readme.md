# IR Data - Lepton 3.5, PureThermal 2, Raspbery Pi, Linux, Windows, Python, OpenCV, Matplotlib

# Raw Data Recording and Viewing

I wanted an infared camera that could be easily controlled remotely and could record raw data. The Lepton 3.5 along with the purethermal 2 board provided a lot of options integrated with a raspberry pi. Looking through Groupgets software GetThermal and purethermal1-uvc-capture, I was able to piece together two user interfaces combining opencv and matplotlib with pyqt4. 

The folder IR Data has the python script irdatavXX.X.py and a .ui file. IR Data is configured to run on a raspberry pi 3b+ at a 45% CPU usage (cv2.resize takes up too much resources on the pi).

### IR Data Abilities

- View IR Camera Stream
- Display Max and Min Temperatures
- Record Raw Data as HDF5 without overloading CPU
- Save Specific Filenames to Directories

The folder IR Data Viewer has the python script irDataViewervXX.py and another .ui file. IR Data Viewer is a post processing script designed to take in the binary .HDF5 files and process them into a matplotlib figure.

### IR Data Viewer Abilities

- View .HDF5 Recorded Raw Data in matplotlib format
- Save .AVI Files of specific length
- Save PNG Images
- Generate TIFF Files for further processing in Matlab or GNU Octave
- View Temperatures at any pixel on the frame
- Zoom in and analyze your data in depth
- Executable files are included for Linux and Windows Machines!

Special thanks to the developers of GetThermal and the Flir Community Forum.

## REVISION CHANGES

### IR Data

- v12 = Works, but crashes on pi
- v14 = Uses new .ui and doesn't crash on pi
- v15 = New save format
- v16 = Improvments all around

### IR Data Viewer

- v10 = Open and review .hdf5 files

## SYSTEM UPDATE/INSTALL PACKAGE COMMANDS

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

Make sure device is plugged into computer.

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

## Development

Install Qt Designer:

	sudo apt-get install qt4-designer

Or Qt Creator:

	sudo apt-get install qtcreator

## Helpful Links

- https://pythonspot.com/qt4-file-dialog/
- https://stackoverflow.com/questions/4286036/how-to-have-a-directory-dialog-in-pyqt
