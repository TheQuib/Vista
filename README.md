# Vista
Scrapes data from the HughesNet usage page, displays on a Waveshare 7.5" e-ink display (epd7in5) and opens a web server for display management.

# Requirements
 - Raspberry Pi Zero, 3, 4
 - Waveshare 7.5" e-ink display (V2)

# Install
## With included installer script
You can install everything by running:
```bash
cd ~
git clone https://github.com/thequib/vista
cd vista
chmod +x install.sh
./install.sh
```


## Manual installation
Alternatively, you can install this manually

### Install prerequisite packages
```bash
sudo apt update
sudo apt install python3 python3-pip python3-numpy libopenjp2-7-dev
```

### Install Python dependencies
```bash
pip install -r requirements.txt
```

### Enable the Pi's SPI interface
#### Using sed and tee
```bash
# Ensure any existing 'dtparam=spi' line is commented out
sudo sed -i 's/^\(dtparam=spi.*\)$/#\1/' "/boot/config.txt"
# Add 'dtparam=spi=on' to the end of the file
echo "dtparam=spi=on" | sudo tee -a "/boot/config.txt" > /dev/null
```

#### Using `sudo raspi-config`
  - Enter `sudo raspi-config`
  - Choose option *3*, **Interface Options**
  - Choose option *I4*, **SPI**
  - `Left-arrow` to **Yes**, and hit enter
  - `Right-arrow` *twice* to **Finish**, and hit enter


### Copy project files
```bash
cd ~
mkdir /opt/vista
sudo cp -r vista/* /opt/vista
```

### Create service for web app (optional)
```bash
# Create service file
cat <<EOF | sudo tee /etc/systemd/system/vistaweb.service > /dev/null
[Unit]
Description=Vista Web Service
After=network.target

[Service]
User=pi
WorkingDirectory=/opt/vista
ExecStart=/usr/bin/python /opt/vista/web.py

Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start app
sudo systemctl daemon-reload
sudo systemctl enable vistaweb.service
sudo systemctl start vistaweb.service
```

### Create cron job for the script to run every `x` minutes
#### Via command one-liner
```bash
CRON_JOB="@reboot cd /opt/vista && /usr/bin/python3 boot.py >> ~/vista.log 2>&1\n*/5 * * * * cd /opt/vista && /usr/bin/python main.py >> ~/vista.log 2>&1"
(crontab -l 2>/dev/null | grep -v -F "/opt/vista/main.py"; echo -e "$CRON_JOB") | crontab -
```

#### Manually
Open the crontab:
```bash
crontab -e
# Select your preferred text editor, default is Nano (1)
```

Enter the following
```
@reboot cd /opt/vista && /usr/bin/python3 boot.py >> ~/vista.log 2>&1\
*/5 * * * * cd /opt/vista && /usr/bin/python main.py >> ~/vista.log 2>&1"
```

Save the file

# Uninstall
## With included uninstaller script
You can uninstall everything automatically by running:
```bash
cd /opt/vista
# If you installed manually, you will need to run:
#sudo chmod +x uninstall.sh
./uninstall.sh
```

## Manual uninstallation
### Stop and remove the web service
This is only required if you installed the web service

```bash
sudo systemctl stop vistaweb.service
sudo systemctl disable vistaweb.service
sudo rm /etc/systemd/system/vistaweb.service
sudo systemctl daemon-reload
```

### Remove the cron jobs
#### Via command two-liner
```bash
(crontab -l | grep -v -F "@reboot cd $INSTALL_DIR && /usr/bin/python3 $REBOOT_SCRIPT >> ~/vista.log 2>&1") | crontab -
(crontab -l | grep -v -F "*/5 * * * * cd $INSTALL_DIR && /usr/bin/python3 $REFRESH_SCRIPT >> ~/vista.log 2>&1") | crontab -
```

#### Manually
Open the crontab:
```bash
crontab -e
# Select your preferred text editor, default is Nano (1)
```

Remove the following
```
@reboot cd /opt/vista && /usr/bin/python3 boot.py >> ~/vista.log 2>&1\
*/5 * * * * cd /opt/vista && /usr/bin/python main.py >> ~/vista.log 2>&1"
```

Save the file

### Remove the project files
```bash
sudo rm -rf /opt/vista
```



# Useful resources
 - [[Waveshare] 7.5inch e-Paper HAT Manual](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)
   - [Working with Raspberry Pi](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi)
 - [[Waveshare] Raspberry Pi Guides for SPI e-Paper](https://www.waveshare.com/wiki/Template:Raspberry_Pi_Guides_for_SPI_e-Paper)
 - [[Waveshare - Github] Repository with examples](https://github.com/waveshare/e-Paper)