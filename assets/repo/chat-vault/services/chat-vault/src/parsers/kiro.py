#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiro CLI 解析器 - 从 SQLite 数据库读取"""
import os
import json
import sqlite3
import hashlib
from datetime import datetime
from .base import BaseParser, SessionData

KIRO_DB = os.path.expanduser("~/.local/share/kiro-cli/data.sqlite3")

class KiroParser(BaseParser):
    def find_files(self, paths: list) -> list:
        """返回数据库路径（如果存在）"""
        if os.path.exists(KIRO_DB):
            return [KIRO_DB]
        return []
    
    def parse_file(self, filepath: str) -> list:
        """解析 Kiro SQLite 数据库，返回多个 SessionData"""
        sessions = []
        file_mtime = os.path.getmtime(filepath)
        
        conn = sqlite3.connect(filepath)
        for row in conn.execute('SELECT key, value FROM conversations'):
            cwd, value = row
            try:
                data = json.loads(value)
            except json.JSONDecodeError:
                continue
            
            conv_id = data.get('conversation_id', hashlib.md5(cwd.encode()).hexdigest()[:12])
            history = data.get('history', [])
            
            messages = []
            first_timestamp = None
            
            for item in history:
                # 用户消息
                if 'user' in item:
                    user = item['user']
                    ts = user.get('timestamp', '')
                    if ts and not first_timestamp:
                        first_timestamp = ts
                    content = user.get('content', {})
                    if isinstance(content, dict) and 'Prompt' in content:
                        prompt = content['Prompt'].get('prompt', '')
                        if prompt:
                            messages.append({
                                'time': ts or '',
                                'role': 'user',
                                'content': prompt
                            })
                
                # AI 回复
                if 'assistant' in item:
                    assistant = item['assistant']
                    ts = assistant.get('timestamp', '')
                    content = assistant.get('content', {})
                    if isinstance(content, dict) and 'Message' in content:
                        msg = content['Message'].get('message', '')
                        if msg:
                            messages.append({
                                'time': ts or '',
                                'role': 'ai',
                                'content': msg
                            })
            
            if messages:
                # 优先用第一条消息的 timestamp，否则用 file_mtime
                if first_timestamp:
                    # 转换为 UTC ISO8601 格式 (去掉时区偏移)
                    start_time = first_timestamp.replace('+08:00', 'Z').replace('+00:00', 'Z')
                    if not start_time.endswith('Z'):
                        start_time = start_time[:19] + 'Z'
                else:
                    from datetime import timezone
                    start_time = datetime.fromtimestamp(file_mtime, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                
                sessions.append(SessionData(
                    session_id=f'kiro-{conv_id[:12]}',
                    source='kiro',
                    file_path=f'kiro:{conv_id}',
                    file_mtime=file_mtime,
                    cwd=cwd,
                    start_time=start_time,
                    messages=messages
                ))
        
        conn.close()
        return sessions
