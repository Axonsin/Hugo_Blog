import os
import re
import random
from datetime import datetime, timedelta

def generate_random_date():
    """生成 2024-12-01 到 2025-07-02 之间的随机日期"""
    start_date = datetime(2024, 12, 1)
    end_date = datetime(2025, 7, 2)
    
    # 计算日期范围内的天数
    days_between = (end_date - start_date).days
    
    # 生成随机天数偏移
    random_days = random.randint(0, days_between)
    
    # 计算随机日期
    random_date = start_date + timedelta(days=random_days)
    
    return random_date.strftime('%Y-%m-%d')

def extract_title_from_filename(filename):
    """从文件名提取标题"""
    # 移除 .md 扩展名和可能的数字后缀
    title = filename.replace('.md', '')
    title = re.sub(r'\s*\(\d+\)$', '', title)  # 移除 (1) 这样的后缀
    return title

def generate_tags_and_description(filename, content):
    """根据文件名和内容生成标签和描述"""
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    tags = []
    description = ""
    summary = ""
    
    # 根据文件名和内容关键词生成标签
    if 'unity' in filename_lower or 'unity' in content_lower:
        tags.append('Unity')
    if 'blender' in filename_lower or 'blender' in content_lower:
        tags.append('Blender')
    if 'shader' in filename_lower or 'shader' in content_lower or '着色器' in content_lower:
        tags.append('Shader')
    if 'animation' in filename_lower or 'retargeting' in filename_lower or '动画' in content_lower:
        tags.append('Animation')
    if 'houdini' in filename_lower or 'houdini' in content_lower:
        tags.append('Houdini')
    if 'vex' in filename_lower or 'vex' in content_lower:
        tags.append('VEX')
    if 'git' in filename_lower or 'git' in content_lower:
        tags.append('Git')
    if 'obs' in filename_lower or 'obs' in content_lower:
        tags.append('OBS')
    if '渲染' in filename_lower or '渲染' in content_lower or 'render' in content_lower:
        tags.append('渲染')
    if '材质' in filename_lower or '材质' in content_lower or 'material' in content_lower:
        tags.append('材质')
    if '光照' in filename_lower or '光照' in content_lower or 'lighting' in content_lower or '体积光' in content_lower:
        tags.append('光照')
    if '算法' in filename_lower or '算法' in content_lower or 'algorithm' in content_lower:
        tags.append('算法')
    if '物理' in filename_lower or '物理' in content_lower or 'physics' in content_lower:
        tags.append('物理')
    if '颜色' in filename_lower or '色彩' in content_lower or 'color' in content_lower:
        tags.append('色彩')
    if '问题' in filename_lower or '故障' in content_lower or 'bug' in content_lower or '修复' in content_lower:
        tags.append('故障排除')
    if '教程' in filename_lower or '教程' in content_lower or 'tutorial' in content_lower:
        tags.append('教程')
    if '技巧' in filename_lower or '技巧' in content_lower or 'tips' in content_lower:
        tags.append('技巧')
    if '配置' in filename_lower or '配置' in content_lower or 'config' in content_lower:
        tags.append('配置')
    if 'mmd' in filename_lower or 'mmd' in content_lower or 'miku' in content_lower:
        tags.append('MMD')
    if 'retargeting' in filename_lower or 'retargeting' in content_lower:
        tags.append('Retargeting')
    if 'ddns' in filename_lower or 'cloudflare' in content_lower:
        tags.append('网络配置')
    if '插件' in filename_lower or '插件' in content_lower or 'plugin' in content_lower:
        tags.append('插件')
    
    # 如果没有找到特定标签，添加一些通用标签
    if not tags:
        tags = ['技术']
    
    # 生成描述和摘要
    title = extract_title_from_filename(filename)
    
    # 根据标题生成描述
    if 'Unity' in tags and 'Retargeting' in tags:
        description = "Unity骨骼动画Retargeting的配置方法和注意事项"
        summary = "骨骼动画指北"
    elif 'Unity' in tags and '体积光' in title:
        description = "Unity中实现体积光效果的三种不同方案对比"
        summary = "体积光实现方案"
    elif 'Blender' in tags and 'Unity' in tags:
        description = "Blender模型导入Unity的完整工作流程"
        summary = "Blender导入Unity指南"
    elif 'Shader' in tags and 'OBS' in tags:
        description = "在OBS中使用ShaderFilter插件创建自定义视觉效果"
        summary = "OBS自定义Shader效果"
    elif 'VEX' in tags:
        description = "Houdini VEX编程中的变量使用技巧"
        summary = "VEX编程技巧"
    elif 'Git' in tags:
        description = "Git项目中.gitignore文件的配置方法"
        summary = "Git配置指南"
    elif '算法' in tags:
        description = f"{title}的原理解析和实现方法"
        summary = "算法原理解析"
    elif '故障排除' in tags:
        description = f"{title}的解决方案和处理方法"
        summary = "问题解决方案"
    elif '渲染' in tags:
        description = f"{title}的技术原理和应用"
        summary = "渲染技术解析"
    else:
        description = f"{title}的详细介绍和使用方法"
        summary = "技术分享"
    
    return tags, description, summary

def add_frontmatter_to_file(filepath):
    """为单个文件添加Front Matter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有Front Matter
    if content.startswith('---'):
        print(f"文件 {os.path.basename(filepath)} 已有Front Matter，跳过")
        return
    
    filename = os.path.basename(filepath)
    title = extract_title_from_filename(filename)
    date = generate_random_date()
    tags, description, summary = generate_tags_and_description(filename, content)
    
    # 生成Front Matter
    frontmatter = f"""---
title: {title}
date: {date}
tags: {tags}
description: "{description}"
summary: {summary}
categories: [杂谈]
---

"""
    
    # 添加Front Matter到文件开头
    new_content = frontmatter + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已为 {filename} 添加Front Matter")

def main():
    """主函数"""
    yuque_import_dir = r'd:\HugoPages\axonsin\content\posts\yuque-import'
    
    if not os.path.exists(yuque_import_dir):
        print(f"目录不存在: {yuque_import_dir}")
        return
    
    # 获取所有markdown文件
    md_files = [f for f in os.listdir(yuque_import_dir) if f.endswith('.md')]
    
    print(f"找到 {len(md_files)} 个markdown文件")
    
    for md_file in md_files:
        filepath = os.path.join(yuque_import_dir, md_file)
        add_frontmatter_to_file(filepath)
    
    print("所有文件处理完成！")

if __name__ == "__main__":
    main()
