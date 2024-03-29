#!/bin/bash

# Ensure the script is NOT run as root
if [ "$(id -u)" == "0" ]; then
   echo "This script should not be run as root or with sudo. Please run as your normal user." 1>&2
   exit 1
fi

# Define paths and names
SOURCE_DIR="$(dirname "$0")"
INSTALL_DIR="/opt/skystat"
FLASK_APP="web.py"
SCRIPT_NAME="main.py"
SERVICE_NAME="skystatweb"
PYTHON_PATH="/usr/bin/python3"  # Change this if you're using a virtualenv

# Copy project files to the install directory
echo "Copying project files to $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR
sudo cp -r $SOURCE_DIR/assets $INSTALL_DIR
sudo cp -r $SOURCE_DIR/src $INSTALL_DIR
sudo cp $SOURCE_DIR/drawImage.py $INSTALL_DIR
sudo cp $SOURCE_DIR/example.html $INSTALL_DIR
sudo cp $SOURCE_DIR/facts.json $INSTALL_DIR
sudo cp $SOURCE_DIR/main.py $INSTALL_DIR
sudo cp $SOURCE_DIR/web.py $INSTALL_DIR
sudo chmod +x $INSTALL_DIR/main.py $INSTALL_DIR

# Create systemd service file for Flask app
echo "Creating systemd service file for the Flask app..."
cat <<EOF | sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null
[Unit]
Description=Skystat Flask Web Service
After=network.target

[Service]
User=pi
WorkingDirectory=$INSTALL_DIR
ExecStart=$PYTHON_PATH $INSTALL_DIR/$FLASK_APP

Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Get IP address of wlan0 interface
IP_ADDRESS=$(ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

# Enable and start the Flask app service
echo "Enabling and starting the Flask app service on http://$IP_ADDRESS:5000..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service
sudo systemctl start ${SERVICE_NAME}.service

# Create a combined cron job for the script
echo "Creating a cron job for $SCRIPT_NAME to run at startup and every 5 minutes..."
CRON_JOB="@reboot $PYTHON_PATH $INSTALL_DIR/$SCRIPT_NAME >> $INSTALL_DIR/main.log 2>&1\n*/5 * * * * $PYTHON_PATH $INSTALL_DIR/$SCRIPT_NAME >> $INSTALL_DIR/main.log 2>&1"
(crontab -l 2>/dev/null | grep -v -F "$INSTALL_DIR/$SCRIPT_NAME"; echo -e "$CRON_JOB") | crontab -

echo "Installation completed."

# Ask the user if they want to run main.py now
read -p "Do you want to push information to the display now? (y/n) " answer

case $answer in
    [Yy]* )
        echo "Pushing..."
        $PYTHON_PATH "$INSTALL_DIR/$SCRIPT_NAME"
        ;;
    [Nn]* )
        echo "Not pushing changes. You can run it later by executing $PYTHON_PATH $INSTALL_DIR/$SCRIPT_NAME"
        echo "or by rebooting / waiting 5 minutes."
        ;;
    * )
        echo "Please answer yes (y) or no (n)."
        ;;
esac