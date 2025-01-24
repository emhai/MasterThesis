import numpy as np
import cv2
import os
import argparse
import utils

def run(path, width, height):

    path = path.rstrip("/")

    newImage = np.zeros((height, width, 3), np.uint8)
    cv2.imwrite(path, newImage, [cv2.IMWRITE_PNG_COMPRESSION, 0])


def main():
    """
    Takes path ../name/original_images, center crops images to given size (probably 1024x576) to fit to
    viewcrafters output and puts them to folder ../name/cropped_images
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=str, help='Path to the directory')
    parser.add_argument('width', type=int, help='Width of new image')
    parser.add_argument('height', type=int, help='Height of new image')
    # todo or parse other image and use that size

    args = parser.parse_args()
    run(args.path, args.width, args.height)

if __name__ == "__main__":
    main()