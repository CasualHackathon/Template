#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese translation script
Translate the README.md file to a Chinese version README_ZH-CN.md
"""

import os
import shutil
import re
from datetime import datetime

# Character mapping table - English to Chinese translation
TRANSLATION_MAP = {
    # Main titles and sections
    "⏰ Event Timeline": "⏰ 活动时间线",
    "📝 Participants": "📝 参与者",
    "🌟 Guests": "🌟 嘉宾",
    "🤝 Co-organizers": "🤝 联合主办方",
    "🌐 Community Support": "🌐 社区支持",
    
    # Table titles
    "Event": "活动",
    "Time": "时间",
    "Format": "形式",
    "Recap": "回顾",
    "Project:": "项目：",
    "🧩 Participation": "🧩 参与方式",
    "💪 Team Members": "💪 团队成员",
    "🏁 Progress": "🏁 进度",
    "🌱 Status": "🌱 状态",
    "🏅 NFT Badge": "🏅 NFT徽章",
    
    # Status related
    "Active": "进行中",
    "Submitted": "已提交",
    "Team": "团队",
    "Solo": "个人",
    
    # Time related
    "Open Day": "开放日",
    "Demo Day": "演示日",
    "Online": "线上",
    "Relaxed participation": "放松参与",
    "Open to everyone": "对所有人开放",
    
    # Others
    "Last updated:": "最后更新：",
}

def translate_content(content):
    """Translate English text in content to Chinese"""
    translated_content = content
    
    # Apply translation mapping
    for english, chinese in TRANSLATION_MAP.items():
        translated_content = translated_content.replace(english, chinese)
    
    return translated_content

def create_chinese_readme():
    """Create a Chinese version of the README file"""
    # Source file path
    source_file = "README.md"
    target_file = "README_ZH-CN.md"
    
    # Check if source file exists
    if not os.path.exists(source_file):
        print(f"Error: Source file {source_file} does not exist")
        return False
    
    try:
        # Read source file content
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Translate content
        translated_content = translate_content(content)
        
        # Write to target file
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"✅ Successfully created Chinese version: {target_file}")
        print(f"📝 Translated {len(TRANSLATION_MAP)} terms")   
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating Chinese version: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting Chinese translation...")
    
    # Get current working directory
    current_dir = os.getcwd()
    print(f"📁 Current working directory: {current_dir}")
    
    # Create Chinese version
    success = create_chinese_readme()
    
    if success:
        print("🎉 Chinese translation completed!")
    else:
        print("💥 Chinese translation failed!")
        exit(1)

if __name__ == "__main__":
    main() 