import os
import re
import requests
import hashlib
from urllib.parse import urlparse
import shutil

# --- 配置区 ---
# 你从语雀导出的 Markdown 文件存放的目录
# 假设你把它们都放在了 content/posts/yuque-import 目录下
MARKDOWN_DIR = "content/posts/yuque-import" 
# 语雀图片链接的特征，用于正则匹配
# 修正点: 使用了非捕获分组 (?:...) 来避免产生额外的捕获结果
YUQUE_CDN_PATTERN = r"https?://(?:cdn\.nlark\.com|aliyuncs\.com)/yuque"
# --- 配置区结束 ---

# 正则表达式，用于匹配 Markdown 中的图片链接
# 现在它会正确地只捕获两个部分：1.alt文本, 2.图片URL
IMG_REGEX = re.compile(r"!\[(.*?)\]\((%s.*?)\)" % YUQUE_CDN_PATTERN)

def process_markdown_file(md_file_path):
    """处理单个 Markdown 文件"""
    print(f"--- 开始处理文件: {md_file_path} ---")

    # 1. 将普通 .md 文件转换为 Page Bundle 结构
    dir_path, file_name = os.path.split(md_file_path)
    base_name, ext = os.path.splitext(file_name)
    
    # 如果已经是 index.md 或 _index.md，则直接使用其所在目录
    if file_name.lower() in ["index.md", "_index.md"]:
        bundle_dir = dir_path
        # 如果是这种情况，md_file_path 已经是正确的路径，不需要移动
    else:
        bundle_dir = os.path.join(dir_path, base_name)
        new_md_path = os.path.join(bundle_dir, "index.md")

        if not os.path.exists(bundle_dir):
            os.makedirs(bundle_dir)
            print(f"创建页面捆绑目录: {bundle_dir}")
        
        # 移动并重命名 md 文件
        shutil.move(md_file_path, new_md_path)
        md_file_path = new_md_path
        print(f"已将 {file_name} 移动到 {new_md_path}")

    # 2. 读取新的 md 文件内容
    with open(md_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 3. 查找所有匹配的图片链接
    # 修正后的 findall 将只返回 (alt_text, url) 这样的二元组
    images = IMG_REGEX.findall(content)
    if not images:
        print("未找到需要处理的语雀图片。\n")
        return

    print(f"找到 {len(images)} 张语雀图片，开始下载和替换...")
    
    # 4. 遍历所有找到的图片链接
    for alt_text, url in images:
        try:
            # 清理 URL，移除 # 后面的参数
            clean_url = url.split('#')[0]
            
            # 生成一个简短且唯一的文件名，避免中文或特殊字符问题
            # 使用 URL 的 MD5 哈希值前8位作为文件名
            file_ext = os.path.splitext(urlparse(clean_url).path)[1] or '.png' # 如果没有后缀，默认为.png
            file_hash = hashlib.md5(clean_url.encode()).hexdigest()[:8]
            new_filename = f"{file_hash}{file_ext}"
            
            # 图片要保存的本地路径
            local_image_path = os.path.join(bundle_dir, new_filename)
            
            # 下载图片
            if not os.path.exists(local_image_path):
                print(f"  -> 正在下载: {clean_url}")
                headers = {'User-Agent': 'Mozilla/5.0'} # 模拟浏览器，防止被禁
                response = requests.get(clean_url, headers=headers, stream=True)
                response.raise_for_status() # 如果下载失败则抛出异常
                
                with open(local_image_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"     保存成功: {local_image_path}")
            else:
                print(f"  -> 图片已存在，跳过下载: {new_filename}")

            # 替换 Markdown 内容中的旧 URL 为新本地路径
            # 注意：这里我们只替换文件名，因为图片和md文件在同一目录
            original_markdown_link = f"![{alt_text}]({url})"
            new_markdown_link = f"![{alt_text}]({new_filename})"
            content = content.replace(original_markdown_link, new_markdown_link)

        except requests.exceptions.RequestException as e:
            print(f"     下载失败: {url}, 错误: {e}")
        except Exception as e:
            print(f"     处理失败: {url}, 错误: {e}")

    # 5. 将修改后的内容写回文件
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"文件 {md_file_path} 处理完成。\n")


if __name__ == "__main__":
    if not os.path.isdir(MARKDOWN_DIR):
        print(f"错误: 目录 '{MARKDOWN_DIR}' 不存在。请检查配置。")
    else:
        # 遍历目录下的所有 .md 文件
        for root, _, files in os.walk(MARKDOWN_DIR):
            # 创建一个文件列表的副本进行迭代，因为我们可能会在循环中重命名文件
            for file in list(files):
                if file.endswith(".md"):
                    process_markdown_file(os.path.join(root, file))
        print("所有 Markdown 文件处理完毕！")