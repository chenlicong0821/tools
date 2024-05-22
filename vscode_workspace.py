import os
import sys
import json


def is_go_repository(directory):
    """
    判断一个目录是否是Go的仓库。
    """
    go_mod_path = os.path.join(directory, "go.mod")
    return os.path.isfile(go_mod_path)


def is_python_repository(directory, is_root):
    # 检查目录是否存在
    if not os.path.isdir(directory):
        return False

    # 遍历目录中的文件和一级子目录
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # 如果是文件并且以.py结尾
        if os.path.isfile(item_path):
            if item.endswith(".py"):
                return True
        # 如果不是根目录，则遍历一级子目录
        elif os.path.isdir(item_path) and not is_root:
            for subdir_item in os.listdir(item_path):
                subdir_item_path = os.path.join(item_path, subdir_item)
                if os.path.isfile(subdir_item_path) and subdir_item.endswith(".py"):
                    return True

    # 如果目录中没有找到任何Python文件或特定的项目文件，则返回False
    return False


def create_vscode_workspace(directory, workspace_name, subdirectories):
    if not subdirectories:
        print(f"No subdirectories to add in the workspace: {workspace_name}")
        return
    workspace_path = os.path.join(directory, f"{workspace_name}.code-workspace")
    subdirectories_sorted = sorted(subdirectories)
    folder_list = [{"path": d} for d in subdirectories_sorted]
    with open(workspace_path, "w") as f:
        workspace_data = {"folders": folder_list}
        json.dump(workspace_data, f, indent=4)
        print(f"Created Visual Studio Code workspace: {workspace_name}")


def traverse_and_create_workspaces(root_dir):
    # 使用转换为绝对路径
    abs_dir = os.path.abspath(root_dir)
    base_dir = os.path.basename(abs_dir)
    # 使用字典来跟踪需要遍历的目录
    dirs_to_visit = {abs_dir: True}
    go_dirs = []
    py_dirs = []
    is_repo = False
    while dirs_to_visit:
        # 获取字典的第一个键
        current_dir = next(iter(dirs_to_visit))
        is_root = dirs_to_visit[current_dir]
        del dirs_to_visit[current_dir]
        print(f"Current directory: {current_dir}")
        # 判断当前目录是否是Go项目
        if is_go_repository(current_dir):
            # 将Go项目添加到需要创建工作空间的集合中
            go_dirs.append(os.path.basename(current_dir))
            is_repo = True
        # 判断当前目录是否是Python项目
        if is_python_repository(current_dir, is_root):
            # 将Python项目添加到需要创建工作空间的集合中
            py_dirs.append(os.path.basename(current_dir))
            is_repo = True
        if is_repo:
            continue
        # 如果不是代码仓库，则遍历其子目录
        for subdir in os.listdir(current_dir):
            # 忽略以 . 开头的子目录
            if subdir.startswith("."):
                continue
            subdir_path = os.path.join(current_dir, subdir)
            if os.path.isdir(subdir_path):
                # 将子目录添加到需要遍历的集合中
                dirs_to_visit[subdir_path] = False

    workspace_name_go = f"{base_dir}_Go"
    workspace_name_py = f"{base_dir}_Py"
    # 创建Visual Studio Code工作空间
    create_vscode_workspace(abs_dir, workspace_name_go, go_dirs)
    create_vscode_workspace(abs_dir, workspace_name_py, py_dirs)


if __name__ == "__main__":
    directory_path = sys.argv[1] if len(sys.argv) > 1 else input(" 请输入目录路径：")
    # 使用函数，传入你想要遍历的目录路径
    traverse_and_create_workspaces(directory_path)
