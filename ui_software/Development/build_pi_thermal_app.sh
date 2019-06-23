#!/usr/bin/env bash
#File created by Jerry Pierre  

install_thermal_dependencies(){

    echo "updating system."
    sudo apt-get update
    sudo apt-get dist-upgrade -y --autoremove

    echo "Installing thermal dependencies."
    sudo apt-get install -y python3-pyqt5
    sudo apt-get install -y python3-h5py
    sudo apt-get install -y python3-psutil
    sudo pip3 install opencv-contrib-python
    sudo pip3 install --no-cache-dir tifffile
    sudo apt-get install -y python3-matplotlib
    sudo apt-get install -y libatlas-base-dev
    sudo apt-get install -y libjasper-dev
    sudo apt-get install -y libqtgui4
    sudo apt-get install -y libqt4-test
}

install_thermal_app(){

    echo "Installing and building thermal app."
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

    sudo sh -c "echo 'SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"1e4e\", ATTRS{idProduct}==\"0100\", SYMLINK+=\"pt1\", GROUP=\"usb\", MODE=\"666\"' > /etc/udev/rules.d/99-pt1.rules"

}

main () {

    install_thermal_dependencies
    install_thermal_app
}

main "$@"
