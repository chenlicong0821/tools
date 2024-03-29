import os
import json


def list_subdirectories(directory_path):
    subdirectories = [d for d in os.listdir(directory_path) if os.path.isdir(
        os.path.join(directory_path, d)) and not d.startswith('.')]
    subdirectories_sorted = sorted(subdirectories)
    folder_list = [{"path": d} for d in subdirectories_sorted]
    return folder_list


if __name__ == "__main__":
    directory_path = input("请输入目录路径：")
    if os.path.isdir(directory_path):
        folders = list_subdirectories(directory_path)
        result = {"folders": folders}
        print(json.dumps(result, indent=4))
    else:
        print("输入的路径不是一个有效的目录。")
