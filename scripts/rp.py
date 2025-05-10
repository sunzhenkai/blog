import os
import re
from pathlib import Path


def convert_date_format(content):
    # 正则匹配日期行，允许斜杠前后有空格，不区分大小写
    pattern = re.compile(
        r"^\s*(date|update):\s*(\d{4})\s*/\s*(\d{1,2})\s*/\s*(\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s*$",
        flags=re.MULTILINE | re.IGNORECASE,
    )

    def replacer(match):
        key = match.group(1)  # 保留原始大小写
        year = match.group(2)
        month = int(match.group(3))
        day = int(match.group(4))
        time = match.group(5)

        # 格式化为ISO 8601并添加时区
        new_date = f"{year}-{month:02d}-{day:02d}T{time}+08:00"
        return f'{key}: "{new_date}"'

    return pattern.sub(replacer, content)


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".md"):
                file_path = Path(root) / file
                with open(file_path, "r", encoding="utf-8") as f:
                    original = f.read()

                converted = convert_date_format(original)

                if converted != original:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(converted)
                    print(f"已更新: {file_path}")
                else:
                    print(f"无需修改: {file_path}")


if __name__ == "__main__":
    target_dir = input("请输入要处理的目录路径：").strip()
    if Path(target_dir).is_dir():
        process_directory(target_dir)
        print("处理完成！")
    else:
        print("错误：输入的路径不是有效目录")
