#!/bin/bash

# Ensure the script is NOT run as root
if [ "$(id -u)" == "0" ]; then
   echo "This script should not be run as root or with sudo. Please run as your normal user." 1>&2
   exit 1
fi

# Define paths and names
INSTALL_DIR="/opt/vista"
SERVICE_NAME="vistaweb"
REFRESH_SCRIPT="main.py"
REBOOT_SCRIPT="boot.py"

# Stop the Flask app service
echo "Stopping the Flask app service..."
sudo systemctl stop ${SERVICE_NAME}.service

# Disable the Flask app service
echo "Disabling the Flask app service..."
sudo systemctl disable ${SERVICE_NAME}.service

# Remove the systemd service file
echo "Removing the systemd service file..."
sudo rm /etc/systemd/system/${SERVICE_NAME}.service
sudo systemctl daemon-reload

# Remove the cron jobs
echo "Removing the cron jobs for $REFRESH_SCRIPT..."
(crontab -l | grep -v -F "@reboot cd $INSTALL_DIR && /usr/bin/python3 $REBOOT_SCRIPT >> ~/vista.log 2>&1") | crontab -
(crontab -l | grep -v -F "*/5 * * * * cd $INSTALL_DIR && /usr/bin/python3 $REFRESH_SCRIPT >> ~/vista.log 2>&1") | crontab -

# Remove the installed project files
echo "Removing installed project files from $INSTALL_DIR..."
sudo rm -rf $INSTALL_DIR

echo "Uninstallation completed."
