from PIL import Image, ImageOps
import os
import argparse
import utils

def run(path, width, height):

    size = (width, height)

    print(f"Cropping images {os.path.join(path)}")

    for path, dirs, files in os.walk(path):
        for file in files:
            image_path = os.path.join(path, file)
            image = Image.open(image_path)
            file_name = os.path.basename(image_path)

            image = ImageOps.fit(image, size, method=Image.LANCZOS, centering=(0.5, 0.5))
            image.save(os.path.join(path, file_name))

def main():
    """
    Takes path ../name/original_images, center crops images to given size (probably 1024x576) to fit to
    viewcrafters output and puts them to folder ../name/cropped_images
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=utils.dir_path, help='Path to the directory')
    parser.add_argument('width', type=int, help='Width of new image')
    parser.add_argument('height', type=int, help='Height of new image')
    # todo or parse other image and use that size

    args = parser.parse_args()
    path = args.path.rstrip("/")
    run(path, args.width, args.height)

if __name__ == "__main__":
    main()