# Parabilis Thermal
Parabilis Space Technologies Thermal Imaging Software

### Recording Abilities:
- View the Flir Lepton 9 Hz Stream
- Display Max and Min Temperatures (F or C)
- Record Raw Data as HDF5 without overloading raspberry pi CPU
- Save to Specific Filenames and Directories
- Be Controlled Wirelessly using RealVNC

### Post Processing Abilities:
- View .HDF5 Recorded Raw Data in matplotlib format
- Save .AVI Files of specific length
- Save PNG Images
- Generate TIFF Files for further processing in MATLAB or GNU Octave
- View Temperatures at any pixel on the frame
- Zoom in and analyze your data in depth

### Required Components:
- Flir Lepton 3.5
- PureThermal2 Interface Board (With USB Cord)
- Raspberry Pi 3
- Raspberry Pi 3 Power Supply
- Display with Keyboard/Mouse Control

### Software Primary Dependencies:
- Python 3
- PyQt5
- OpenCV
- libuvc

## Raspberry Pi Setup
Plug Raspberry Pi into HDMI display and connect keyboard/mouse. Must have Rasbian Stretch installed onto SD Card. Connect the Raspberry Pi to your local network/WiFi and open linux terminal to perform following terminal commands.

### System Update/Upgrade:
```
  sudo apt-get update
  sudo apt-get upgrade
  sudo apt-get dist-upgrade
```
### Required Packages:
```
  sudo apt-get install python3-pyqt5
  sudo apt-get install python3-h5py
  sudo apt-get install python3-psutil
  sudo apt-get install python3-matplotlib

  sudo pip3 install opencv-contrib-python
  sudo pip3 install --no-cache-dir tifffile

  sudo apt-get install libatlas-base-dev
  sudo apt-get install libjasper-dev
  sudo apt-get install libqtgui4
  sudo apt-get install libqt4-test

  sudo apt-get install libusb-1.0-0-dev
  sudo apt-get install build-essential
```
You may need to use pip or pip3 to install some of these packages.

### Software:
```
  cd Documents
  git clone https://github.com/Kheirlb/purethermal1-uvc-capture.git
  cd purethermal1-uvc-capture
  cd ui_software
  git clone https://github.com/groupgets/libuvc
  sudo apt-get install cmake
  cd libuvc
  mkdir build
  cd build
  cmake ..
  make && sudo make install
  sudo ldconfig -v
  cd ../..
```
### USB Permissions:
```
  sudo sh -c "echo 'SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"1e4e\", ATTRS{idProduct}==\"0100\", SYMLINK+=\"pt1\", GROUP=\"usb\", MODE=\"666\"' > /etc/udev/rules.d/99-pt1.rules"
```
### Wireless Control Enable:
```
  sudo raspi-config
  - Interfacing Options
  -- VNC
  --- Yes
```
Download VNC Viewer from RealVNC onto desired computer. Use the raspberrypi IP address to connect. The IP address is assigned when the raspberry pi is connected to your local network/WiFi.

## Run Software
Navigate to ui_software/Parabilis_Thermal and run desired version:
```
sudo python3 RecordIR_XX.X.py
```
or
```
sudo python3 PostProcessIR_vXX.py
```
## Additional Comments:
Special thanks to Parabilis Space Technologies, the developers of GroupGets GetThermal and purethermal1-uvc-capture, and the Flir Community Forum who helped me achieve my goals in this project.
