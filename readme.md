# Parabilis Thermal
Parabilis Space Technologies Thermal Imaging Software

### Recording Abilities:
- View the Flir Lepton 9 Hz Stream
- Display Max and Min Temperatures (F or C)
- Record Raw Data as HDF5 without overloading raspberry pi CPU
- Save to Specific Filenames and Directories
- Be Controlled Wirelessly using RealVNC
- Stable Build: RecordIR_v18.3.py

![Record IR Screenshot](/images/RecordIR.jpg?raw=true)

### Post Processing Abilities:
- View .HDF5 Recorded Raw Data in matplotlib format
- Save .AVI Files of specific length
- Save PNG Images
- Generate TIFF Files for further processing in MATLAB or GNU Octave
- View Temperatures at any pixel on the frame
- Zoom in and analyze your data in depth
- Stable Build: PostProcessIR_v11.py

![Post Process IR Screenshot](/images/PostProcessIR.jpg?raw=true)

### Required Components:
- Flir Lepton 3.5
- PureThermal2 Interface Board (With USB Cord)
- Raspberry Pi 3
- Raspberry Pi 3 Power Supply
- Display with Keyboard/Mouse Control

### Software Primary Dependencies:
- Rasbian Stretch
- Python 3
- PyQt5
- OpenCV
- libuvc

## Raspberry Pi Setup
Plug Raspberry Pi into HDMI display and connect keyboard/mouse. Must have Rasbian Stretch installed onto SD Card. Connect the Raspberry Pi to your local network/WiFi and open linux terminal to run build script or perform following terminal commands.

## Build Script
Big shout out to Jerry Pierre for creating a simply and easy to use raspberry pi build script which condenses all of the terminal commands into a simple shell script. Simply copy/save the build_pi_thermal_app.sh file in this repository to your raspberry pi and perform the following two commands in the terminal. The raspberry pi update/upgrade can take 15+ minutes and the package/software download & installation will take approximately 5 minutes.
```
sudo chmod 775 build_pi_thermal_app.sh
sudo ./build_pi_thermal_app.sh
```

## Terminal Commands
If the build script does not work or you wish to do things manually, you can use the following terminal commands.

### System Update/Upgrade:
```
  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt-get dist-upgrade -y --autoremove
```
### Required Packages:
```
  sudo apt-get install -y python3-pyqt5
  sudo apt-get install -y python3-h5py
  sudo apt-get install -y python3-psutil
  sudo apt-get install -y python3-matplotlib

  sudo pip3 install opencv-contrib-python
  sudo pip3 install --no-cache-dir tifffile

  sudo apt-get install -y libatlas-base-dev
  sudo apt-get install -y libjasper-dev
  sudo apt-get install -y libqtgui4
  sudo apt-get install -y libqt4-test
```
You may need to alternate using pip, pip3, or apt-get to install some of these packages.

### Software:
```
  cd Documents
  git clone https://github.com/Kheirlb/purethermal1-uvc-capture.git
  git clone https://github.com/groupgets/libuvc
  sudo apt-get install cmake -y
  sudo apt-get install libusb-1.0-0-dev -y
  sudo apt-get install libjpeg-dev -y
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

If you used the build script, then RecordIR_XX.X.py was created as an executable using chmod +x and can now be double-clicked to run.

## Additional Comments:
Special thanks to Parabilis Space Technologies, Jerry Pierre, the developers of GroupGets GetThermal and purethermal1-uvc-capture, and the Flir Community Forum who helped me achieve my goals in this project.
