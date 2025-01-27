# This script was used to invert the colors of the icons so that Google Earth Pro can apply a color tint to the icon to indicate the damage level.
# Black pixels are inverted to white while retaining transparency.

import os
from PIL import Image

def invert_image_colors(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)

            # Open the image
            with Image.open(input_image_path) as img:
                # Convert image to RGBA if not already in that mode
                img = img.convert("RGBA")
                # Create a new image for the inverted colors
                inverted_img = Image.new("RGBA", img.size)

                # Invert colors while retaining transparency
                for x in range(img.width):
                    for y in range(img.height):
                        r, g, b, a = img.getpixel((x, y))
                        if a > 0:  # Only invert if the pixel is not fully transparent
                            inverted_img.putpixel((x, y), (255 - r, 255 - g, 255 - b, a))
                        else:
                            inverted_img.putpixel((x, y), (r, g, b, a))  # Keep transparent pixels unchanged

                # Save the inverted image
                inverted_img.save(output_image_path)
                print(f'Inverted: {filename}')

# Example usage
input_folder = './icons'  # Replace with your input folder path
output_folder = './inverted_icons'  # Replace with your desired output folder path
invert_image_colors(input_folder, output_folder)