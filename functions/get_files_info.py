import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    if not os.path.isdir(directory):
        return f"Error: \"{directory}\" is not a directory"
    data_list = []
    for item in os.listdir(target_dir):
        name_str = item
        size_str = os.path.getsize(target_dir + "/" + item)
        is_dir_str = os.path.isdir(target_dir + "/" + item)
        data_list.append((name_str, size_str, is_dir_str))
    ret_string = ""
    for item in data_list:
        ret_string += f"- {item[0]}: file_size={item[1]}, is_dir={item[2]}" + "\n"
    return ret_string
    

