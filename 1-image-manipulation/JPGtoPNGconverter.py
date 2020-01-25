# $ python JPGtoPNGconverter.py Pokedex/ new/
# First Argument: Source Folder of Images
# Second Argument: Output Folder of Images in PNG Format

import sys
import os
from PIL import Image

image_folder = sys.argv[1]
output_folder = sys.argv[2]

if not os.path.exists(output_folder):
    os.mkdir(output_folder)


for image in os.listdir(image_folder):
    image_to_png = Image.open(f'{image_folder}{image}')
    image_name = os.path.splitext(image)[0]
    image_to_png.save(f'{output_folder}{image_name}.png', 'png')
    print(f'Saved as PNG Image: \'{os.path.splitext(image)[0]}.png\'')
