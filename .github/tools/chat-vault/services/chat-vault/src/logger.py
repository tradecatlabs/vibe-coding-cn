#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日志模块 - 同时输出到控制台和文件"""
import logging
import os
from datetime import datetime

_logger = None

def setup_logger(log_dir: str = None) -> logging.Logger:
    global _logger
    if _logger:
        return _logger
    
    _logger = logging.getLogger('ai_chat_converter')
    _logger.setLevel(logging.DEBUG)
    _logger.handlers.clear()
    
    fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    # 控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    _logger.addHandler(ch)
    
    # 文件
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"sync_{datetime.now().strftime('%Y%m%d')}.log")
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        _logger.addHandler(fh)
    
    return _logger

def get_logger() -> logging.Logger:
    global _logger
    if not _logger:
        _logger = setup_logger()
    return _logger
