#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language switch script
Switch the language of the README.md file based on the configuration
"""

import os
import shutil

# Global configuration
DEFAULT_LANGUAGE = "en"  # Optional: "en", "zh" - The language of the README.md file

def switch_language_files():
    """Switch the language of the README.md file based on the configuration"""
    readme_path = "README.md"
    readme_zh_path = "docs/README_ZH-CN.md"
    readme_en_path = "docs/README_EN-US.md"
    
    if DEFAULT_LANGUAGE == 'en':
        if not os.path.exists(readme_en_path):
            print(f"❌ English file does not exist: {readme_en_path}")
            return False
        
        # Copy English file to README.md
        shutil.copy2(readme_en_path, readme_path)
        print("✅ Set English as default")
        return True
    
    elif DEFAULT_LANGUAGE == 'zh':
        if not os.path.exists(readme_zh_path):
            print(f"❌ Chinese file does not exist: {readme_zh_path}")
            return False
        
        # Copy Chinese file to README.md
        shutil.copy2(readme_zh_path, readme_path)
        print("✅ Set Chinese as default")
        return True
    
    else:
        print(f"❌ Unsupported language: {DEFAULT_LANGUAGE}")
        return False

def main():
    """Main function"""
    success = switch_language_files()
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 