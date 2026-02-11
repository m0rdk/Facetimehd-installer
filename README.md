# FaceTimeHD DKMS Installer

This is NOT the driver.

This is a Python script that automates the installation of the FaceTimeHD camera
for MacBooks running Linux using DKMS.

Original driver:
https://github.com/patjak/bcwc_pcie

## Features
- Installs firmware
- Installs driver using DKMS
- Survives kernel updates

## Requirements
- Debian/Ubuntu/Mint
- DKMS
- Kernel headers
- Git

## Usage

```bash
chmod +x install_camera_facetimehd.py
sudo python3 install_camera_facetimehd.py
