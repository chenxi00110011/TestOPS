# file_reader.py
def read_file_lines(file_path):
    """读取文本文件并返回按行分割的列表"""
    try:
        # 打开文件
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取所有行，并去除每行末尾的换行符
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return []
    except IOError as e:
        print(f"IOError: {e}")
        return []


# 使用示例
if __name__ == "__main__":
    file_path = './dids.txt'  # 替换成你的文件路径
    lines = read_file_lines(file_path)
    print(lines)
