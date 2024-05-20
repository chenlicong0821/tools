import os
import subprocess


def pull_git_repos_in_directory(directory):
    # 使用集合来跟踪需要遍历的目录
    dirs_to_visit = {directory}

    while dirs_to_visit:
        current_dir = dirs_to_visit.pop()
        print(f"Current directory: {current_dir}")
        # 检查当前目录是否包含.git子目录，这表示它是一个Git仓库
        if os.path.exists(os.path.join(current_dir, '.git')):
            # print(f"Git directory: {current_dir}")
            working_dir = os.getcwd()
            # 切换到当前目录
            os.chdir(current_dir)

            try:
                # 执行 git remote -v 命令
                # subprocess.check_call(['git', 'remote', '-v'])
                # 切换到develop分支
                # subprocess.check_call(['git', 'checkout', 'develop'])
                # 执行git pull命令
                subprocess.check_call(['git', 'pull'])
                print(f"Git pull successful in {current_dir}")
            except subprocess.CalledProcessError as e:
                # 如果git pull失败，则打印错误信息
                print(f"Git pull failed in {current_dir}: {e}")

            # 切换回原始工作目录，以防当前目录被修改影响后续操作
            os.chdir(working_dir)
        else:
            # 如果不是Git仓库，则遍历其子目录
            for subdir in os.listdir(current_dir):
                if subdir.startswith('.'):
                    continue
                subdir_path = os.path.join(current_dir, subdir)
                if os.path.isdir(subdir_path):
                    # 将子目录添加到需要遍历的集合中
                    dirs_to_visit.add(subdir_path)


# 使用函数，传入你想要遍历的目录路径
pull_git_repos_in_directory('/Users/xxx/Documents/code/xxx')
