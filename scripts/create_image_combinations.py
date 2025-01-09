def create_new_folders(folder_path):
    before = [*range(35, 45)]
    after = [*range(55, 45, -1)]

    for i in range(len(before)):
        folder_name = f"test{before[i]}to{after[i]}"
        new_folder_path = os.path.join(folder_path, folder_name)
        os.mkdir(new_folder_path)
        first_file_name = str(before[i]) + ".JPG"
        second_file_name = str(after[i]) + ".JPG"
        shutil.copyfile(folder_path + "/" + first_file_name, new_folder_path + "/" + first_file_name)
        shutil.copyfile(folder_path + "/" + second_file_name, new_folder_path + "/" + second_file_name)

