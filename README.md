# hughesnet-usage-scraper
Scrapes data from the HughesNet usage page and displays to a Waveshare 7.5" e-ink display

# Requirements
 - Raspberry Pi Zero, 3, 4
 - Waveshare 7.5" e-ink display

# Setup
## Raspberry Pi
### Install prerequisites:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-pil python3-numpy
```

### Configurations
 - Enable SPI interface
   - Enter `sudo raspi-config`
   - Choose option *3*, **Interface Options**
   - Choose option *I4*, **SPI**
   - `Left-arrow` to **Yes**, and hit enter
   - `Right-arrow` *twice* to **Finish**, and hit enter


# Useful links
[[Waveshare] Raspberry Pi Guides for SPI e-Paper](https://www.waveshare.com/wiki/Template:Raspberry_Pi_Guides_for_SPI_e-Paper)