import os
import re

# 用户可配置：旧链接和新链接前缀
old_link_prefix = "https://old.example.com/md-images/raw/master/"
new_link_prefix = "https://new.example.com/md-images/"

# 用户可配置：md文件夹路径
markdown_files_dir = "path-to-markdown-files"

# 动态生成的正则表达式
image_url_pattern = re.compile(rf'!\[.*?\]\({re.escape(old_link_prefix)}(.*?)\)')

# 修改链接计数器
modified_link_count = 0

def update_markdown_links(old_prefix, new_prefix):
    """
    遍历 markdown 文件，更新图片链接并统计修改次数。
    :param old_prefix: 旧链接前缀
    :param new_prefix: 新链接前缀
    """
    global modified_link_count
    updated_links = []

    for root, _, files in os.walk(markdown_files_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 查找并替换图片链接
                updated_content = content
                matches = image_url_pattern.findall(content)
                for match in matches:
                    old_url = f"{old_prefix}{match}"
                    new_url = f"{new_prefix}{match}"
                    updated_content = updated_content.replace(old_url, new_url)
                    updated_links.append((file_path, old_url, new_url))

                # 如果文件内容有变化，写回文件
                if updated_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)

                    # 增加修改的链接数量
                    modified_link_count += len(matches)

    # 打印更新的链接信息
    print("更新的图片链接：")
    for file_path, old_url, new_url in updated_links:
        print(f"文件: {file_path}\n旧链接: {old_url}\n新链接: {new_url}\n")

if __name__ == "__main__":
    # 更新 markdown 文件中的图片链接
    update_markdown_links(old_link_prefix, new_link_prefix)

    # 打印修改链接的总数量
    print(f"总共修改了 {modified_link_count} 个链接。")
