import argparse
import shutil
import utils
import re
import os
import json
import numpy as np

def calculate_translation_distance(trans1, trans2):
    """Calculate the Euclidean distance between two translation vectors."""
    return np.linalg.norm(np.array(trans1) - np.array(trans2))

def strip_to_numerals(name):
    return ''.join(re.findall(r'\d+', name))

def load_camera_poses(file_path):
    """Load camera poses from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def run(transforms_path, cameras_path):
    transforms_cameras = load_camera_poses(transforms_path)
    interpolated_cameras = load_camera_poses(cameras_path)

    closest_matches = []

    for cam_a in interpolated_cameras:
        min_distance = float('inf')
        closest_cam = None

        for cam_b in transforms_cameras:
            distance = calculate_translation_distance(cam_a['translation'], cam_b['translation'])

            if distance < min_distance:
                min_distance = distance
                closest_cam = cam_b

        closest_matches.append({
            'camera_a': cam_a,
            'closest_camera_b': closest_cam,
            'distance': min_distance
        })
    return

def main():
    """
    Takes path to transforms.json and the interpolated cameras and finds closest matches.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('transforms_path', type=utils.dir_path, help='Path to transforms.json')
    parser.add_argument('cameras_path', type=utils.dir_path, help='Path to cameras.json')

    args = parser.parse_args()
    run(args.transforms_path, args.cameras_path)


if __name__ == "__main__":
    main()
