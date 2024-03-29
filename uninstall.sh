#!/bin/bash

# Define paths and names
INSTALL_DIR="/opt/skystat"
SERVICE_NAME="skystatweb"
SCRIPT_NAME="main.py"

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
echo "Removing the cron jobs for $SCRIPT_NAME..."
(crontab -l 2>/dev/null | grep -v -F "$INSTALL_DIR/$SCRIPT_NAME") | crontab -

# Remove the installed project files
echo "Removing installed project files from $INSTALL_DIR..."
sudo rm -rf $INSTALL_DIR

echo "Uninstallation completed."
