import os

# todo if necessary
input_folder_name = "input"
output_folder_name = "output"
input_images_prefix = "in"
output_images_prefix = "out"

# https://stackoverflow.com/questions/38834378/path-to-a-directory-as-argparse-argument
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
