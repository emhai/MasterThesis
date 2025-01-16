from PIL import Image, ImageOps
import os
import argparse
import utils

def run(path, width, height):

    path = path.rstrip("/")
    size = (width, height)

    new_folder_path = os.path.join(os.path.dirname(path), "cropped_images")
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)


    print(f"Cropping images {os.path.join(path)}")

    for path, dirs, files in os.walk(path):
        for file in files:
            # todo this works but I could use viewcrafters center_crop_image
            image_path = os.path.join(path, file)
            image = Image.open(image_path)
            file_name = os.path.basename(image_path)

            image = ImageOps.fit(image, size, method=Image.LANCZOS, centering=(0.5, 0.5))
            image.save(os.path.join(new_folder_path, file_name))

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
    run(args.path, args.width, args.height)

if __name__ == "__main__":
    main()