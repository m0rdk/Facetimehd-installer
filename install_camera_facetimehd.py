#!/usr/bin/env python3
import os
import subprocess
import sys

BCWC_REPO_URL = "https://github.com/patjak/bcwc_pcie.git"
FW_REPO_URL = "https://github.com/patjak/facetimehd-firmware.git"

REPO_DIR = os.path.expanduser("~/facetimehd")
BCWC_DIR = os.path.join(REPO_DIR, "bcwc_pcie")
FW_DIR = os.path.join(REPO_DIR, "facetimehd-firmware")

os.makedirs(REPO_DIR, exist_ok=True)

MODULE_NAME = "facetimehd"
MODULE_VERSION = "0.6.13"

def run(cmd, cwd=None):
    print(">>>", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def clone_repo(url, path):
    if not os.path.isdir(path):
        run(["git", "clone", url, path])
    else:
        run(["git", "pull"], cwd=path)

def ensure_dependencies():
    kernel = os.uname().release
    run(["sudo", "apt", "update"])
    run([
        "sudo", "apt", "install", "-y",
        "dkms",
        "build-essential",
        f"linux-headers-{kernel}",
        "git"
    ])

def install_firmware():
    clone_repo(FW_REPO_URL, FW_DIR)
    run(["make"], cwd=FW_DIR)
    run(["sudo", "make", "install"], cwd=FW_DIR)

def dkms_exists():
    result = subprocess.run(
        ["dkms", "status"],
        text=True,
        capture_output=True
    )
    return f"{MODULE_NAME}/{MODULE_VERSION}" in result.stdout

def install_driver_dkms():
    clone_repo(BCWC_REPO_URL, BCWC_DIR)

    dkms_conf = os.path.join(BCWC_DIR, "dkms.conf")
    if not os.path.isfile(dkms_conf):
        print("dkms.conf not found")
        sys.exit(1)

    if not dkms_exists():
        run(["sudo", "dkms", "add", "."], cwd=BCWC_DIR)

    run(["sudo", "dkms", "build", f"{MODULE_NAME}/{MODULE_VERSION}"])
    run(["sudo", "dkms", "install", f"{MODULE_NAME}/{MODULE_VERSION}"])

def load_module():
    run(["sudo", "modprobe", MODULE_NAME])

def main():
    ensure_dependencies()
    install_firmware()
    install_driver_dkms()
    load_module()
    print("Camera should be ready.")

if __name__ == "__main__":
    main()
