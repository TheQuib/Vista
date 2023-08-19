# SkyStat
Scrapes data from the HughesNet usage page, displays on a Waveshare 7.5" e-ink display (epd7in5) and opens a web server for display management.

# Requirements
 - Raspberry Pi Zero, 3, 4
 - Waveshare 7.5" e-ink display (V2)

# Setup
## Raspberry Pi
### Install prerequisites:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-numpy libopenjp2-7-dev
python3 -m pip install Pillow
```

### Check to make sure `spi` is enabled
```bash
cat /boot/config.txt | grep spi
# Should return:
# dtparam=spi=on
```

### Configurations
 - Enable SPI interface
   - Enter `sudo raspi-config`
   - Choose option *3*, **Interface Options**
   - Choose option *I4*, **SPI**
   - `Left-arrow` to **Yes**, and hit enter
   - `Right-arrow` *twice* to **Finish**, and hit enter


# Useful links
 - [[Waveshare] 7.5inch e-Paper HAT Manual](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)
   - [Working with Raspberry Pi](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi)
 - [[Waveshare] Raspberry Pi Guides for SPI e-Paper](https://www.waveshare.com/wiki/Template:Raspberry_Pi_Guides_for_SPI_e-Paper)
 - [[Waveshare - Github] Repository with examples](https://github.com/waveshare/e-Paper)