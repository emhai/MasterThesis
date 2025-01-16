import os
import json
import numpy as np
import matplotlib.pyplot as plt
import argparse

def run(path):

    with open(path, 'r') as f:
        data = json.load(f)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    cameras = []

    for frame in data['frames']:
        transform_matrix = np.array(frame['transform_matrix'])
        rotation_matrix = transform_matrix[:3, :3]
        forward_vector = -rotation_matrix[:, 2]  # Negative Z-axis
        forward_vector = forward_vector / np.linalg.norm(forward_vector)  # Normalize
        position = transform_matrix[:3, 3]
        full_image_path = os.path.join(frame['file_path'])
        cameras.append((position, forward_vector, full_image_path))
        ax.scatter(position[0], position[1], position[2], c='blue', label='Camera', alpha=0.3)
        ax.quiver(position[0], position[1], position[2],
                  forward_vector[0], forward_vector[1], forward_vector[2],
                  length=0.5, color='red')


    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Camera Poses ")

    # plt.show()
    plt.savefig(os.path.join(os.path.dirname(path), "cameras.jpg"))
    plt.close()


def main():
    """
    Takes path to transform.json and creates visualizations of the camera poses
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to transforms.json')

    args = parser.parse_args()
    path = args.path

    run(path)


if __name__ == "__main__":
    main()

