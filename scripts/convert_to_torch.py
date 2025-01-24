"""
Builds on https://github.com/cvg/depthsplat/blob/main/src/scripts/convert_dl3dv_test.py
and  https://github.com/cvg/depthsplat/blob/main/src/scripts/generate_dl3dv_index.py
"""


import argparse
import os
import utils
import torch
import numpy as np
import json

def load_metadata(transforms_path):
    blender2opencv = np.array(
        [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
    )

    url = str(transforms_path).split("/")[-3]
    # todo, just name
    with open(transforms_path, "r") as f:
        meta_data = json.load(f)

    store_h, store_w = meta_data["h"], meta_data["w"]
    fx, fy, cx, cy = (
        meta_data["fl_x"],
        meta_data["fl_y"],
        meta_data["cx"],
        meta_data["cy"],
    )
    saved_fx = float(fx) / float(store_w)
    saved_fy = float(fy) / float(store_h)
    saved_cx = float(cx) / float(store_w)
    saved_cy = float(cy) / float(store_h)

    timestamps = []
    cameras = []
    opencv_c2ws = []  # will be used to calculate camera distance

    for frame in meta_data["frames"]:
        timestamps.append(
            int(os.path.basename(frame["file_path"]).split(".")[0].split("_")[-1])
        )
        camera = [saved_fx, saved_fy, saved_cx, saved_cy, 0.0, 0.0]
        # transform_matrix is in blender c2w, while we need to store opencv w2c matrix here
        opencv_c2w = np.array(frame["transform_matrix"])  @ blender2opencv
        opencv_c2ws.append(opencv_c2w)
        camera.extend(np.linalg.inv(opencv_c2w)[:3].flatten().tolist())
        cameras.append(np.array(camera))

    # timestamp should be the one that match the above images keys, use for indexing
    timestamps = torch.tensor(timestamps, dtype=torch.int64)
    cameras = torch.tensor(np.stack(cameras), dtype=torch.float32)

    return {"url": url, "timestamps": timestamps, "cameras": cameras}


def run(colmap_path, resolution, output_path):

    key = os.path.basename(os.path.dirname(colmap_path.strip("/")))
    images_path = os.path.join(colmap_path, resolution)
    images = {}

    for filename in os.listdir(images_path):
        name, extension = os.path.splitext(filename)
        name = int(name.split("_")[-1])
        file_path = os.path.join(images_path, filename)
        raw = torch.tensor(np.memmap(file_path, dtype="uint8", mode="r"))
        images[name] = raw

    transforms_path = os.path.join(colmap_path, "transforms.json")
    chunk = load_metadata(transforms_path)
    chunk["images"] = [
        images[timestamp.item()] for timestamp in chunk["timestamps"]
    ]

    chunk["key"] = key

    torch_chunk = [chunk]
    torch_filename = "000000.torch"
    torch.save(torch_chunk, os.path.join(output_path, torch_filename))
    index = {key: torch_filename}

    with open(os.path.join(output_path, "index.json"), 'w') as f:
        json.dump(index, f)

def main():
    """
    Takes path ../name/colmap_images and converts the images_8 folder to one big torch file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('colmap_path', type=utils.dir_path, help='Path to the ..name/mvsplat360/colmap')
    parser.add_argument('output_path', type=utils.dir_path, help='Path to the ..name/mvsplat360/input/test')
    parser.add_argument("resolution", type=str, default="images_8", help='images_8, images, ... whichever')

    args = parser.parse_args()
    run(args.colmap_path, args.resolution, args.output_path)

if __name__ == "__main__":
    main()