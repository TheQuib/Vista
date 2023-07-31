#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import logging

import epd7in5_V2

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

class ProgressBar:

    def draw_progress_bar(progress, x, y, bar_width, bar_height, image_width, image_height, padding=4, background_color=(50, 50, 50), bar_fill_color=(150, 150, 150), border_color=(50, 50, 50), border_width=4):
        # Create a new image with the given image_width and image_height
        logging.debug("Create image")
        image = Image.new('RGB', (image_width, image_height), (255,255,255))
        draw = ImageDraw.Draw(image)

        # Calculate the width of the progress bar based on the progress value
        logging.debug("Calculating progress size")
        filled_width = int((progress / 100) * (bar_width - 2 * padding))

        # Draw the border of the background of the progress bar
        logging.debug("Drawing border of bar background")
        background_coords = [(x + padding - border_width, y + padding - border_width),
                            (x + bar_width - padding + border_width - 1, y + bar_height - padding + border_width - 1)]
        draw.rounded_rectangle(background_coords, radius=(bar_height - 2 * padding) // 2, fill=background_color, outline=border_color, width=border_width)


        # Draw the background of the progress bar
        logging.debug("Drawing background of progress bar")
        background_coords = [(x + padding, y + padding), (x + bar_width - padding - 1, y + bar_height - padding - 1)]
        draw.rounded_rectangle(background_coords, radius=(bar_height - 2 * padding) // 2, fill=background_color)

        # Draw the filled portion of the progress bar
        logging.debug("Drawing progress bar")
        filled_coords = [(x + padding, y + padding), (x + filled_width + padding, y + bar_height - padding - 1)]
        draw.rounded_rectangle(filled_coords, radius=(bar_height - 2 * padding) // 2, fill=bar_fill_color)

        # Add text showing the progress percentage above the progress bar
        logging.debug("Drawing progress text")
        progress_text = f"{progress}%"
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=32)
        text_x = x
        text_y = y + bar_height
        draw.text((text_x, text_y), progress_text, font=font, fill=(0, 0, 0))

        # Return image
        return(image)

try:
    logging.info("Initializing and clearing EPD")
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    logging.info("Draw progress bar")
    bar = ProgressBar.draw_progress_bar(55, 75, 50, 300, 40, epd.width, epd.height)
    epd.display(epd.getbuffer(bar))

    logging.info("Set display to sleep")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()