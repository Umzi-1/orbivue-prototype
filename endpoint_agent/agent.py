import time
import json
from datetime import datetime
from pynput import keyboard, mouse
import pygetwindow as gw
from PIL import ImageGrab
import os
import threading
from collections import deque
import psutil
import logging

# Configure logging
logging.basicConfig(filename='agent.log', level=logging.INFO)

class ActivityMonitor:
    def __init__(self):
        self.batch = deque(maxlen=100)  # Use deque to limit memory usage
        self.batch_size = 50  # Increased batch size
        self.last_activity = time.time()
        self.last_screenshot_time = time.time()  # Track last screenshot time
        self.last_mouse_event_time = time.time()  # Throttle mouse events

    def on_keystroke(self, key):
        self.record_activity({
            'type': 'keystroke',
            'timestamp': datetime.now().isoformat(),
            'metadata': str(key)[:1]  # First character only
        })

    def on_mouse_move(self, x, y):
        current_time = time.time()
        # Throttle mouse events to 10 events per second
        if current_time - self.last_mouse_event_time > 0.1:
            self.record_activity({
                'type': 'mouse_move',
                'timestamp': datetime.now().isoformat(),
                'position': (x, y)
            })
            self.last_mouse_event_time = current_time

    def capture_screenshot(self):
        try:
            img = ImageGrab.grab()
            fn = os.path.join("screenshots", f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
            img.save(fn)
            return fn
        except Exception as e:
            print(f"Capture error: {e}")
            return None

    def get_active_window(self):
        try:
            return gw.getActiveWindow().title
        except Exception as e:
            print(f"Window capture error: {e}")
            return "Unknown Window"

    def record_activity(self, data):
        # Only check active window for significant events (keystrokes or clicks)
        if data['type'] in ['keystroke', 'mouse_click']:
            data['window'] = self.get_active_window()
        else:
            data['window'] = None

        self.batch.append(data)
        
        # Send batch if it reaches the batch size
        if len(self.batch) >= self.batch_size:
            self.send_batch()

    def send_batch(self):
        try:
            # Log resource usage for monitoring
            self.log_resource_usage()

            # Capture screenshot only every 5 minutes or on significant activity
            if time.time() - self.last_screenshot_time > 300:  # 300 seconds = 5 minutes
                screenshot = self.capture_screenshot()
                self.last_screenshot_time = time.time()
            else:
                screenshot = None

            payload = {
                'activities': list(self.batch),  # Convert deque to list for JSON serialization
                'screenshot': screenshot,
                'machine_id': 'LOCAL_DEV_MACHINE'
            }

            # Use threading to write data asynchronously
            threading.Thread(target=self.write_data, args=(payload,)).start()
            self.batch.clear()  # Clear the batch after sending
        except Exception as e:
            print(f"Upload error: {e}")

    def write_data(self, payload):
        try:
            fn = os.path.join("data", f"{datetime.now().timestamp()}.json")
            with open(fn, 'w') as f:
                json.dump(payload, f)
        except Exception as e:
            print(f"Error writing data: {e}")

    def log_resource_usage(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        logging.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    monitor = ActivityMonitor()
    with keyboard.Listener(on_press=monitor.on_keystroke) as klistener:
        with mouse.Listener(on_move=monitor.on_mouse_move) as mlistener:
            while True:
                time.sleep(0.1)  # Add a small sleep interval to reduce CPU usage
                klistener.join()
                mlistener.join()