#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import logging
import time

import driver.epd7in5_V2 as epd7in5_V2

from PIL import Image,ImageDraw,ImageFont

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(
            __file__
        )
    )
)

picdir = __location__ + "/assets"
logging.basicConfig(level=logging.DEBUG)

def draw_progress_bar(x, y, image_width, image_height, bar_width, bar_height, progress, padding, background_color, bar_fill_color, border_color, border_width):
    # Create a new image with the given image_width and image_height
    image = Image.new('RGB', (image_width, image_height), (255,255,255))
    draw = ImageDraw.Draw(image)

    # Calculate the width of the progress bar based on the progress value
    filled_width = int((progress / 100) * (bar_width - 2 * padding))

    # Draw the border of the background of the progress bar
    background_coords = [(x + padding - border_width, y + padding - border_width),
                         (x + bar_width - padding + border_width - 1, y + bar_height - padding + border_width - 1)]
    draw.rounded_rectangle(background_coords, radius=(bar_height - 2 * padding) // 2, fill=background_color, outline=border_color, width=border_width)


    # Draw the background of the progress bar
    background_coords = [(x + padding, y + padding), (x + bar_width - padding - 1, y + bar_height - padding - 1)]
    draw.rounded_rectangle(background_coords, radius=(bar_height - 2 * padding) // 2, fill=background_color)

    # Draw the filled portion of the progress bar
    filled_coords = [(x + padding, y + padding), (x + filled_width + padding, y + bar_height - padding - 1)]
    draw.rounded_rectangle(filled_coords, radius=(bar_height - 2 * padding) // 2, fill=bar_fill_color)

    # Add text showing the progress percentage above the progress bar
    progress_text = f"{progress}%"
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=32)
    text_x = x
    text_y = y + bar_height
    draw.text((text_x, text_y), progress_text, font=font, fill=(0, 0, 0))

    image = image.transpose(Image.ROTATE_180)

    # Return image
    return(image)

try:
    logging.info("epd7in5_V2 Test")
    epd = epd7in5_V2.EPD()

    logging.info("Initialize and Clear")
    epd.init()
    epd.Clear()

    logging.info("Draw progress bar")
    bar = draw_progress_bar(50, 50, epd.width, epd.height, 300, 40, 55, 4, (50, 50, 50), (150, 150, 150), (50, 50, 50), 4)
    epd.display(epd.getbuffer(bar))

    logging.info("Set display to sleep")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()