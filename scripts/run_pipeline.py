import os
import resource

import run_colmap
import visualize_cameras
import main

def run():
    path = "/home/emmahaidacher/Desktop/full_datasets/finito2"

    for folder in os.listdir(path):
        print("Running {}".format(folder))
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)

        main.run(os.path.join(path, folder), folder)

        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        cpu_time = usage_end.ru_utime - usage_start.ru_utime
        print("CPU time: {} minutes".format(cpu_time / 60))



if __name__ == "__main__":
    run()