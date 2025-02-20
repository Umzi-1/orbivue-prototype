# Endpoint Agent

The Endpoint Agent is a lightweight monitoring tool designed to capture user activity on Windows machines. It logs keystrokes, mouse movements, active windows, and captures screenshots, storing the data locally for further processing.

## Features
- **Keystroke Logging:** Captures keystrokes (metadata only, no sensitive data).
- **Mouse Activity Tracking:** Logs mouse movements and idle time.
- **Active Window Tracking:** Records the currently active window title.
- **Screenshot Capture:** Takes periodic screenshots.
- **Local Data Storage:** Stores data in JSON files and screenshots in a local directory.

## Prerequisites
- Python 3.9+
- Windows OS (Tested on Windows 10/11)

## Installation
### Clone the Repository
```bash
git clone <repository-url>
cd monitoring_prototype/endpoint_agent
```

### Set Up a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration
The agent requires no additional configuration. By default:
- Data is stored in the `data/` folder.
- Screenshots are stored in the `screenshots/` folder.

## Usage
### Run the Agent
```bash
python agent.py
```

### Perform Activities
- Type on the keyboard.
- Move the mouse.
- Switch between applications.

### View Captured Data
- JSON files containing activity logs are saved in the `data/` folder.
- Screenshots are saved in the `screenshots/` folder.

## Folder Structure
```
endpoint_agent/
├── agent.py                # Main monitoring script
├── requirements.txt        # Python dependencies
├── data/                   # Auto-created folder for JSON data
│   └── *.json             # Generated activity logs
└── screenshots/            # Auto-created folder for screenshots
    └── *.png              # Captured screenshots
```

## Dependencies
- `pynput==1.7.6`: For keyboard and mouse input monitoring.
- `pygetwindow==0.0.9`: For active window tracking.
- `Pillow==10.0.1`: For screenshot capture.
- `pywin32==306`: For Windows-specific functionality.

## Limitations
- **Local Storage Only:** Data is stored locally and not uploaded to a server.
- **No Encryption:** Data is stored in plain JSON and PNG formats.
- **Windows Only:** Designed specifically for Windows OS.

## Stopping the Agent
Press `Ctrl + C` in the Command Prompt window to stop the agent.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer
This tool is intended for educational and testing purposes only. Ensure you have proper authorization before using it on any system. The developers are not responsible for any misuse of this software.
