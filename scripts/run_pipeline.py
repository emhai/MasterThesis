import os
import resource
import subprocess

import run_colmap
import visualize_cameras
import main
import gc
import torch

def run():
    path = "/home/emmahaidacher/Desktop/full_datasets/finito"

    for folder in os.listdir(path):
        print("###################################################")
        print("RUNNING {}".format(folder))
        print("###################################################")
        subprocess.run("nvidia-smi", shell=True)
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
        try:
            main.run(os.path.join(path, folder), f"small_{folder}")
        except Exception as e:
            print("###################################################")
            print(f"Error processing {folder}: {e}")
            print("###################################################")

        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu_time = usage_end.ru_utime - usage_start.ru_utime
        subprocess.run("nvidia-smi", shell=True)
        print("CPU time: {} minutes".format(cpu_time / 60))

        torch.cuda.empty_cache()
        gc.collect()

        print("###################################################")
        print("SUCCESS {}".format(folder))
        print("###################################################")


if __name__ == "__main__":
    run()