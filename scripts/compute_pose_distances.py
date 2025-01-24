import math
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
import seaborn as sns

from numpy.ma.extras import average


def run(path):

    with open(path, 'r') as f:
        data = json.load(f)

    mean = 0
    amount = 0
    last_translation = 0
    last_name = 0
    distances = []
    for frame in data['frames']:
        transform_matrix = np.array(frame['transform_matrix'])
        name = frame["file_path"].split(".")[0].split("_")[-1]
        if int(name) < 200 or int(name) > 260:
            continue
        translation = [transform_matrix[0][3], transform_matrix[1][3], transform_matrix[2][3]]
        if last_translation == 0:
            last_translation = translation
            last_name = name
            continue
        dist = math.sqrt((last_translation[0] - translation[0])**2 + (last_translation[1] - translation[1])**2 + (last_translation[2] - translation[2])**2)
        distances.append(dist)
        mean += dist
        amount += 1
        print(f"Dist between {last_name} and {name} = {dist}")
        last_translation = translation
        last_name = name

    average_mean = mean / amount
    print(f"Average distance {average_mean}")
    sns.boxplot(distances)
    plt.show()


def main():
    """
    Takes path to transform.json and calculates distances
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to transforms.json')

    args = parser.parse_args()
    path = args.path

    run(path)


if __name__ == "__main__":
    main()

