import os
import time
import re
import datetime
import subprocess
import pygetwindow as gw
import pyautogui
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as selenium_exceptions

# === CONFIG ===
VIDEO_DURATION = 50  # seconds
screen_width, screen_height = pyautogui.size()

#VIDEO_SIZE = f"{screen_width}x{screen_height}"
VIDEO_SIZE = "2560, 1380" #2k Monitor= 2560x1440. Reduced Y value to cut off bottom taskbar"
#CAPTURE_WIDTH = 1080
#CAPTURE_HEIGHT = 600
OUTPUT_FOLDER = r"C:\Users\danie\OneDrive\Desktop\FFmpeg Automation\Recordings"
SPREADSHEET_PATH = "La Fleur Test Lead List.xlsx"

# === SETUP ===
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def url_to_clean_name(url: str) -> str:
    cleaned = re.sub(r"https?://(www\.)?", "", url)
    cleaned = re.sub(r"[^\x00-\x7F]+", "", cleaned)  # Remove non-ASCII
    cleaned = re.sub(r"[^\w]", "_", cleaned)
    domain = cleaned.split("_")[0]
    date_str = datetime.datetime.now().strftime("%d.%m.%Y")
    return f"{domain}.{date_str}.mp4"

def record_website(url, output_path):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1875,1080")  
    # Hides the automation bar
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Hides banner
    chrome_options.add_experimental_option("useAutomationExtension", False)  # Disables extra automation tracking

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)
    except selenium_exceptions.WebDriverException as e:
        print(f"❌ Error loading {url}: {e}")
        driver.quit() 
        return  # Skip this URL and move to the next one
    
    chrome_window = None
    for w in gw.getWindowsWithTitle('Chrome'):
        if 'chrome' in w.title.lower() and 'devtools' not in w.title.lower():
            chrome_window = w
            break

    if not chrome_window:
        print(f"❌ Could not find Chrome window for {url}")
        driver.quit()
        return

    # Resize Chrome to be slightly larger than capture area
    chrome_window.moveTo(-10, 0)

    try:
        chrome_window.activate()
    except Exception as e:
        print(f"⚠️ Window activation skipped due to: {e}")
    time.sleep(1)

    ffmpeg_cmd = [
        
        r"C:\ffmpeg\bin\ffmpeg.exe", '-y', '-f', 'gdigrab',
        '-framerate', '30',
        '-offset_x', '0',
        #'-offset_y', '0',
        '-offset_y', '0',
        '-video_size', VIDEO_SIZE,
        
        '-i', 'desktop',
        '-t', str(VIDEO_DURATION),
        '-pix_fmt', 'yuv420p',
        '-vcodec', 'libx264',
        '-preset', 'veryfast',
        output_path
    ]
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd)

    # Simulate natural scrolling behavior
    time.sleep(1)
    driver.execute_script("document.body.style.zoom='80%'")


    #Added vertical height percentages instead of pixel heights so both short and long pages can behave accordingly

    scroll_percentages = [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9]
    
    for percentage in scroll_percentages:
        # Get the height of the entire page
        page_height = driver.execute_script("return document.documentElement.scrollHeight")
        # Calculate the scroll position based on the percentage
        scroll_position = int(page_height * percentage)
        
        # Scroll to the calculated position
        #driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        driver.execute_script("window.scrollTo({ 'top': 0, 'behavior': 'smooth' });")
        
        # Wait for a random time between 4 and 8 seconds to simulate human scrolling speed
        time.sleep(random.uniform(4.0, 6.0))


    #scroll_points = [300, 900, 1500, 2400]
#    scroll_points = [random.randint(200, 800), random.randint(900, 1400), random.randint(1500, 2200), random.randint(2300, 3000)]
#
#    for y in scroll_points:
#        driver.execute_script(f"window.scrollTo({{top: {y}, behavior: 'smooth'}});")
#        #time.sleep(random.uniform(1.5, 3.5))
#        time.sleep(random.uniform(2.0, 5.0))  # Was 1.5-3.5, now slower and more natural

    # Quick scroll back to top
    time.sleep(1)
    driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
    time.sleep(2)


    scroll_percentages2 = [ 0.2, 0.5]

    for percentage in scroll_percentages2:
        # Get the height of the entire page
        page_height = driver.execute_script("return document.documentElement.scrollHeight")
        # Calculate the scroll position based on the percentage
        scroll_position = int(page_height * percentage)
        
        # Scroll to the calculated position
        #driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        driver.execute_script(f"window.scrollTo({{top: {scroll_position}, behavior: 'smooth'}});")
        
        # Wait for a random time between 4 and 8 seconds to simulate human scrolling speed
        time.sleep(random.uniform(2.0, 5.0))
    time.sleep(2)

    driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")

    time.sleep(5)


    ffmpeg_process.wait()
    driver.quit()
    print(f"✅ Finished recording: {output_path}")

# === MAIN ===
if __name__ == "__main__":
    print("📄 Reading spreadsheet...")
    df = pd.read_excel(SPREADSHEET_PATH, header=0)
    print("📌 Columns found:", df.columns.tolist())  # Debug line

    # Print preview of first few rows (to verify data)
    print(df.head())

    # Try to access column with trimmed whitespace
    column_matches = [col for col in df.columns if "company website" in col.lower()]

    if column_matches:
        column_name = column_matches[0]
        urls = df[column_name].dropna().unique().tolist()

        #testing row number
        start_index = 19
        for url in urls[start_index:]:
        #for url in urls:
            filename = url_to_clean_name(url)
            output_path = os.path.join(OUTPUT_FOLDER, filename)

            print(f"\n🎬 Recording {url}...")
            record_website(url, output_path)
    else:
        print("❌ Could not find a 'Company Website' column. Check your spreadsheet headers.")

    print("\n✅ All recordings completed and saved locally.")
