#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SQLite 存储模块 - 完整版"""
import sqlite3
import json
import os
import datetime
import tiktoken

SCHEMA_VERSION = 5
CLIS = ('codex', 'kiro', 'gemini', 'claude')

_encoder = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(_encoder.encode(text)) if text else 0

class ChatStorage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)
        self._init_db()
    
    def _conn(self):
        return sqlite3.connect(self.db_path)
    
    def _init_db(self):
        with self._conn() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)''')
            for cli in CLIS:
                conn.execute(f'''CREATE TABLE IF NOT EXISTS meta_{cli} (key TEXT PRIMARY KEY, value TEXT)''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    file_path TEXT PRIMARY KEY,
                    session_id TEXT,
                    source TEXT NOT NULL,
                    cwd TEXT,
                    messages TEXT,
                    file_mtime INTEGER,
                    start_time TEXT,
                    token_count INTEGER DEFAULT 0
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_source ON sessions(source)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON sessions(session_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_start_time ON sessions(start_time)')
            self._set_meta('meta', 'schema_version', str(SCHEMA_VERSION))
    
    def _set_meta(self, table: str, key: str, value: str):
        with self._conn() as conn:
            conn.execute(f'INSERT OR REPLACE INTO {table} (key, value) VALUES (?, ?)', (key, value))
    
    def _get_meta(self, table: str, key: str) -> str:
        with self._conn() as conn:
            row = conn.execute(f'SELECT value FROM {table} WHERE key = ?', (key,)).fetchone()
            return row[0] if row else None
    
    def update_cli_meta(self, cli: str, path: str, sessions: int, messages: int, tokens: int = None):
        table = f'meta_{cli}'
        now = datetime.datetime.now().isoformat()
        # 顺序: path, sessions, messages, total_tokens, last_sync
        self._set_meta(table, 'path', path)
        self._set_meta(table, 'sessions', str(sessions))
        self._set_meta(table, 'messages', str(messages))
        self._set_meta(table, 'total_tokens', str(tokens or 0))
        self._set_meta(table, 'last_sync', now)
    
    def update_total_meta(self, sessions: int, messages: int, tokens: int = None):
        now = datetime.datetime.now().isoformat()
        self._set_meta('meta', 'total_sessions', str(sessions))
        self._set_meta('meta', 'total_messages', str(messages))
        if tokens is not None:
            self._set_meta('meta', 'total_tokens', str(tokens))
        self._set_meta('meta', 'last_sync', now)
    
    def get_total_meta(self) -> dict:
        return {
            'schema_version': int(self._get_meta('meta', 'schema_version') or 0),
            'total_sessions': int(self._get_meta('meta', 'total_sessions') or 0),
            'total_messages': int(self._get_meta('meta', 'total_messages') or 0),
            'last_sync': self._get_meta('meta', 'last_sync'),
        }
    
    def get_file_mtime(self, file_path: str) -> int:
        with self._conn() as conn:
            row = conn.execute('SELECT file_mtime FROM sessions WHERE file_path = ?', (file_path,)).fetchone()
            return row[0] if row else 0
    
    def upsert_session(self, session_id: str, source: str, file_path: str,
                       cwd: str, messages: list, file_mtime: int, start_time: str = None):
        # kiro: 和 claude: 开头的是虚拟路径，不转换
        if file_path and not file_path.startswith(('claude:', 'kiro:')) and not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        
        total_tokens = sum(count_tokens(msg.get('content', '')) for msg in messages)
        if not start_time and messages:
            start_time = messages[0].get('time')
        
        messages_json = json.dumps(messages, ensure_ascii=False)
        with self._conn() as conn:
            conn.execute('''
                INSERT INTO sessions (file_path, session_id, source, cwd, messages, file_mtime, start_time, token_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(file_path) DO UPDATE SET
                    session_id=excluded.session_id, messages=excluded.messages,
                    file_mtime=excluded.file_mtime, start_time=excluded.start_time, token_count=excluded.token_count
            ''', (file_path, session_id, source, cwd, messages_json, file_mtime, start_time, total_tokens))
    
    def get_cli_stats(self, cli: str) -> dict:
        with self._conn() as conn:
            sessions = conn.execute('SELECT COUNT(*) FROM sessions WHERE source = ?', (cli,)).fetchone()[0]
            row = conn.execute('SELECT SUM(json_array_length(messages)) FROM sessions WHERE source = ?', (cli,)).fetchone()
            messages = row[0] or 0
            tokens = conn.execute('SELECT SUM(token_count) FROM sessions WHERE source = ?', (cli,)).fetchone()[0] or 0
        return {'sessions': sessions, 'messages': messages, 'tokens': tokens}
    
    def get_total_stats(self) -> dict:
        with self._conn() as conn:
            sessions = conn.execute('SELECT COUNT(*) FROM sessions').fetchone()[0]
            row = conn.execute('SELECT SUM(json_array_length(messages)) FROM sessions').fetchone()
            messages = row[0] or 0
            tokens = conn.execute('SELECT SUM(token_count) FROM sessions').fetchone()[0] or 0
        return {'sessions': sessions, 'messages': messages, 'tokens': tokens}
    
    def get_token_stats(self) -> dict:
        with self._conn() as conn:
            rows = conn.execute('SELECT source, SUM(token_count) FROM sessions GROUP BY source').fetchall()
        return {r[0]: r[1] or 0 for r in rows}
    
    # === 清理孤立记录 ===
    def prune(self) -> dict:
        """删除源文件已不存在的记录"""
        removed = {'codex': 0, 'kiro': 0, 'gemini': 0, 'claude': 0}
        with self._conn() as conn:
            rows = conn.execute('SELECT file_path, source FROM sessions').fetchall()
            for fp, source in rows:
                if fp.startswith('claude:'):
                    continue  # Claude 使用虚拟路径
                if not os.path.exists(fp):
                    conn.execute('DELETE FROM sessions WHERE file_path = ?', (fp,))
                    removed[source] = removed.get(source, 0) + 1
        return removed
    
    # === 查询 ===
    def search(self, keyword: str, source: str = None, limit: int = 50) -> list:
        """搜索消息内容"""
        sql = "SELECT file_path, session_id, source, cwd, messages, start_time FROM sessions WHERE messages LIKE ?"
        params = [f'%{keyword}%']
        if source:
            sql += " AND source = ?"
            params.append(source)
        sql += f" ORDER BY start_time DESC LIMIT {limit}"
        
        results = []
        with self._conn() as conn:
            for row in conn.execute(sql, params):
                results.append({
                    'file_path': row[0], 'session_id': row[1], 'source': row[2],
                    'cwd': row[3], 'messages': json.loads(row[4]), 'start_time': row[5]
                })
        return results
    
    def get_session(self, file_path: str) -> dict:
        """获取单个会话"""
        with self._conn() as conn:
            row = conn.execute(
                'SELECT file_path, session_id, source, cwd, messages, start_time, token_count FROM sessions WHERE file_path = ?',
                (file_path,)
            ).fetchone()
        if not row:
            return None
        return {
            'file_path': row[0], 'session_id': row[1], 'source': row[2], 'cwd': row[3],
            'messages': json.loads(row[4]), 'start_time': row[5], 'token_count': row[6]
        }
    
    def list_sessions(self, source: str = None, limit: int = 100, offset: int = 0) -> list:
        """列出会话"""
        sql = "SELECT file_path, session_id, source, cwd, start_time, token_count FROM sessions"
        params = []
        if source:
            sql += " WHERE source = ?"
            params.append(source)
        sql += f" ORDER BY start_time DESC LIMIT {limit} OFFSET {offset}"
        
        results = []
        with self._conn() as conn:
            for row in conn.execute(sql, params):
                results.append({
                    'file_path': row[0], 'session_id': row[1], 'source': row[2],
                    'cwd': row[3], 'start_time': row[4], 'token_count': row[5]
                })
        return results
    
    # === 导出 ===
    def export_json(self, output_path: str, source: str = None):
        """导出为 JSON"""
        sql = "SELECT file_path, session_id, source, cwd, messages, start_time, token_count FROM sessions"
        params = []
        if source:
            sql += " WHERE source = ?"
            params.append(source)
        sql += " ORDER BY start_time"
        
        data = []
        with self._conn() as conn:
            for row in conn.execute(sql, params):
                data.append({
                    'file_path': row[0], 'session_id': row[1], 'source': row[2], 'cwd': row[3],
                    'messages': json.loads(row[4]), 'start_time': row[5], 'token_count': row[6]
                })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return len(data)
    
    def export_csv(self, output_path: str, source: str = None):
        """导出为 CSV（扁平化消息）"""
        import csv
        sql = "SELECT session_id, source, cwd, messages, start_time FROM sessions"
        params = []
        if source:
            sql += " WHERE source = ?"
            params.append(source)
        sql += " ORDER BY start_time"
        
        count = 0
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['session_id', 'source', 'cwd', 'time', 'role', 'content'])
            with self._conn() as conn:
                for row in conn.execute(sql, params):
                    session_id, src, cwd, msgs_json, _ = row
                    for msg in json.loads(msgs_json):
                        writer.writerow([session_id, src, cwd, msg.get('time', ''), msg.get('role', ''), msg.get('content', '')])
                        count += 1
        return count
    
    # === 获取所有文件路径（用于 prune 检查） ===
    def get_all_file_paths(self, source: str = None) -> set:
        sql = "SELECT file_path FROM sessions"
        params = []
        if source:
            sql += " WHERE source = ?"
            params.append(source)
        with self._conn() as conn:
            return {row[0] for row in conn.execute(sql, params)}
