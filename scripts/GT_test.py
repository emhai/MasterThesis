import json
import numpy as np
from scipy.spatial import ConvexHull


def load_transforms(json_path):
    """
    Load the transforms.json file and extract image filenames and positions.
    """
    with open(json_path, 'r') as f:
        data = json.load(f)

    images = []
    for frame in data['frames']:
        pose = np.array(frame['transform_matrix'])
        position = pose[:3, 3]  # Extract the translation part
        filename = frame['file_path'].split('/')[-1]  # Extract the image filename
        images.append({'filename': filename, 'position': position})

    return images


def calculate_pairwise_distances(images):
    """
    Compute the pairwise distances between all images based on positions.
    """
    positions = np.array([img['position'] for img in images])
    distances = np.linalg.norm(positions[:, None] - positions[None, :], axis=-1)
    return distances


def select_test_images(images, mode='linear'):
    """
    Select 3 test images based on spatial arrangement.
    Modes:
    - 'linear': Select 3 images farthest apart along one axis.
    - 'triangular': Select 3 images forming the largest triangle.
    """
    positions = np.array([img['position'] for img in images])
    if mode == 'linear':
        # Sort by the x-axis and select the first, middle, and last image
        sorted_indices = np.argsort(positions[:, 0])
        indices = [sorted_indices[0], sorted_indices[len(sorted_indices) // 2], sorted_indices[-1]]
    elif mode == 'triangular':
        # Use ConvexHull to find the outermost points and select the first 3
        hull = ConvexHull(positions)
        indices = hull.vertices[:3]  # First 3 vertices of the convex hull
    else:
        raise ValueError("Mode must be 'linear' or 'triangular'")

    return [images[i] for i in indices]


def find_ground_truth_images(test_images, images):
    """
    Find ground truth images that lie spatially between the test images.
    """
    test_positions = np.array([img['position'] for img in test_images])
    ground_truth_images = []

    for img in images:
        if img in test_images:
            continue

        position = img['position']
        # Check if the image is close to the line segments formed by test images
        # (Simplification: Check the distance to each line segment)
        is_between = False
        for i in range(len(test_positions)):
            for j in range(i + 1, len(test_positions)):
                start, end = test_positions[i], test_positions[j]
                segment_vec = end - start
                point_vec = position - start
                t = np.dot(point_vec, segment_vec) / np.dot(segment_vec, segment_vec)
                if 0 <= t <= 1:  # Check if the projection lies on the segment
                    projection = start + t * segment_vec
                    dist = np.linalg.norm(projection - position)
                    if dist < 0.1:  # Threshold for "in-between" (tune this as needed)
                        is_between = True
                        break
            if is_between:
                break

        if is_between:
            ground_truth_images.append(img)

    return ground_truth_images


def main():
    # Paths
    transforms_path = "/home/emmahaidacher/Masterthesis/MasterThesis/tests/nerf_flowers/colmap_images/transforms.json"

    # Load images and their positions
    images = load_transforms(transforms_path)

    # Select test images
    test_images = select_test_images(images, mode='linear')  # or mode='linear'

    # Find ground truth images
    ground_truth_images = find_ground_truth_images(test_images, images)

    # Output results
    print("Test Images:")
    for img in test_images:
        print(f" - {img['filename']}")

    print("\nGround Truth Images:")
    for img in ground_truth_images:
        print(f" - {img['filename']}")


if __name__ == "__main__":
    main()
