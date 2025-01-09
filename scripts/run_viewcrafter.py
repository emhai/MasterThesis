import argparse
import subprocess
import utils
import os


def run(path):

    for path, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(path, file))

    # https://stackoverflow.com/questions/16180414/how-to-execute-a-shell-script-through-python
    process = subprocess.Popen(['abc.sh', name, filename1, filname2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()  # Wait for process to complete.

    # iterate on the stdout line by line
    for line in process.stdout.readlines():
        print(line)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=utils.dir_path, help='Path to the directory')
    args = parser.parse_args()
    run(args.path)

if __name__ == "__main__":
    main()