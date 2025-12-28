#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 聊天记录集中存储工具

命令:
  python main.py              # 同步一次
  python main.py --watch      # 持续监控
  python main.py --prune      # 清理孤立记录
  python main.py --stats      # 显示统计
  python main.py --search <keyword>  # 搜索
  python main.py --export json|csv [--source codex|kiro|gemini|claude]
"""
import os
import sys
import subprocess

# 项目根目录
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_DIR = os.path.join(PROJECT_DIR, '.venv')
REQUIREMENTS = os.path.join(PROJECT_DIR, 'requirements.txt')

def ensure_venv():
    """检测并创建虚拟环境，安装依赖"""
    # 打包版本跳过
    if getattr(sys, 'frozen', False):
        return
    
    # 已在虚拟环境中运行则跳过
    if sys.prefix != sys.base_prefix:
        return
    
    # 检查 .venv 是否存在
    venv_python = os.path.join(VENV_DIR, 'bin', 'python') if os.name != 'nt' else os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    
    if not os.path.exists(venv_python):
        print("首次运行，创建虚拟环境...")
        subprocess.run([sys.executable, '-m', 'venv', VENV_DIR], check=True)
        print("安装依赖...")
        pip = os.path.join(VENV_DIR, 'bin', 'pip') if os.name != 'nt' else os.path.join(VENV_DIR, 'Scripts', 'pip.exe')
        subprocess.run([pip, 'install', '-r', REQUIREMENTS, '-q'], check=True)
        print("环境准备完成，重新启动...\n")
    
    # 使用虚拟环境重新执行
    os.execv(venv_python, [venv_python] + sys.argv)

# 启动前检测虚拟环境
ensure_venv()

# 支持 PyInstaller 打包
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import argparse
from config import CONFIG
from parsers import CodexParser, GeminiParser, ClaudeParser, KiroParser
from storage import ChatStorage
from logger import setup_logger, get_logger

storage: ChatStorage = None

def main():
    global storage
    
    parser = argparse.ArgumentParser(description='AI Chat Converter')
    parser.add_argument('-w', '--watch', action='store_true', help='持续监控模式')
    parser.add_argument('--prune', action='store_true', help='清理孤立记录')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--search', type=str, help='搜索关键词')
    parser.add_argument('--export', choices=['json', 'csv'], help='导出格式')
    parser.add_argument('--source', choices=['codex', 'kiro', 'gemini', 'claude'], help='指定来源')
    parser.add_argument('--output', type=str, help='导出文件路径')
    args = parser.parse_args()
    
    # 初始化
    setup_logger(CONFIG["log_dir"])
    log = get_logger()
    
    storage = ChatStorage(CONFIG["db_path"])
    
    # 命令分发
    if args.prune:
        cmd_prune()
    elif args.stats:
        cmd_stats()
    elif args.search:
        cmd_search(args.search, args.source)
    elif args.export:
        cmd_export(args.export, args.source, args.output)
    elif args.watch:
        cmd_sync()
        cmd_watch()
    else:
        cmd_sync()

def cmd_sync():
    log = get_logger()
    log.info("=" * 50)
    log.info("AI 聊天记录 → 集中存储")
    log.info("=" * 50)
    log.info(f"数据库: {CONFIG['db_path']}")
    
    total_added, total_updated, total_skipped, total_errors = 0, 0, 0, 0
    
    for cli, key, parser_cls in [
        ('codex', 'codex_paths', lambda: CodexParser('codex')),
        ('kiro', 'kiro_paths', KiroParser),
        ('gemini', 'gemini_paths', GeminiParser),
        ('claude', 'claude_paths', ClaudeParser),
    ]:
        paths = CONFIG.get(key, [])
        if not paths:
            continue
        
        parser = parser_cls()
        if cli in ('claude', 'kiro'):
            a, u, s, e = process_multi(parser, paths, cli)
        else:
            a, u, s, e = process(parser, paths)
        
        log.info(f"[{cli.capitalize()}] 新增:{a} 更新:{u} 跳过:{s} 错误:{e}")
        update_cli_meta(cli)
        total_added += a
        total_updated += u
        total_skipped += s
        total_errors += e
    
    total = storage.get_total_stats()
    storage.update_total_meta(total['sessions'], total['messages'], total['tokens'])
    
    log.info("=" * 50)
    log.info(f"总计: {total['sessions']} 会话, {total['messages']} 消息")
    if total_errors > 0:
        log.warning(f"错误: {total_errors} 个文件解析失败")
    log.info("✓ 同步完成!")
    
    print_token_stats()

def cmd_watch():
    from watcher import ChatWatcher
    from datetime import datetime
    
    log = get_logger()
    log.info("")
    log.info("=" * 50)
    log.info("实时监听模式 (watchdog)")
    log.info("=" * 50)
    
    watch_paths = []
    path_source_map = {}
    
    for cli, key in [('codex', 'codex_paths'), ('kiro', 'kiro_paths'), 
                     ('gemini', 'gemini_paths'), ('claude', 'claude_paths')]:
        for p in CONFIG.get(key, []):
            if os.path.isdir(p) or os.path.isfile(p):
                watch_paths.append(p)
                path_source_map[p] = cli
    
    def on_change(file_path, event_type):
        now = datetime.now().strftime('%H:%M:%S')
        source = None
        for p, s in path_source_map.items():
            if file_path.startswith(p) or file_path == p:
                source = s
                break
        if not source:
            return
        
        try:
            if source == 'kiro':
                parser = KiroParser()
                for sess in parser.parse_file(file_path):
                    storage.upsert_session(sess.session_id, sess.source, sess.file_path, sess.cwd, sess.messages, int(sess.file_mtime), sess.start_time)
                log.info(f"[{now}] kiro 更新")
            elif source == 'claude':
                parser = ClaudeParser()
                for sess in parser.parse_file(file_path):
                    fp = f"claude:{sess.session_id}"
                    storage.upsert_session(sess.session_id, sess.source, fp, sess.cwd, sess.messages, int(sess.file_mtime), sess.start_time)
                log.info(f"[{now}] claude 更新")
            else:
                parser = CodexParser(source) if source == 'codex' else GeminiParser()
                sess = parser.parse_file(file_path)
                fp = os.path.abspath(sess.file_path)
                storage.upsert_session(sess.session_id, sess.source, fp, sess.cwd, sess.messages, int(sess.file_mtime), sess.start_time)
                log.info(f"[{now}] {source} {event_type}: {os.path.basename(file_path)}")
            
            update_cli_meta(source)
            total = storage.get_total_stats()
            storage.update_total_meta(total['sessions'], total['messages'], total['tokens'])
        except Exception as e:
            log.error(f"[{now}] 处理失败 {file_path}: {e}")
    
    log.info(f"监听目录: {len(watch_paths)} 个")
    watcher = ChatWatcher(watch_paths, on_change)
    watcher.start()

def cmd_prune():
    log = get_logger()
    log.info("清理孤立记录...")
    removed = storage.prune()
    total = sum(removed.values())
    if total > 0:
        for cli, count in removed.items():
            if count > 0:
                log.info(f"  {cli}: 删除 {count} 条")
        log.info(f"✓ 共清理 {total} 条孤立记录")
    else:
        log.info("✓ 无孤立记录")

def cmd_stats():
    log = get_logger()
    meta = storage.get_total_meta()
    tokens = storage.get_token_stats()
    
    log.info("=" * 50)
    log.info("统计信息")
    log.info("=" * 50)
    log.info(f"数据库: {CONFIG['db_path']}")
    log.info(f"总会话: {meta['total_sessions']}")
    log.info(f"总消息: {meta['total_messages']}")
    log.info(f"最后同步: {meta['last_sync']}")
    log.info("")
    log.info("Token 统计 (tiktoken):")
    total_tokens = 0
    for source in ['codex', 'kiro', 'gemini', 'claude']:
        t = tokens.get(source, 0)
        if t > 0:
            log.info(f"  {source}: {t:,}")
            total_tokens += t
    log.info(f"  总计: {total_tokens:,}")

def cmd_search(keyword: str, source: str = None):
    log = get_logger()
    results = storage.search(keyword, source)
    log.info(f"搜索 '{keyword}' 找到 {len(results)} 个会话:")
    for r in results[:20]:
        log.info(f"  [{r['source']}] {r['session_id']} - {r['cwd'] or 'N/A'}")

def cmd_export(fmt: str, source: str = None, output: str = None):
    log = get_logger()
    if not output:
        output = os.path.join(CONFIG["output_dir"], f"export.{fmt}")
    
    if fmt == 'json':
        count = storage.export_json(output, source)
    else:
        count = storage.export_csv(output, source)
    
    log.info(f"✓ 导出 {count} 条到 {output}")

def print_token_stats():
    log = get_logger()
    tokens = storage.get_token_stats()
    log.info("")
    log.info("=== Token 统计 (tiktoken) ===")
    total = 0
    for source in ['codex', 'kiro', 'gemini', 'claude']:
        t = tokens.get(source, 0)
        if t > 0:
            log.info(f"  {source}: {t:,} tokens")
            total += t
    log.info(f"  总计: {total:,} tokens")

def update_cli_meta(cli: str):
    stats = storage.get_cli_stats(cli)
    path = CONFIG.get(f"{cli}_paths", [""])[0] if CONFIG.get(f"{cli}_paths") else ""
    storage.update_cli_meta(cli, path, stats['sessions'], stats['messages'], stats['tokens'])

def process(parser, paths) -> tuple:
    log = get_logger()
    added, updated, skipped, errors = 0, 0, 0, 0
    for f in parser.find_files(paths):
        try:
            s = parser.parse_file(f)
            file_path = os.path.abspath(s.file_path)
            db_mtime = storage.get_file_mtime(file_path)
            file_mtime = int(s.file_mtime)
            if db_mtime == 0:
                storage.upsert_session(s.session_id, s.source, file_path, s.cwd, s.messages, file_mtime, s.start_time)
                added += 1
            elif file_mtime > db_mtime:
                storage.upsert_session(s.session_id, s.source, file_path, s.cwd, s.messages, file_mtime, s.start_time)
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            log.debug(f"解析失败 {f}: {e}")
            errors += 1
    return added, updated, skipped, errors

def process_multi(parser, paths, source: str) -> tuple:
    """处理返回多个会话的解析器（Claude/Kiro）"""
    log = get_logger()
    added, updated, skipped, errors = 0, 0, 0, 0
    for f in parser.find_files(paths):
        try:
            for s in parser.parse_file(f):
                file_path = s.file_path  # kiro:xxx 或 claude:xxx
                db_mtime = storage.get_file_mtime(file_path)
                file_mtime = int(s.file_mtime)
                if db_mtime == 0:
                    storage.upsert_session(s.session_id, s.source, file_path, s.cwd, s.messages, file_mtime, s.start_time)
                    added += 1
                elif file_mtime > db_mtime:
                    storage.upsert_session(s.session_id, s.source, file_path, s.cwd, s.messages, file_mtime, s.start_time)
                    updated += 1
                else:
                    skipped += 1
        except Exception as e:
            log.debug(f"解析失败 {f}: {e}")
            errors += 1
    return added, updated, skipped, errors

if __name__ == '__main__':
    main()
