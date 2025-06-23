"""
Real-time file monitoring module for the File Organizer
"""

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PySide6.QtCore import QObject, Signal

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            self.callback(f"➕ New file: {os.path.basename(event.src_path)}")

    def on_deleted(self, event):
        if not event.is_directory:
            self.callback(f"🗑️ Deleted: {os.path.basename(event.src_path)}")

    def on_moved(self, event):
        if not event.is_directory:
            self.callback(f"📦 Moved: {os.path.basename(event.src_path)} → {os.path.basename(event.dest_path)}")

class DirectoryWatcher(QObject):
    file_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.observer = None
        self.watching_path = None
        
    def start_watching(self, path):
        """Start monitoring a directory for changes"""
        if self.observer:
            self.stop_watching()
            
        self.watching_path = path
        handler = FileChangeHandler(self.file_changed.emit)
        self.observer = Observer()
        self.observer.schedule(handler, path, recursive=True)
        self.observer.start()
        
    def stop_watching(self):
        """Stop monitoring the current directory"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.watching_path = None
            
    def is_watching(self):
        """Check if currently monitoring a directory"""
        return self.observer is not None and self.observer.is_alive() 