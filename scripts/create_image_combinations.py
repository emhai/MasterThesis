import argparse
import shutil

import utils
import re
import os

def strip_to_numerals(name):
    return ''.join(re.findall(r'\d+', name))

def run(path):
    path = path.rstrip("/")
    filenames = [f for f in os.listdir(path)]
    filenames.sort()
    len_filenames = len(filenames)
    for i in range(len(filenames) // 2):
        name1 = strip_to_numerals(filenames[i])
        name2 = strip_to_numerals(filenames[len_filenames - 1 - i])
        folder_name = f"test{name1}x{name2}"
        folder_path = os.path.join(os.path.dirname(path), "tests", folder_name)
        os.makedirs(folder_path)
        shutil.copyfile(os.path.join(path, filenames[i]), os.path.join(folder_path, filenames[i]))
        shutil.copyfile(os.path.join(path, filenames[len_filenames - 1 - i]), os.path.join(folder_path, filenames[len_filenames - 1 - i]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=utils.dir_path, help='Path to the directory')

    args = parser.parse_args()
    run(args.path)

if __name__ == "__main__":
    main()