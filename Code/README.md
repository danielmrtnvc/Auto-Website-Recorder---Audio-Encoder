# Auto Website Recorder v4

## Overview
Auto Website Recorder v4 is a Python automation script that records website interactions and scroll behavior for a list of URLs. It uses Selenium to open websites, PyAutoGUI to manipulate browser windows, and FFmpeg to capture screen recordings.

## Requirements
Before running this script, ensure you have the following installed on your system:

- **Python** (>= 3.8)
- **Google Chrome** (latest version recommended)
- **FFmpeg** (must be installed and accessible via `C:\ffmpeg\bin\ffmpeg.exe`)
- Required Python packages (install via `pip install -r requirements.txt`):
  - `selenium`
  - `pygetwindow`
  - `pyautogui`
  - `pandas`

## Installation
1. **Install FFmpeg:**
   - Download FFmpeg from https://ffmpeg.org/download.html.
   - Extract and place it in `C:\ffmpeg\bin\`.
   - Ensure `ffmpeg.exe` is located at `C:\ffmpeg\bin\ffmpeg.exe`.

2. **Install Python dependencies:**
   ```sh
   pip install selenium pygetwindow pyautogui pandas
   ```

3. **Ensure Chrome WebDriver is installed:**
   - Download the compatible `chromedriver.exe` from https://sites.google.com/chromium.org/driver/.
   - Place it in a directory accessible via PATH or alongside the script.

## Usage
1. **Prepare Your Spreadsheet:**
   - Place your Excel file (`La Fleur Test Lead List.xlsx`) in the same directory.
   - Ensure it has a column named "Company Website" (case-insensitive) containing the list of URLs.

2. **Run the Script:**
   ```sh
   python Auto_Website_Recorder_v4.py
   ```

3. **Output:**
   - The recordings will be saved in the directory specified by `OUTPUT_FOLDER` (default: `C:\Users\danie\OneDrive\Desktop\FFmpeg Automation\Recordings`).

## Configurable Settings
You can modify the following settings in the script to adjust the recording behavior:

| Setting            | Description                                  | Default Value |
|-------------------|---------------------------------|--------------|
| `VIDEO_DURATION` | Duration of each recording (seconds) | `50` |
| `VIDEO_SIZE` | Resolution of the recorded video | `2560,1380` (2K monitor, adjusted height) |
| `OUTPUT_FOLDER` | Directory where recordings are saved | `C:\Users\danie\OneDrive\Desktop\FFmpeg Automation\Recordings` |
| `SPREADSHEET_PATH` | Path to the Excel file containing URLs | `La Fleur Test Lead List.xlsx` |

## How It Works
1. The script reads URLs from an Excel file.
2. It opens each URL in Chrome with automation settings disabled.
3. FFmpeg captures the screen while the script scrolls naturally through the page.
4. The recording is saved as an `.mp4` file, named based on the website domain and date.

## Notes
- Ensure Chrome is not already running before executing the script.
- If FFmpeg does not start, check if the path to `ffmpeg.exe` is correctly set.
- The script will attempt to activate the Chrome window before recording to ensure proper focus.

## Troubleshooting
- **FFmpeg not found error?**
  - Ensure `ffmpeg.exe` is installed at `C:\ffmpeg\bin\ffmpeg.exe`.
  - Add `C:\ffmpeg\bin\` to your system `PATH` environment variable.

- **Chrome not detected?**
  - Ensure Chrome is installed and up to date.
  - Verify that `chromedriver.exe` matches your Chrome version.

- **Script not scrolling properly?**
  - Adjust the `scroll_percentages` in the script to customize scroll behavior.
  
---

This script is intended for private use only. Modify it as needed to suit your automation needs!

# Audio Encoder

## Description
This script processes video files by attaching an external audio track to them using FFmpeg. It scans a designated folder for video files, merges them with a predefined audio file, and saves the final versions in a separate output folder.

## Prerequisites
- **FFmpeg**: This script requires FFmpeg to be installed on your machine. You can download it from:
  
  https://ffmpeg.org/download.html

- **Folder Structure**:
  - `Recordings` folder containing the original videos.
  - `Final` folder where processed videos will be saved.
  - `audio.m4a` file (or another specified audio file) to be added to the videos.

## How to Use
1. Ensure FFmpeg is installed and accessible.
2. Place the videos you want to process in the `Recordings` folder.
3. Ensure the audio file is correctly referenced in the script (`audio.m4a` by default).
4. Run the script:
   ```sh
   python Audio_Encoder.py
   ```
5. The processed videos with attached audio will be saved in the `Final` folder.

## Configuration
You can adjust the following settings in the script:
- **`recordings_folder`**: Path to the folder containing original video files.
- **`final_folder`**: Path where the processed videos will be saved.
- **`audio_file`**: Path to the audio file that will be added to the videos.

## Supported Video Formats
The script currently processes:
- `.mp4`
- `.mkv`
- `.avi`

More formats can be added by modifying this section in the script:
```python
if filename.endswith((".mp4", ".mkv", ".avi")):
```

## Output
Once processed, videos will retain their original filenames but will now include the external audio track.

✅ All processed videos will be saved in the `Final` folder.