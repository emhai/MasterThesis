import argparse
import json
import itertools
import numpy as np
import os
from scipy.spatial import ConvexHull
from shutil import copyfile


def point_in_triangle(p, triangle):

    v0 = triangle[1] - triangle[0]
    v1 = triangle[2] - triangle[0]
    v2 = p - triangle[0]

    # Cross products
    cross1 = np.cross(v0, v1)
    cross2 = np.cross(v0, v2)
    cross3 = np.cross(v1, v2)

    # Check if the sign of all cross products is the same, meaning the point is inside
    # todo, with wiggle room
    inside = np.all(np.sign(cross1) == np.sign(cross2)) and np.all(np.sign(cross2) == np.sign(cross3))
    return inside


def run(path):

    output_dir = "output_images"
    with open(path, 'r') as f:
        transforms = json.load(f)

    cameras = transforms['frames']

    camera_combinations = itertools.combinations(cameras, 3)

    for combo in camera_combinations:
        positions = [camera['position'] for camera in combo]
        triangle = np.array(positions)

        inside_cameras = []
        for camera in cameras:
            if point_in_triangle(camera['position'], triangle):
                inside_cameras.append(camera)

        if inside_cameras:
            continue
            # save in dataframe, which ground truth, which test.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to transforms.json')

    args = parser.parse_args()
    path = args.path

    run(path)


if __name__ == "__main__":
    main()
