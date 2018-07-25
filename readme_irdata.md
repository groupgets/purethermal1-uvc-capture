#UPDATES
	sudo apt-get update
	sudo apt-get install python-qt4
	sudo apt-get install python-opencv
	sudo apt-get install python-tifffile 
	sudo apt-get install git
	sudo apt-get update && sudo apt-get install build-essential

#GITHUB
	cd Documents
	cd mkdir Lepton
	cd Lepton
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

#FYI
Might have to run .py files as sudo (admin)

All Raw Data is Save to Same Directory as .PY

Use .m script and Octave GNU to process .tiff raw data files.