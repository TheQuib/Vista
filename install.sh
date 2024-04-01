#!/bin/bash

# Ensure the script is NOT run as root
if [ "$(id -u)" == "0" ]; then
   echo "This script should not be run as root or with sudo. Please run as your normal user." 1>&2
   exit 1
fi


################
# DEPENDENCIES #
################

# Determine the directory in which the script resides
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Update package lists
echo "Updating package lists..."
sudo apt update

# Ensure Python is installed
if ! command -v /usr/bin/python &> /dev/null
then
    echo "Installing Python..."
    sudo apt-get install -y python3 python3-numpy libopenjp2-7-dev
else
    echo "Python is already installed."
fi

# Ensure Pip is installed
if ! command -v pip &> /dev/null
then
    echo "Installing Python-Pip..."
    sudo apt-get install -y python3-pip
else
    echo "Pip is already installed."
fi

# Ensure Python dependencies are installed
pip install -r $CURRENT_DIR/requirements.txt

# Check if 'dtparam=spi=on' exists and is uncommented
if grep -qE "^dtparam=spi=on$" "/boot/config.txt"
then
    echo "SPI interface is already enabled."
else
    # Ensure any existing 'dtparam=spi' line is commented out
    sudo sed -i 's/^\(dtparam=spi.*\)$/#\1/' "/boot/config.txt"
    
    # Add 'dtparam=spi=on' to the end of the file
    echo "Enabling SPI interface..."
    echo "dtparam=spi=on" | sudo tee -a "/boot/config.txt" > /dev/null
    $REBOOT_REQUIRED="true"
fi


###################
# VISTA INSTALL #
###################

# Define paths and names
SOURCE_DIR="$(dirname "$0")"
INSTALL_DIR="/opt/vista"
FLASK_APP="web.py"
REFRESH_SCRIPT="main.py"
REBOOT_SCRIPT="boot.py"
SERVICE_NAME="vistaweb"
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
sudo cp $SOURCE_DIR/boot.py $INSTALL_DIR
sudo cp $SOURCE_DIR/web.py $INSTALL_DIR
sudo cp $SOURCE_DIR/uninstall.sh $INSTALL_DIR
sudo chmod +x $INSTALL_DIR/main.py $INSTALL_DIR
sudo chmod +x $INSTALL_DIR/uninstall.sh $INSTALL_DIR
sudo chmod +x $INSTALL_DIR/boot.p $INSTALL_DIR

# Create systemd service file for Flask app
echo "Creating systemd service file for the Flask app..."
cat <<EOF | sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null
[Unit]
Description=Vista Web Service
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
echo "Creating a cron job for running at startup and every 5 minutes..."
CRON_JOB="@reboot cd $INSTALL_DIR && $PYTHON_PATH $REBOOT_SCRIPT >> ~/vista.log 2>&1\n*/5 * * * * cd $INSTALL_DIR && $PYTHON_PATH $REFRESH_SCRIPT >> ~/vista.log 2>&1"
(crontab -l 2>/dev/null | grep -v -F "$INSTALL_DIR/$REFRESH_SCRIPT"; echo -e "$CRON_JOB") | crontab -

echo "Installation completed."


################
# POST INSTALL #
################
# Check if reboot is required
if [ "$REBOOT_REQUIRED" = "true" ]
then
    # Ask for reboot
    read -p "SPI interface enabled. Reboot now to apply changes? (y/n) " answer

    case $answer in
        [Yy]* )
            echo "Rebooting now..."
            sudo reboot
            ;;
        [Nn]* )
            echo "Please reboot the system manually to apply SPI interface changes."
            ;;
        * )
            echo "Invalid response. Please reboot the system manually to apply SPI interface changes."
            ;;
    esac
else
    # Ask the user if they want to run main.py now
    read -p "Do you want to push information to the display now? (y/n) " answer

    case $answer in
        [Yy]* )
            echo "Pushing..."
            $PYTHON_PATH "$INSTALL_DIR/$REFRESH_SCRIPT"
            ;;
        [Nn]* )
            echo "Not pushing changes. You can push manually by execution $INSTALL_DIR/$REFRESH_SCRIPT"
            ;;
        * )
            echo "Please answer yes (y) or no (n)."
            ;;
    esac
fi