import time
import json
from datetime import datetime
from pynput import keyboard, mouse
import pygetwindow as gw
from PIL import ImageGrab
import os

class ActivityMonitor:
    def __init__(self):
        self.batch = []
        self.batch_size = 5  # Small batch for testing
        self.last_activity = time.time()
        
    def on_keystroke(self, key):
        self.record_activity({
            'type': 'keystroke',
            'timestamp': datetime.now().isoformat(),
            'metadata': str(key)[:1]  # First character only
        })

    def on_mouse_move(self, x, y):
        self.record_activity({
            'type': 'mouse_move',
            'timestamp': datetime.now().isoformat(),
            'position': (x, y)
        })

    def capture_screenshot(self):
        try:
            img = ImageGrab.grab()
            fn = os.path.join("screenshots", f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
            img.save(fn)
            return fn
        except Exception as e:
            print(f"Capture error: {e}")

    def get_active_window(self):
        try:
            return gw.getActiveWindow().title
        except Exception as e:
            print(f"Window capture error: {e}")
            return "Unknown Window"

    def record_activity(self, data):
        data['window'] = self.get_active_window()
        self.batch.append(data)
        
        if len(self.batch) >= self.batch_size:
            self.send_batch()

    def send_batch(self):
        try:
            screenshots = [self.capture_screenshot()]
            payload = {
                'activities': self.batch,
                'screenshots': screenshots,
                'machine_id': 'LOCAL_DEV_MACHINE'
            }
            # Store locally instead of HTTP send
            fn = os.path.join("data", f"{datetime.now().timestamp()}.json")
            with open(fn, 'w') as f:
                json.dump(payload, f)
            self.batch = []
        except Exception as e:
            print(f"Upload error: {e}")

if __name__ == "__main__":
    monitor = ActivityMonitor()
    with keyboard.Listener(on_press=monitor.on_keystroke) as klistener:
        with mouse.Listener(on_move=monitor.on_mouse_move) as mlistener:
            klistener.join()
            mlistener.join()