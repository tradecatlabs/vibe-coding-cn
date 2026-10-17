#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨平台文件监控 (Linux/macOS/Windows)"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class ChatFileHandler(FileSystemEventHandler):
    def __init__(self, callback, extensions):
        self.callback = callback
        self.extensions = extensions
    
    def _check(self, event):
        if event.is_directory:
            return
        path = event.src_path
        if any(path.endswith(ext) for ext in self.extensions):
            self.callback(path, event.event_type)
    
    def on_created(self, event):
        self._check(event)
    
    def on_modified(self, event):
        self._check(event)

class ChatWatcher:
    def __init__(self, paths: list, callback, extensions=('.jsonl', '.json')):
        self.observer = Observer()
        handler = ChatFileHandler(callback, extensions)
        for path in paths:
            self.observer.schedule(handler, path, recursive=True)
    
    def start(self):
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        self.observer.stop()
        self.observer.join()
