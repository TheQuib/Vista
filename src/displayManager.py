#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import logging

from . import epd7in5_V2

from PIL import Image,ImageDraw,ImageFont

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(
            __file__
        )
    )
)

epd = epd7in5_V2.EPD()

logging.basicConfig(level=logging.DEBUG)

class DisplayManager:

    def __init__(self, image_width=epd.width, image_height=epd.height):
        self.image = Image.new('RGB', (image_width, image_height), (255,255,255))
        self.draw = ImageDraw.Draw(self.image)

    def draw_progress_bar(self, progress, x, y, bar_width, bar_height, padding=4, background_color=(50, 50, 50), bar_fill_color=(150, 150, 150), border_color=(50, 50, 50), border_width=4):
        logging.debug("Calculating progress size")
        filled_width = int((progress / 100) * (bar_width - 2 * padding))

        logging.debug("Drawing border of bar background")
        background_coords = [(x + padding - border_width, y + padding - border_width),
                             (x + bar_width - padding + border_width - 1, y + bar_height - padding + border_width - 1)]
        self.draw.rounded_rectangle(background_coords, radius=(bar_height - 2 * padding) // 2, fill=background_color, outline=border_color, width=border_width)

        logging.debug("Drawing background of progress bar")
        background_coords = [(x + padding, y + padding), (x + bar_width - padding - 1, y + bar_height - padding - 1)]
        self.draw.rounded_rectangle(background_coords, radius=(bar_height - 2 * padding) // 2, fill=background_color)

        logging.debug("Drawing progress bar")
        filled_coords = [(x + padding, y + padding), (x + filled_width + padding, y + bar_height - padding - 1)]
        self.draw.rounded_rectangle(filled_coords, radius=(bar_height - 2 * padding) // 2, fill=bar_fill_color)

        logging.debug("Drawing progress text")
        progress_text = f"{progress}%"
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=32)
        text_x = x
        text_y = y + bar_height
        self.draw.text((text_x, text_y), progress_text, font=font, fill=(0, 0, 0))