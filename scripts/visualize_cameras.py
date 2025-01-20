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
        forward_vector = -rotation_matrix[:, 2]
        forward_vector = forward_vector / np.linalg.norm(forward_vector)
        position = transform_matrix[:3, 3]
        full_image_path = os.path.join(frame['file_path'])
        filename = os.path.basename(full_image_path)
        cameras.append((position, forward_vector, full_image_path))

        camera_size = 0.2
        x_offset = np.array([camera_size, -camera_size, -camera_size, camera_size])
        y_offset = np.array([camera_size, camera_size, -camera_size, -camera_size])
        z_offset = np.zeros(4)

        corners = np.vstack((x_offset, y_offset, z_offset)).T
        corners = (rotation_matrix @ corners.T).T + position

        for i in range(4):
            next_idx = (i + 1) % 4
            ax.plot(
                [corners[i, 0], corners[next_idx, 0]],
                [corners[i, 1], corners[next_idx, 1]],
                [corners[i, 2], corners[next_idx, 2]],
                c='blue'
            )

        # ax.scatter(position[0], position[1], position[2], c='blue', alpha=0.3)
        ax.quiver(position[0], position[1], position[2],
                  forward_vector[0], forward_vector[1], forward_vector[2],
                  length=0.4, color='red', alpha=0.6)
        ax.text(position[0], position[1], position[2], filename.split("_")[-1].split(".")[0], color='black', size=5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Camera Poses")

    plt.savefig(os.path.join(os.path.dirname(path), "cameras.jpg"), dpi=300, bbox_inches='tight')
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

