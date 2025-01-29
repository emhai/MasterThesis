from scipy.spatial.distance import euclidean
import numpy as np
from itertools import combinations
import pandas as pd
import json

# Helper function to calculate if a point is within or near a triangle
def is_point_near_triangle(point, triangle, error_margin=1e-3):
    """
    Check if a point is near or on a triangle in 3D space within an error margin
    and respects the hemispherical constraint.

    :param point: The point to check (numpy array of shape (3,)).
    :param triangle: The three vertices of the triangle (numpy array of shape (3, 3)).
    :param error_margin: Allowed error margin for proximity.
    :return: True if the point is near or on the triangle and in the hemisphere, False otherwise.
    """
    # Triangle vertices
    v1, v2, v3 = triangle

    # Compute the triangle's normal vector
    normal = np.cross(v2 - v1, v3 - v1)
    normal = normal / np.linalg.norm(normal)  # Normalize

    # Compute the centroid of the triangle
    centroid = (v1 + v2 + v3) / 3

    # Check the point's hemisphere (relative to the triangle)
    point_vector = point - centroid
    if np.dot(point_vector, normal) < -error_margin:
        return False  # The point lies in the opposite hemisphere

    # Compute distances from the point to the triangle's edges and plane
    plane_distance = abs(np.dot(normal, point - v1))  # Perpendicular distance to the plane
    if plane_distance <= error_margin:
        # If near the plane, check proximity to edges
        def point_to_edge_distance(p, a, b):
            ap = p - a
            ab = b - a
            projection = np.dot(ap, ab) / np.dot(ab, ab)
            closest_point = a + np.clip(projection, 0, 1) * ab
            return euclidean(p, closest_point)

        edge_distances = [
            point_to_edge_distance(point, v1, v2),
            point_to_edge_distance(point, v2, v3),
            point_to_edge_distance(point, v3, v1),
        ]
        print(min(edge_distances) <= error_margin)
        return min(edge_distances) <= error_margin

    return False

# Parse the transforms.json file
def parse_transforms_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    cameras = []
    for frame in data["frames"]:
        transform_matrix = np.array(frame["transform_matrix"])
        position = transform_matrix[:3, 3]  # Extract camera position
        cameras.append({
            "position": position,
            "image_path": frame["file_path"]
        })

    return cameras

# Main function to find camera triplets and check for inclusions
def find_camera_triplets_with_inclusions(cameras, error_margin=1e-3):
    results = []

    # Get all combinations of three cameras
    triplets = combinations(range(len(cameras)), 3)

    for triplet in triplets:
        indices = list(triplet)
        triangle = np.array([cameras[i]["position"] for i in indices])
        included_cameras = []

        # Check all other cameras
        for i, camera in enumerate(cameras):
            if i not in indices:  # Exclude the cameras forming the triangle
                if is_point_near_triangle(camera["position"], triangle, error_margin):
                    included_cameras.append(i)

        # Save the result if one or more cameras are inside or near
        if included_cameras:
            results.append({
                "triplet": indices,
                "included_cameras": included_cameras,
                "image_paths": [cameras[i]["image_path"] for i in indices]
            })

    return results

# Save results to a DataFrame
def save_to_dataframe(results):
    df = pd.DataFrame(results)
    return df

# Example usage
def main():
    # File path to the transforms.json file
    file_path = "/home/emmahaidacher/Desktop/full_datasets/processed_vasedeck_all/transforms.json"

    # Parse the file
    cameras = parse_transforms_json(file_path)

    # Find triplets with included cameras
    results = find_camera_triplets_with_inclusions(cameras, error_margin=1e-3)

    # Save to DataFrame
    df = save_to_dataframe(results)

    # Output the DataFrame
    print(df)
    # Optionally save the DataFrame to a CSV file
    df.to_csv("camera_triplets_with_inclusions.csv", index=False)

if __name__ == "__main__":
    main()
