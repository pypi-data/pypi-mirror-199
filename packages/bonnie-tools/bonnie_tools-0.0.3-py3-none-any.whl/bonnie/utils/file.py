import os


def add_suffix_to_filename(src_file: str, suffix: str) -> str:
    # 获取文件路径、文件名和扩展名
    file_path, file_name = os.path.split(src_file)
    name, ext = os.path.splitext(file_name)
    # 拼接新的文件名并返回
    new_name = name + suffix + ext
    return os.path.join(file_path, new_name)
