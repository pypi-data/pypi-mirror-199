# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
from robin_sd_download.supportive_scripts import logger


def install_sshpass():
    try:
        subprocess.run(["sshpass", "-V"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("sshpass is already installed.")
    except subprocess.CalledProcessError:
        print("sshpass not found. Attempting to install...")
        try:
            if sys.platform.startswith("linux"):
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install",
                               "-y", "sshpass"], check=True)
                print("sshpass installed successfully.")
            else:
                print(
                    "Unsupported platform for sshpass installation. Please install sshpass manually.")
                return
        except subprocess.CalledProcessError as e:
            print(f"Error during sshpass installation: {e}")
            return


def get_remote_ip():
    try:
        detected_ip = subprocess.check_output(
            ['hostname', '-I']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        detected_ip = None

    if detected_ip:
        user_confirmation = input(
            f"Detected target IP address is {detected_ip}. Is this correct? (yes/no): ").strip().lower()
        if user_confirmation == 'yes':
            return detected_ip

    remote_ip = input("Please enter the IP address of the target device: ")
    return remote_ip


def check_web_servers():
    """
    Check if Nginx or Apache is running on the device.
    """
    nginx_process = subprocess.run(
        ["pgrep", "nginx"], capture_output=True, text=True)
    apache_process = subprocess.run(
        ["pgrep", "apache2"], capture_output=True, text=True)

    if nginx_process.returncode == 0:
        logger.log(message="Nginx is running on this device.",
                   log_level="info", to_terminal=True)
    elif apache_process.returncode == 0:
        logger.log(message="Apache is running on this device.",
                   log_level="info", to_terminal=True)
    else:
        logger.log(message="Neither Nginx nor Apache is running on this device.",
                   log_level="error", to_terminal=True)


def offline_install():
    """Installs the software on the remote machine.

    Returns:
        bool: True if the software was successfully installed, False otherwise.
    """
    # Check if Nginx or Apache is running on this device
    # check_web_servers()

    # # Try to find remote IP of target device, or prompt user to enter it
    # remote_ip = get_remote_ip()

    # # Prompt user to enter username for remote device
    # remote_username = input(
    #     "Please enter the username for the target device: ")

    # # prompt user to enter pass for remote device
    # remote_pass = input(
    #     "Please enter the password for the target device: ")

    # # Check if sshpass is installed (install this , when downloading the robin_sd_download package -> sudo apt-get install sshpass)
    # install_sshpass()

    # Create /home/robin/temp/ folder

    # Unzip the files in the temp folder

    # Copy unzipped download folder to remote system (from /home/robin/temp/)
    # subprocess.run(['sudo', 'sshpass', '-p', remote_pass, 'scp', '-o', 'StrictHostKeyChecking=no', '-o',
    #                'UserKnownHostsFile=/dev/null', zipfile_path, f'{remote_username}@{remote_ip}:/home/{remote_username}/'], check=True)

    # Create backup folder at /home/robin/backup

    # Make backups
    # -> create new folder in backup folder with current date
    # -> copy all files from /etc/apt/sources.list to backup folder
    # -> copy all files from /etc/apt/sources.list.d/ to backup folder

    # Add apt-keys in temp folder to remote system (cuda, robin.pub)

    # Should We Run an Update?

    # Run selected options...

    # Running Cleanup
