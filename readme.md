# PureThermal 2, Lepton 3.5, Raw Data

## REVISION CHANGES

- v12 = Works, but crashes on pi
- v14 = Uses new .ui and doesn't crash on pi.
- v15 = New save format.

## SYSTEM UPDATE/INSTALL COMMANDS

Terminal Commands:

	sudo apt-get update
	sudo apt-get install python-qt4
	sudo apt-get install python-opencv
	sudo apt-get install python-tifffile 
	sudo apt-get install python-h5py
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

## RUNNING SCRIPT

Make sure device is plugged into computer.

Terminal Commands:

	sudo python irdatav15c.py

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
