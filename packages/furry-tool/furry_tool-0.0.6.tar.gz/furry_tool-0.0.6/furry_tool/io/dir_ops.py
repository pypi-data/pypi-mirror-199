import os


def get_dir_files_by_asb_filename(path: str):
    """
    取得path目录下的所有文件的绝对路径，并返回数组
    :param path: 目录路径
    :return:
    """
    # 将相对路径path转换为绝对路径
    dir_path = os.path.abspath(path)
    dirs = [dir_path]
    files = []
    for dir in dirs:
        files.extend(
            [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        )
    return files