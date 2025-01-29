import math
import json
import re

import numpy as np
import argparse
import seaborn as sns

def strip_to_numerals(name):
    # probably unnecessary because files are 001 to ....
    name = ''.join(re.findall(r'\d+', name))
    name = f"{int(name):03}"
    return name

def calc_distance(translation1, translation2):
    return math.sqrt((translation2[0] - translation1[0]) ** 2 + (translation2[1] - translation1[1]) ** 2 + (
            translation2[2] - translation1[2]) ** 2)


def run(transform_path, results_path):
    with open(transform_path, 'r') as f:
        data = json.load(f)

    with open(results_path, 'r') as f:
        results_data = json.load(f)

    all_frames = data['frames']

    matrices = {}

    for i, frame in enumerate(all_frames):
        transformation_matrix = frame['transform_matrix']
        name = strip_to_numerals(frame['file_path'])
        translation = [transformation_matrix[0][3], transformation_matrix[1][3], transformation_matrix[2][3]]
        i = f"{i:03}"
        matrices[i] = {"name": name, "translation": translation}

    for framework in ["viewcrafter", "mvsplat360"]:
        for result in results_data[framework]:
            indices = result.split(".")[0].split("_")
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    first_name = indices[i]
                    second_name = indices[j]
                    first_translation = matrices[first_name]["translation"]
                    second_translation = matrices[second_name]["translation"]

                    distance = calc_distance(first_translation, second_translation)
                    results_data[framework][result][f"distance_{first_name}_{second_name}"] = distance
                    # print(indices[i], indices[j], distance)

    with open(results_path, 'w') as f:
        json.dump(results_data, f, indent=4)



def main():
    """
    Takes path to transform.json and calculates distances
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('transforms_path', type=str, help='Path to transforms.json')
    parser.add_argument('results_path', type=str, help='Path to results.json')

    args = parser.parse_args()
    transforms_path = args.transforms_path
    results_path = args.results_path

    run(transforms_path, results_path)


if __name__ == "__main__":
    main()

