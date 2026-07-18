import subprocess
import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_server()

    def start_server(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        
        print("\n--- Starting Uvicorn Server ---")
        # Run uvicorn without its internal --reload flag to avoid Windows crashes
        self.process = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app", "--port", "8000"])

    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py') or event.src_path.endswith('.env'):
            print(f"\n[Watcher] Detected change in {event.src_path}. Restarting...")
            self.start_server()

if __name__ == "__main__":
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    print("[Watcher] Started watching for file changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    observer.join()
