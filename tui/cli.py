#!/usr/bin/env python3
"""AI Native Pipeline TUI CLI 入口"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tui.app import main

if __name__ == "__main__":
    main()